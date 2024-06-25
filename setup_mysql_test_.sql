-- Create the database
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create new user
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY hbnb_test_pwd;

-- Grant privileges
GRANT ALL PRIVILEGES ON 'hbnb_test_db'.* TO 'hbnb_test'@'localhost';

-- Grant SELECT Privilege
GRANT SELECT ON 'performance_schema'.* TO 'hbnb_test'@'localhost';

-- Apply the changes
FLUSH PRIVILEGES;

