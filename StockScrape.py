# StockScrape
import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_stock_details(stock_symbol):
    try:
        url = 'https://www.google.com/finance'

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        input_element = soup.find('input', class_='Ax4B8 ZAGvjd')

        input_name = input_element.get('name')
        autocomplete = input_element.get('autocomplete')
        aria_controls = input_element.get('aria-controls')

        payload = {
            'q': stock_symbol,
            'autocomplete': autocomplete,
            'o': stock_symbol,
            'gs_l': 'finance-immersive'
        }

        response = requests.get(url, params=payload)
        soup = BeautifulSoup(response.content, 'html.parser')


        price_element = soup.find('div', class_='YMlKec fxKbKc')
        price = price_element.text.strip()


        elements = soup.find_all('div', class_='mfs7Fc')
        elemtnts1 = soup.find_all('div',class_='P6K39c')

        arr1 = []
        arr2 = []

        for element, elem in zip(elements, elemtnts1):
            text = element.text.strip()
            arr1.append(text)
            text1 = elem.text.strip()
            arr2.append(text1)

        tuple1 = tuple(arr1)
        tuple2 = tuple(arr2)

        dic = {'Content':tuple1,'Result':tuple2}
        df = pd.DataFrame(dic)

        return price, df
    except AttributeError:
        return None

def show_stock_details():
    stock_symbol = stock_entry.get()
    result = get_stock_details(stock_symbol)

    if result is not None:
        price, details = result
        if price is not None:
            price_label.config(text=f"The price of {stock_symbol} is: {price}")
        else:
            price_label.config(text=f"Invalid stock symbol: {stock_symbol}")
        
        treeview.delete(*treeview.get_children())
        if details is not None:
            for index, row in details.iterrows():
                treeview.insert("", "end", values=row.tolist())
    else:
        price_label.config(text="Error retrieving stock details.")

root = tk.Tk()
root.title("Stock Details")
root.geometry("480x480")
root.configure(bg="#e6e6e6")

stock_label = tk.Label(root, text="Enter the name of Stock:")
stock_label.pack()
stock_entry = tk.Entry(root)
stock_entry.pack()


show_button = tk.Button(root, text="Show Details", command=show_stock_details)
show_button.pack()


price_label = tk.Label(root)
price_label.pack()


treeview = ttk.Treeview(root, columns=("Content", "Result"), show="headings")
treeview.heading("Content", text="Content")
treeview.heading("Result", text="Result")
treeview.pack()

root.mainloop()
