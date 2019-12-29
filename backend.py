import tkinter as tk
from tkinter import ttk
import mysql.connector
from tabulate import tabulate
import base64
from sql_data import *


class DisplayWindow(ttk.Frame):

    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

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

        ##right frame
        self.right_side_buttons = ttk.Frame(self)
        self.right_side_buttons.grid(row=0, column=1, sticky='NSEW')
        self.right_side_buttons.columnconfigure(0, weight=1)
        self.right_side_buttons.rowconfigure((0,9), weight=0)
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
        self.title = ttk.Label(self.right_side_buttons,
                               text="Query buttons",
                               justify=tk.RIGHT
                               )
        self.title.grid(column=0, row=0, sticky='ew', padx=15, pady=5)

        self.button_1 = ttk.Button(self.right_side_buttons,
                                   text='Show Last Transactions',
                                   command=self.last_transactions)
        self.button_1.grid(column=0, row=1, pady=10, padx=15, sticky='ewn')
        self.button_2 = ttk.Button(self.right_side_buttons,
                                   text='Turnover',
                                   command=self.turnover)
        self.button_2.grid(column=0, row=2, pady=10, padx=15, sticky='ewn')

    # function which connects to database then prints result to text window

    def connect_to_db(self, table_headers, sql_query):
        query_results = list()
        pasw = base64.b64decode("MVRzY25MQkJiSg==").decode("utf-8")

        # connection to datebase
        connection = mysql.connector.connect(host='remotemysql.com',
                                             database='rPxEEccXtK',
                                             user='rPxEEccXtK',
                                             password=pasw)

        cursor = connection.cursor()
        cursor.execute(sql_query)
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
        self.text.insert(tk.END, 'MySQL query:\n')
        self.text.insert(tk.END, sql_query)
        self.text.insert(tk.END, '\nMySQL query results:\n')
        self.text.insert(tk.END, (f"Total records: {cursor.rowcount}\n\n"))
        self.text.insert(tk.END, tabulate(query_results, table_headers,
                                                     tablefmt='psql',
                                                     stralign='right',
                                                     numalign='right'))

        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed")

    def last_transactions(self):

        self.connect_to_db(last_transactions_headers, last_transactions_query)

    def turnover(self):

        self.connect_to_db(turnover_headers, turnover_query)
