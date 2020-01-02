################################### Last Transactions ################################################
last_transactions_headers = ['Transaction Date', 'City', 'Brand', 'Brand Category',
                             'Car Age','Car Condition','Price', 'Payment type', 'Salesman']

last_transactions_query_desc = '''
Show last transactions with details: date, price, brand name, 
employee name and type of payment. Requires connection of data from all tables.
'''
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
        CONCAT(FORMAT(price,0),' $') AS price,
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

################################### Brand Turnover ################################################

turnover_headers = ['Brand', 'Turnover', 'Average age of sold cars',
                    'Number of sold cars', 'Average transaction value']
turnover_query_desc = '''
Which brand generates the highest turnover?
What is the average age of sold cars?
What is the volume of sales per unit?
What is the average transaction value?
'''
turnover_query = '''
    SELECT
        brand,
        CONCAT(FORMAT(SUM(price),0), ' $') as turnover,
        CONCAT(ROUND(AVG(car_age),1),' years') AS avg_age,
        COUNT(maker_id) as 'number of sold cars',
        CONCAT(FORMAT(SUM(price)/COUNT(maker_id),0),' $') AS average_transaction
    FROM transactions
    JOIN makers
        ON transactions.maker_id=makers.id
    WHERE transaction_date BETWEEN %s AND %s
    GROUP BY maker_id
    ORDER BY SUM(price) DESC LIMIT %s
'''

################################## Payment types #################################################

payment_headers = ['Payment type','Turnover', 'Number of transactions']

payment_query_desc ='''
Which type of payment generates the highest turnover and which one the lowest?
'''

payment_query='''
    SELECT
        payment_type,
        CONCAT(FORMAT(SUM(price),0), ' $') AS turnover,
        COUNT(payment_id) AS num_of_transactions
    FROM transactions
    JOIN payments
        ON transactions.payment_id=payments.id
    WHERE transaction_date BETWEEN %s AND %s
    GROUP BY payment_id
    ORDER BY SUM(price) DESC LIMIT %s
'''

################################### Employees performance ##############################################
employees_headers = ['Employee id','Name', 'City of operation', 'Turnover',
                     'Num of transactions', 'Average transaction value']

employees_query_desc = '''What is the performance of our employees? Who is the best, where she/he operates?'''

employees_guery='''
    SELECT
        employees.id,
        employees.name,
        employees.city,
        CONCAT(FORMAT(SUM(price),0), ' $') AS turnover,
        COUNT(*) AS num_of_transactions,
        CONCAT(FORMAT(AVG(price),0),' $') AS avg_transaction_value
    FROM transactions
    RIGHT JOIN employees
        ON transactions.employee_id = employees.id
    WHERE transactions.transaction_date BETWEEN %s AND %s
        GROUP BY employees.id
    ORDER BY SUM(price) DESC LIMIT %s
'''



application_description = '''
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

'''