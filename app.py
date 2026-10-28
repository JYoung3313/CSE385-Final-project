"""User Manager: a small Flask + MySQL CRUD demo for a database systems course."""
import csv
import io
import os
import secrets

from dotenv import load_dotenv
from flask import (Flask, Response, abort, flash, redirect, render_template,
                   request, session, url_for)
from mysql.connector import Error, errorcode, pooling

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")

# One pool for the whole app: connections are expensive, so reuse them.
pool = pooling.MySQLConnectionPool(
    pool_name="webpool",
    pool_size=5,
    host=os.environ.get("DB_HOST", "localhost"),
    port=int(os.environ.get("DB_PORT", 3306)),
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DB_NAME"],
)

ROLES = ("student", "instructor", "admin")
# Identifiers cannot be parameterized, so we whitelist sortable columns.
SORTABLE = {"user_id": "user_id", "name": "full_name", "email": "email",
            "role": "role", "created": "created_at"}


# ---------- database helper ----------
def run(sql, params=(), *, fetch=False, commit=False):
    """Run ONE parameterized statement and always give the connection back."""
    conn = pool.get_connection()
    cur = None
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params)
        if commit:
            conn.commit()
        return cur.fetchall() if fetch else cur.rowcount
    except Error:
        conn.rollback()
        raise
    finally:
        if cur:
            cur.close()
        conn.close()  # returns the connection to the pool


# ---------- CSRF protection (state-changing requests only) ----------
def csrf_token():
    if "_csrf" not in session:
        session["_csrf"] = secrets.token_hex(16)
    return session["_csrf"]


app.jinja_env.globals["csrf_token"] = csrf_token
app.jinja_env.globals["ROLES"] = ROLES


@app.before_request
def verify_csrf():
    if request.method == "POST":
        sent = request.form.get("_csrf", "")
        if not secrets.compare_digest(sent, session.get("_csrf", "")):
            abort(400, "Invalid CSRF token")


# ---------- validation ----------
def read_form(form):
    data = {
        "full_name": form.get("full_name", "").strip(),
        "email": form.get("email", "").strip().lower(),
        "role": form.get("role", "student"),
        "is_active": 1 if form.get("is_active") else 0,
    }
    errors = []
    if not data["full_name"] or len(data["full_name"]) > 100:
        errors.append("Name is required (max 100 characters).")
    if "@" not in data["email"] or len(data["email"]) > 120:
        errors.append("A valid email is required.")
    if data["role"] not in ROLES:
        errors.append("Invalid role.")
    return data, errors


def db_error_message(e):
    if e.errno == errorcode.ER_DUP_ENTRY:
        return "That email is already registered."
    app.logger.exception("Database error")  # details go to the log, not the user
    return "A database error occurred. Please try again."


# ---------- READ: list + search + sort ----------
@app.route("/")
def index():
    q = request.args.get("q", "").strip()
    sort = request.args.get("sort", "user_id")
    column = SORTABLE.get(sort, "user_id")
    users = run(
        f"SELECT * FROM users WHERE full_name LIKE %s OR email LIKE %s "
        f"ORDER BY {column}",           # column comes from our whitelist, not the user
        (f"%{q}%", f"%{q}%"), fetch=True)
    return render_template("index.html", users=users, q=q, sort=sort)


# ---------- CREATE ----------
@app.route("/users/new", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        data, errors = read_form(request.form)
        if not errors:
            try:
                run("INSERT INTO users (full_name, email, role, is_active) "
                    "VALUES (%(full_name)s, %(email)s, %(role)s, %(is_active)s)",
                    data, commit=True)
                flash("User added.", "ok")
                return redirect(url_for("index"))
            except Error as e:
                errors.append(db_error_message(e))
        for err in errors:
            flash(err, "error")
        return render_template("form.html", user=data, mode="Add")
    return render_template("form.html",
                           user={"role": "student", "is_active": 1}, mode="Add")


# ---------- UPDATE ----------
@app.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
def edit(user_id):
    rows = run("SELECT * FROM users WHERE user_id = %s", (user_id,), fetch=True)
    if not rows:
        abort(404)
    if request.method == "POST":
        data, errors = read_form(request.form)
        data["user_id"] = user_id
        if not errors:
            try:
                run("UPDATE users SET full_name=%(full_name)s, email=%(email)s, "
                    "role=%(role)s, is_active=%(is_active)s "
                    "WHERE user_id=%(user_id)s", data, commit=True)
                flash("User updated.", "ok")
                return redirect(url_for("index"))
            except Error as e:
                errors.append(db_error_message(e))
        for err in errors:
            flash(err, "error")
        return render_template("form.html", user=data, mode="Edit")
    return render_template("form.html", user=rows[0], mode="Edit")


# ---------- DELETE (POST only: GET must never change data) ----------
@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete(user_id):
    removed = run("DELETE FROM users WHERE user_id = %s", (user_id,), commit=True)
    flash("User removed." if removed else "User not found.",
          "ok" if removed else "error")
    return redirect(url_for("index"))


# ---------- REPORT ----------
@app.route("/report")
def report():
    totals = run("SELECT COUNT(*) AS total, COALESCE(SUM(is_active),0) AS active "
                 "FROM users", fetch=True)[0]
    by_role = run("SELECT role, COUNT(*) AS total, SUM(is_active) AS active "
                  "FROM users GROUP BY role ORDER BY total DESC", fetch=True)
    recent = run("SELECT full_name, email, role, created_at FROM users "
                 "ORDER BY created_at DESC, user_id DESC LIMIT 5", fetch=True)
    sql_report_data = run("SELECT * FROM users ORDER BY user_id", fetch=True)
    
    return render_template("report.html", totals=totals, by_role=by_role,
                           recent=recent, sql_report_data=sql_report_data)


@app.route("/report.csv")
def report_csv():
    rows = run("SELECT user_id, full_name, email, role, is_active, created_at "
               "FROM users ORDER BY user_id", fetch=True)
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["user_id", "full_name", "email", "role", "is_active", "created_at"])
    for r in rows:
        writer.writerow(r.values())
    return Response(buf.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=users.csv"})



# ---------- connection check (handy in class) ----------
@app.route("/health")
def health():
    try:
        run("SELECT 1", fetch=True)
        return {"database": "ok"}
    except Error:
        return {"database": "unreachable"}, 503


if __name__ == "__main__":
    app.run(debug=True)
