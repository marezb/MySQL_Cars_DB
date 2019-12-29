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
    ORDER BY transaction_date DESC LIMIT 20
    '''

turnover_headers = ['Brand', 'Turnover']

turnover_query = '''
            SELECT 
                brand,
                SUM(price) as turnover
            FROM transactions
            JOIN makers
                ON transactions.maker_id=makers.id
            GROUP BY maker_id
            ORDER BY turnover DESC LIMIT 3
            '''