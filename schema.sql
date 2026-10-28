-- Run as a MySQL admin:  mysql -u root -p < schema.sql
CREATE DATABASE IF NOT EXISTS webdemo CHARACTER SET utf8mb4;
USE webdemo;

CREATE TABLE IF NOT EXISTS users (
  user_id    INT AUTO_INCREMENT PRIMARY KEY,
  full_name  VARCHAR(100) NOT NULL,
  email      VARCHAR(120) NOT NULL UNIQUE,
  role       ENUM('student','instructor','admin') NOT NULL DEFAULT 'student',
  is_active  TINYINT(1) NOT NULL DEFAULT 1,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
             ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_users_role (role)
);

INSERT INTO users (full_name, email, role, is_active) VALUES
  ('Ada Lovelace',  'ada@example.edu',   'instructor', 1),
  ('Alan Turing',   'alan@example.edu',  'student',    1),
  ('Grace Hopper',  'grace@example.edu', 'admin',      1),
  ('Edsger Dijkstra','edsger@example.edu','student',   0);

-- Least-privilege account for the web app (change the password!)
CREATE USER IF NOT EXISTS 'webapp'@'localhost' IDENTIFIED BY 'ChangeMe!123';
GRANT SELECT, INSERT, UPDATE, DELETE ON webdemo.users TO 'webapp'@'localhost';
FLUSH PRIVILEGES;
