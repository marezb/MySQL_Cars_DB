# MySQL_Cars_DB
This is a fake database which holds data of “West Coast Cars” company.
"WCC" is selling new and used cars across USA. The company has 60 employees and sells 50 brands.
Starting from 1st of January 2017 till the end of 2019 the company sold 1577 cars.
Using the menu on the right side you can filter this database to check aggregated data from all 4 tables.


Tables in DB:

60 employees:
  CREATE TABLE employees (
    id INT NOT NULL auto_increment PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    address VARCHAR(255)NOT NULL,
    telephone VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW());

50 brands:
CREATE TABLE makers(
    id INT NOT NULL auto_increment PRIMARY KEY,
    brand VARCHAR(100) NOT NULL);

5 payment types:
  CREATE TABLE payments(
    id INT NOT NULL auto_increment PRIMARY KEY,
    payment_type VARCHAR(100) NOT NULL);

1577  sales records:
  CREATE TABLE transactions (
    id INT NOT NULL auto_increment PRIMARY KEY,
    transaction_date DATE NOT NULL,
    city VARCHAR(100) NOT NULL,
    car_age INT NOT NULL,
    price INT NOT NULL,
    maker_id INT NOT NULL,
    payment_id INT NOT NULL,
    employee_id INT NOT NULL,
    FOREIGN KEY(maker_id) REFERENCES makers(id),
    FOREIGN KEY(payment_id) REFERENCES payments(id),
    FOREIGN KEY(employee_id) REFERENCES employees(id));
