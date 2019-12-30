last_transactions_headers = ['Transaction Date', 'City', 'Brand', 'Car Age', 'Price', 'Payment type', 'Salesman']

last_transactions_query = '''
    SELECT
        transaction_date,
        transactions.city,
        brand,
        CONCAT(car_age,' years'),
        CONCAT(price,' $'),
        payment_type,
        name as 'employee name'
    FROM transactions
    LEFT JOIN makers
        ON transactions.maker_id=makers.id
    LEFT JOIN payments
        ON transactions.payment_id=payments.id
    LEFT JOIN employees
        ON transactions.employee_id = employees.id
    ORDER BY transaction_date DESC LIMIT %s '''

turnover_headers = ['Brand', 'Turnover']

turnover_query = '''
            SELECT 
                brand,
                SUM(price) as turnover
            FROM transactions
            JOIN makers
                ON transactions.maker_id=makers.id
            GROUP BY maker_id
            ORDER BY turnover DESC LIMIT %s'''


description = '''
This tkinter GUI connects with fake database which I created to present MySQL skills. 
This is a simplified database which represents imaginary company “West Coast Cars” 
which is selling new and used cars across USA. “WCC” has 61 employees and sells 50 brands.
Starting from 1st of January 2017 till the end of 2019 company sold 1577 cars
what is shown in the transactions table.

Tables in DB:

61 employees:
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

'''