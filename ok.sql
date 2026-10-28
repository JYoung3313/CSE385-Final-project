-- Select * from users
-- SELECT * FROM users WHERE full_name LIKE '%{q}%'

SELECT * FROM users WHERE full_name;

-- SELECT * FROM users WHERE full_name LIKE 'zzz' OR '1'='1';


-- SELECT * FROM users WHERE zzz OR '1'='1'

-- select 'zzz' UNION SELECT user_id, email, full_name, role, is_active, created_at, updated_at FROM users

SELECT * FROM users WHERE full_name LIKE '%s' OR email LIKE '%s'