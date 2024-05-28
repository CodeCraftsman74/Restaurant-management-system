import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

# Connect to the MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="Restaurant_Management_System"
)

c = mydb.cursor()

def update_record(table_name, column_names, values, id=None):
    columns = ", ".join(column_names)
    placeholders = ", ".join(["%s"] * len(column_names))

    if id is None:
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        c.execute(query, values)
    else:
        set_clause = ", ".join([f"{column_name} = %s" for column_name in column_names])
        query = f"UPDATE {table_name} SET {set_clause} WHERE id = %s"
        c.execute(query, values + [id])

    mydb.commit()

def update_entry(table_name, column_names, id, entries):
    values = [entry.get() for entry in entries]
    update_record(table_name, column_names, values, id)

def show_table(table_name):
    window = tk.Toplevel(root)
    window.title(table_name)
    window.configure(bg='#F0F0F0')  # Set background color

    c.execute(f"SELECT * FROM {table_name}")
    records = c.fetchall()
    column_names = [description[0] for description in c.description]

    # Create treeview for displaying records
    tree = ttk.Treeview(window, columns=column_names, show='headings')
    tree.pack(fill='both', expand=True, padx=20, pady=20)

    # Configure column headings
    for col in column_names:
        tree.heading(col, text=col, anchor='center')
        tree.column(col, anchor='center', width=100)  # Adjust width as needed

    # Insert records into treeview
    for record in records:
        tree.insert('', 'end', values=record)

    # Add buttons for adding and editing records
    button_frame = tk.Frame(window, bg='#F0F0F0')
    button_frame.pack(fill='x', padx=20, pady=10)

    add_button = ttk.Button(button_frame, text="Add Record", command=lambda table_name=table_name, column_names=column_names, window=window: add_record(table_name, column_names, window))
    add_button.pack(side='left', padx=5)

    edit_button = ttk.Button(button_frame, text="Edit Record", command=lambda table_name=table_name, column_names=column_names, window=window: edit_record(table_name, column_names, window, tree))
    edit_button.pack(side='left', padx=5)

    # Display bar chart for SalesRepo and OrderDetails tables
    if table_name == "SalesRepo":
        plot_sales_chart(window, records, column_names)
    elif table_name == "OrderDetails":
        plot_order_chart(window, records, column_names)

def add_record(table_name, column_names, window):
    add_window = tk.Toplevel(window)
    add_window.title("Add Record")
    add_window.configure(bg='#F0F0F0')

    entries = []
    for i, column_name in enumerate(column_names):
        label = ttk.Label(add_window, text=column_name)
        label.grid(row=i, column=0, padx=10, pady=5, sticky='e')
        entry = ttk.Entry(add_window)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)

    save_button = ttk.Button(add_window, text="Save", command=lambda table_name=table_name, column_names=column_names, entries=entries: update_record(table_name, column_names, [entry.get() for entry in entries]))
    save_button.grid(row=len(column_names), column=0, columnspan=2, padx=10, pady=10)

def edit_record(table_name, column_names, window, tree):
    selected_item = tree.focus()
    if selected_item:
        record_values = tree.item(selected_item, 'values')
        record_id = record_values[0]  # Assuming the first column is the ID

        edit_window = tk.Toplevel(window)
        edit_window.title("Edit Record")
        edit_window.configure(bg='#F0F0F0')

        entries = []
        for i, value in enumerate(record_values):
            label = ttk.Label(edit_window, text=column_names[i])
            label.grid(row=i, column=0, padx=10, pady=5, sticky='e')
            entry = ttk.Entry(edit_window)
            entry.insert(0, value)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)

        save_button = ttk.Button(edit_window, text="Save", command=lambda table_name=table_name, column_names=column_names, id=record_id, entries=entries: update_record(table_name, column_names, [entry.get() for entry in entries], id))
        save_button.grid(row=len(column_names), column=0, columnspan=2, padx=10, pady=10)
    else:
        messagebox.showwarning("No Record Selected", "Please select a record to edit.")

