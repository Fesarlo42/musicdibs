-- Create normal user
CREATE USER IF NOT EXISTS 'musicdibs_user'@'localhost' IDENTIFIED BY '${MYSQL_USER_PASSWORD}';
GRANT SELECT, INSERT, UPDATE, DELETE ON musicdibs.* TO 'musicdibs_user'@'localhost';

-- Create admin for maintenance tasks
CREATE USER IF NOT EXISTS 'musicdibs_admin'@'localhost' IDENTIFIED BY '${MYSQL_ADMIN_PASSWORD}';
GRANT ALL PRIVILEGES ON musicdibs.* TO 'musicdibs_admin'@'localhost';

FLUSH PRIVILEGES;