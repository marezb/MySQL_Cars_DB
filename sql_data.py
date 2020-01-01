last_transactions_headers = ['Transaction Date', 'City', 'Brand', 'Brand Category',
                             'Car Age','Car Condition','Price', 'Payment type', 'Salesman']

last_transactions_query_desc = '''Show last transactions with details: date, price, brand name, 
employee name and type of payment. Requires data from all tables. '''
last_transactions_query = '''
    SELECT
        transaction_date,
        transactions.city,
        brand,
           CASE
               WHEN brand LIKE 'Aston Martin'
                        OR brand LIKE 'Bentley'
                        OR brand LIKE 'Bugatti'
                        OR brand LIKE 'Ferrari'
                        OR brand LIKE 'Jaguar'
                        OR brand LIKE 'Maserati'
                        OR brand LIKE 'Porsche'
                        OR brand LIKE 'Rolls-Royce'
                        OR brand LIKE 'Lamborghini'
                   THEN 'Luxury'
                   ELSE 'Standard'
            END AS 'brand category',
        CONCAT(car_age,' years') AS 'car age',
           CASE
               WHEN car_age = 0 THEN 'New Car'
                ELSE 'Used Car'
            END AS 'condition',
        CONCAT(price,' $') AS price,
        payment_type,
        name as 'Salesman'
    FROM transactions
    LEFT JOIN makers
        ON transactions.maker_id=makers.id
    LEFT JOIN payments
        ON transactions.payment_id=payments.id
    LEFT JOIN employees
        ON transactions.employee_id = employees.id
    WHERE transaction_date BETWEEN %s AND %s
    ORDER BY transaction_date DESC LIMIT %s
    '''


turnover_headers = ['Brand', 'Turnover']
turnover_query_desc = '''Which brand generates the biggest turnover? '''
# turnover_query = '''
#     SELECT
#         brand,
#         CONCAT(SUM(price), ' $') AS turnover
#     FROM transactions
#     JOIN makers
#         ON transactions.maker_id=makers.id
#     GROUP BY maker_id
#     ORDER BY turnover DESC LIMIT %s'''

turnover_query = '''
SELECT
    employees.id,
    employees.name,
    SUM(price) AS 'TURNOVER',
    COUNT(*) AS 'NUM OF TRANSACTIONS',
    CONCAT(ROUND(AVG(price),2),' $') AS 'AVERAGE TRANSACTION PRICE'
FROM transactions
RIGHT JOIN employees
    ON transactions.employee_id = employees.id
    WHERE transaction_date BETWEEN '2018-01-01' AND '2018-12-31'
    GROUP BY employees.id
    ORDER BY SUM(price) DESC 
    LIMIT %s'''


application_description = '''
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