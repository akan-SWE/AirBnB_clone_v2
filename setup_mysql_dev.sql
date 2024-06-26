-- Create the Database
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Create the User
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Grant only SELECT Privilege to the User
GRANT SELECT ON `performance_schema`.* TO 'hbnb_dev'@'localhost';

-- Grant all privileges to the User
GRANT ALL PRIVILEGES ON `hbnb_dev_db`.* TO 'hbnb_dev'@'localhost';

-- Apply the changes
FLUSH PRIVILEGES;
