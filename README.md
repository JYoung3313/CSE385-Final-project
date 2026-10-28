# User Manager: Flask + MySQL CRUD Demo
https://gitlab.csi.miamioh.edu/zhengw22/cse385a_databasesystem_demo


A small web application for a database systems course. It can **add**, **update**,
and **remove** users, list them with search and sort, and show a **report** (totals,
users by role, recent sign-ups, CSV export).

## Quick start

```bash
# 1. Create database, table, sample data and a least-privilege account
mysql -u root -p < schema.sql

# 2. Python environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Configuration (credentials stay out of source code)
cp .env.example .env              # edit values if you changed the password

# 4. Run
python app.py                     # open http://127.0.0.1:5000
```

Check the connection at `http://127.0.0.1:5000/health`.

## Where each concept lives (`app.py`)


| Concept                           | Location                                       |
| --------------------------------- | ---------------------------------------------- |
| Connection pooling                | `pooling.MySQLConnectionPool(...)`             |
| Safe execute / release / rollback | `run()`                                        |
| Parameterized queries             | every`run(...)` call; values passed separately |
| Identifier whitelist (ORDER BY)   | `SORTABLE` and `index()`                       |
| CREATE / READ / UPDATE / DELETE   | `create()`, `index()`, `edit()`, `delete()`    |
| Aggregation report                | `report()` (`COUNT`, `SUM`, `GROUP BY`)        |
| Constraint to friendly error      | `db_error_message()` (duplicate email)         |
| CSRF and POST-only deletes        | `verify_csrf()`, `delete()`                    |

## Student exercises

1. Add pagination with `LIMIT` / `OFFSET`.
2. Add a `departments` table with a foreign key and show it in the report.
3. Replace hard delete with soft delete (`deleted_at`).
4. Run `EXPLAIN` on the search query; add an index and compare.
5. Break it on purpose: build one query with an f-string, then attack it.

## Troubleshooting

- *Access denied*: password in `.env` must match `schema.sql`.
- *Can't connect*: is MySQL running, and are host and port correct?
- *Too many connections*: a code path forgot to release its connection.

## Demo pages

Home page: ![Home page](.\images\index.png)
Add user: ![Home page](.\images\add_user.png)
Report: ![Report](.\images\report.png)


Educational demo: before real deployment add authentication, HTTPS, TLS to the
database, and a production WSGI server (e.g. gunicorn).