def plot_sales_chart(window, records, column_names):
    # Extract data for bar chart
    sales_data = {}
    for record in records:
        item = record[1]  # Assuming the item name is in the second column
        quantity = record[2]  # Assuming the quantity is in the third column
        if item in sales_data:
            sales_data[item] += quantity
        else:
            sales_data[item] = quantity

    # Create bar chart
    figure = plt.Figure(figsize=(6, 4), dpi=100)
    ax = figure.add_subplot(111)
    item_names = list(sales_data.keys())
    quantities = list(sales_data.values())
    ax.bar(item_names, quantities)
    ax.set_title("Sales Data")
    ax.set_xlabel("Item")
    ax.set_ylabel("Quantity Sold")

    # Add plot to window
    canvas = FigureCanvasTkAgg(figure, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

def plot_order_chart(window, records, column_names):
    # Extract data for bar chart
    order_data = {}
    for record in records:
        item = record[1]  # Assuming the item name is in the second column
        quantity = record[2]  # Assuming the quantity is in the third column
        if item in order_data:
            order_data[item] += quantity
        else:
            order_data[item] = quantity

    # Create bar chart
    figure = plt.Figure(figsize=(6, 4), dpi=100)
    ax = figure.add_subplot(111)
    item_names = list(order_data.keys())
    quantities = list(order_data.values())
    ax.bar(item_names, quantities)
    ax.set_title("Order Data")
    ax.set_xlabel("Item")
    ax.set_ylabel("Quantity Ordered")

    # Add plot to window
    canvas = FigureCanvasTkAgg(figure, master=window)
    canvas = FigureCanvasTkAgg(figure, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    

def plot_order_chart(window, records, column_names):
    # Extract data for bar chart
    order_data = {}
    for record in records:
        item = record[1]  # Assuming the item name is in the second column
        quantity = record[2]  # Assuming the quantity is in the third column
        if item in order_data:
            order_data[item] += quantity
        else:
            order_data[item] = quantity

    # Create bar chart
    figure = plt.Figure(figsize=(6, 4), dpi=100)
    ax = figure.add_subplot(111)
    item_names = list(order_data.keys())
    quantities = list(order_data.values())
    ax.bar(item_names, quantities)
    ax.set_title("Order Data")
    ax.set_xlabel("Item")
    ax.set_ylabel("Quantity Ordered")

    # Add plot to window
    canvas = FigureCanvasTkAgg(figure, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

def main_application_window():
    window = tk.Toplevel(root)
    window.title("Main Application Window")
    window.geometry('800x600')
    window.configure(bg='#F0F0F0')

    style = ttk.Style()
    style.theme_use('clam')  # Set theme for modern look

    tables = ["userdata", "SalesRepo", "CustomerDetails", "OrderDetails", "ItemsRate", "OrderCost", "Inventory"]

    for table in tables:
        button = ttk.Button(window, text=table, command=lambda table=table: show_table(table), width=20)
        button.pack(pady=10)

def authenticate():
    username = username_entry.get()
    password = password_entry.get()

    c.execute("SELECT * FROM userdata WHERE username=%s AND password=%s", (username, password))

    if c.fetchone() is not None:
        messagebox.showinfo("Login info", "Login Successful")
        main_application_window()
    else:
        messagebox.showinfo("Login info", "Invalid Credentials")

root = tk.Tk()
root.title("Restaurant Management System")
root.geometry('300x200')
root.configure(bg='#F0F0F0')

style = ttk.Style()
style.theme_use('clam')  # Set theme for modern look

username_label = ttk.Label(root, text="Username")
username_label.pack(pady=5)
username_entry = ttk.Entry(root)
username_entry.pack(pady=5)

password_label = ttk.Label(root, text="Password")
password_label.pack(pady=5)
password_entry = ttk.Entry(root, show='*')
password_entry.pack(pady=5)

submit_button = ttk.Button(root, text="Submit", command=authenticate)
submit_button.pack(pady=10)

root.mainloop()