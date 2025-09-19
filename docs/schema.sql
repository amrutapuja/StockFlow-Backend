CREATE DATABASE stockflow;
CREATE USER 'stockuser'@'localhost' IDENTIFIED BY 'stockpass';
GRANT ALL PRIVILEGES ON stockflow.* TO 'stockuser'@'localhost';
FLUSH PRIVILEGES;
