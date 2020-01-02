import mysql.connector
from tabulate import tabulate
import tkinter as tk
from tkinter import ttk
import base64
import time
from sql_data import *


# num_or_rows = tk.StringVar(value=10)

class DisplayWindow(ttk.Frame):

    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.num_of_rows = tk.StringVar(value=100)

        self.start_year = tk.StringVar(value=2017)
        self.start_month = tk.StringVar(value=1)
        self.start_day = tk.StringVar(value=1)
        self.end_year = tk.StringVar(value=2020)
        self.end_month = tk.StringVar(value=12)
        self.end_day = tk.StringVar(value=31)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        ###############################################################################################################
        # frames for elements to order them independently
        ##left frame for main text widget
        self.left_side_text = ttk.Frame(self)
        self.left_side_text.grid(row=0, column=0, sticky='NSEW')
        self.left_side_text.columnconfigure(0, weight=1)
        self.left_side_text.columnconfigure(1, weight=0)
        self.left_side_text.rowconfigure(0, weight=0)
        self.left_side_text.rowconfigure(1, weight=1)
        self.left_side_text.rowconfigure(2, weight=0)

        ##right frame for buttons and filters
        self.right_side_buttons = ttk.Frame(self)
        self.right_side_buttons.grid(row=0, column=1, sticky='NSEW')
        self.right_side_buttons.columnconfigure(0, weight=1)
        self.right_side_buttons.columnconfigure(1, weight=0)
        self.right_side_buttons.rowconfigure((0, 9), weight=0)
        self.right_side_buttons.rowconfigure(10, weight=1)

        ###############################################################################################################
        # main text widget title
        self.title = ttk.Label(self.left_side_text, text="Display window with query results")
        self.title.grid(column=0, row=0, sticky='NSWE', padx=10, pady=5)

        # main text widget
        self.text = tk.Text(self.left_side_text,
                            height=40,
                            wrap='none',
                            width=100,
                            relief='flat', )
        self.text.grid(column=0, row=1, padx=10, pady=5, sticky='nswe')

        # scrollbar vertical
        self.text_scroll = ttk.Scrollbar(self.left_side_text, orient="vertical", command=self.text.yview)
        self.text_scroll.grid(column=1, row=1, rowspan=10, sticky=("NSW"))
        self.text['yscrollcommand'] = self.text_scroll.set

        # scrollbar horizontal
        self.text_scrollx = ttk.Scrollbar(self.left_side_text, orient="horizontal", command=self.text.xview)
        self.text_scrollx.grid(column=0, row=2, sticky=("EW"))
        self.text['xscrollcommand'] = self.text_scrollx.set

        ###############################################################################################################
        # right side buttons
        ###############################################################################################################

        self.title = ttk.Label(self.right_side_buttons,
                               text="Query buttons", )
        self.title.grid(column=0, row=0, sticky='ew', padx=15, pady=50)

        self.desc1 = ttk.Label(self.right_side_buttons,
                               text="Rows to show:")
        self.desc1.grid(column=0, row=1, sticky='ew', padx=15, pady=5)

        self.rows = ttk.Entry(self.right_side_buttons, width=5, justify='center', textvariable=self.num_of_rows)
        self.rows.grid(column=1, row=1, sticky='ew', padx=15, pady=5)

        ############################################################################
        # date entry fields
        self.desc2 = ttk.Label(self.right_side_buttons,
                               text="Start date")
        self.desc2.grid(column=0, row=2, rowspan=2, sticky='ew', padx=15, pady=5)
        self.desc2 = ttk.Label(self.right_side_buttons,
                               text="Start date")
        self.desc2.grid(column=0, row=2, rowspan=2, sticky='ew', padx=15, pady=5)

        ############# description
        self.desc_year = ttk.Label(self.right_side_buttons, text=" year:")
        self.desc_month = ttk.Label(self.right_side_buttons, text="month:")
        self.desc_day = ttk.Label(self.right_side_buttons, text="  day:  ")
        self.desc_year.grid(column=1, row=2, sticky='ew', padx=15, pady=0)
        self.desc_month.grid(column=2, row=2, sticky='ew', padx=15, pady=0)
        self.desc_day.grid(column=3, row=2, sticky='ew', padx=15, pady=0)

        years = (2017, 2018, 2019, 2020)
        self.entry_start_year = ttk.Combobox(self.right_side_buttons, width=5, justify='center',
                                             textvariable=self.start_year, values=years)
        months = tuple(x for x in range(1, 13))
        self.entry_start_month = ttk.Combobox(self.right_side_buttons, width=3, justify='center',
                                              textvariable=self.start_month, values=months)
        days = tuple(x for x in range(1, 32))
        self.entry_start_day = ttk.Combobox(self.right_side_buttons, width=3, justify='center',
                                            textvariable=self.start_day, values=days)
        self.entry_start_year.grid(column=1, row=3, sticky='ew', padx=15, pady=5)
        self.entry_start_month.grid(column=2, row=3, sticky='ew', padx=15, pady=5)
        self.entry_start_day.grid(column=3, row=3, sticky='ew', padx=15, pady=5)

        self.desc3 = ttk.Label(self.right_side_buttons,
                               text="End date")
        self.desc3.grid(column=0, row=4, rowspan=2, sticky='ew', padx=15, pady=5)
        ############# description
        self.desc_end_year = ttk.Label(self.right_side_buttons, text=" year:")
        self.desc_end_month = ttk.Label(self.right_side_buttons, text="month:")
        self.desc_end_day = ttk.Label(self.right_side_buttons, text="  day:  ")
        self.desc_end_year.grid(column=1, row=4, sticky='ew', padx=15, pady=0)
        self.desc_end_month.grid(column=2, row=4, sticky='ew', padx=15, pady=0)
        self.desc_end_day.grid(column=3, row=4, sticky='ew', padx=15, pady=0)

        ############# entry
        self.entry_end_year = ttk.Combobox(self.right_side_buttons, width=4, justify='center',
                                           textvariable=self.end_year, values=years)
        self.entry_end_month = ttk.Combobox(self.right_side_buttons, width=3, justify='center',
                                            textvariable=self.end_month, values=months)
        self.entry_end_day = ttk.Combobox(self.right_side_buttons, width=3, justify='center',
                                          textvariable=self.end_day, values=days)
        self.entry_end_year.grid(column=1, row=5, sticky='ew', padx=15, pady=5)
        self.entry_end_month.grid(column=2, row=5, sticky='ew', padx=15, pady=5)
        self.entry_end_day.grid(column=3, row=5, sticky='ew', padx=15, pady=5)
        ########################################################################################

        self.button_1 = ttk.Button(self.right_side_buttons, text='Last Transactions', command=self.last_transactions)
        self.button_2 = ttk.Button(self.right_side_buttons, text='Brand Turnover', command=self.brand_turnover)
        self.button_3 = ttk.Button(self.right_side_buttons, text='Payment types', command=self.payment_types)
        self.button_4 = ttk.Button(self.right_side_buttons, text='Employees performance ',
                                   command=self.employees_performance)

        self.button_1.grid(column=0, row=6, pady=30, padx=15, sticky='ewn', columnspan=4)
        self.button_2.grid(column=0, row=7, pady=30, padx=15, sticky='ewn', columnspan=4)
        self.button_3.grid(column=0, row=8, pady=30, padx=15, sticky='ewn', columnspan=4)
        self.button_4.grid(column=0, row=9, pady=30, padx=15, sticky='ewn', columnspan=4)

        self.text.insert(tk.END, application_description, )

    # function which connects to database then prints result to text window

    def connect_to_db(self, table_headers, sql_query, description):
        query_results = list()
        pasw = base64.b64decode("MVRzY25MQkJiSg==").decode("utf-8")
        limit = int(self.num_of_rows.get())
        start_date = f'{self.start_year.get()}-{self.start_month.get()}-{self.start_day.get()}'
        end_date = f'{self.end_year.get()}-{self.end_month.get()}-{self.end_day.get()}'

        # connection to database
        t1 = time.time()
        connection = mysql.connector.connect(host='remotemysql.com', database='rPxEEccXtK',
                                             user='rPxEEccXtK', password=pasw)

        # connection = mysql.connector.connect(host='85.10.205.173',database='west_coast_cars',
        #                                      user='jack_ryan',password='64609nsf412azda8')
        print("Connection open")

        cursor = connection.cursor()
        cursor.execute(sql_query, (start_date, end_date, limit))
        records = cursor.fetchall()

        # from mysql records we need to prepare list format accepted by 'tabulate' module
        # this is a list within a list, records are divided by comma
        for record in records:
            tabulate_record = []
            index = 0
            for _ in range(len(records[0])):
                tabulate_record.append(f'{record[index]}')
                index += 1
            query_results.append(tabulate_record)

        self.text.delete('1.0', tk.END)
        self.text.insert(tk.END, description)
        self.text.insert(tk.END, '\n\nMySQL query:\n')
        self.text.insert(tk.END, sql_query, '\n')
        self.text.insert(tk.END, '\n\nMySQL query results:\n')
        self.text.insert(tk.END, (f"Total records: {cursor.rowcount}\n\n"))
        self.text.insert(tk.END, tabulate(query_results, table_headers,
                                          tablefmt='psql',
                                          stralign='right',
                                          numalign='right'))

        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed")
        t2 = time.time()
        print(f"Time of operation {((t2 - t1) * 1000):.1f} ms")

    def last_transactions(self):

        self.connect_to_db(last_transactions_headers,
                           last_transactions_query,
                           last_transactions_query_desc)

    def brand_turnover(self):

        self.connect_to_db(turnover_headers,
                           turnover_query,
                           turnover_query_desc)

    def payment_types(self):

        self.connect_to_db(payment_headers,
                           payment_query,
                           payment_query_desc)

    def employees_performance(self):

        self.connect_to_db(employees_headers,
                           employees_guery,
                           employees_query_desc)
