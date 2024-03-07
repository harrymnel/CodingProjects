import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime, timedelta

# Create SQLite database
conn = sqlite3.connect('food_database.db')
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS food_items
             (id INTEGER PRIMARY KEY, name TEXT, expiry_date DATE)''')
conn.commit()

# Function to add new food item
def add_item():
    name = name_entry.get()
    expiry_date = expiry_entry.get()

    if name == '' or expiry_date == '':
        messagebox.showerror("Error", "Please enter both food name and expiry date")
        return

    try:
        expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d").date()
    except ValueError:
        messagebox.showerror("Error", "Please enter expiry date in YYYY-MM-DD format")
        return

    c.execute("INSERT INTO food_items (name, expiry_date) VALUES (?, ?)", (name, expiry_date))
    conn.commit()
    messagebox.showinfo("Success", "Food item added successfully")
    name_entry.delete(0, tk.END)
    expiry_entry.delete(0, tk.END)

# Function to display all food items
def display_items():
    c.execute("SELECT id, name, expiry_date FROM food_items")
    items = c.fetchall()
    if not items:
        messagebox.showinfo("Information", "No food items found")
        return
    else:
        display_text = "Food Items:\n"
        for item in items:
            display_text += f"{item[0]}. {item[1]} - Expires on {item[2]}\n"
        messagebox.showinfo("Food Items", display_text)

# Function to check for items about to expire
def check_expiry():
    today = datetime.now().date()
    expiry_threshold = today + timedelta(days=3)
    c.execute("SELECT name FROM food_items WHERE expiry_date <= ?", (expiry_threshold,))
    expiring_items = c.fetchall()
    if expiring_items:
        expiring_text = "Food items about to expire:\n"
        for item in expiring_items:
            expiring_text += f"{item[0]}\n"
        messagebox.showwarning("Expiring Items", expiring_text)
    else:
        messagebox.showinfo("Information", "No items are about to expire")

# Function to delete selected item
def delete_item():
    selected_id = int(selected_id_entry.get())

    c.execute("SELECT name FROM food_items WHERE id=?", (selected_id,))
    item = c.fetchone()
    if not item:
        messagebox.showerror("Error", "Item not found")
        return

    c.execute("DELETE FROM food_items WHERE id=?", (selected_id,))
    conn.commit()
    messagebox.showinfo("Success", f"Item '{item[0]}' deleted successfully")
    selected_id_entry.delete(0, tk.END)

# GUI setup
root = tk.Tk()
root.title("Food Expiry Tracker")
    
# Labels and Entry for adding new item
tk.Label(root, text="Food Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Expiry Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
expiry_entry = tk.Entry(root)
expiry_entry.grid(row=1, column=1, padx=5, pady=5)

add_button = tk.Button(root, text="Add Item", command=add_item)
add_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="we")

# Separator for better visual separation
separator = tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN)
separator.grid(row=3, column=0, columnspan=2, sticky="we", padx=5, pady=5)

# Buttons for displaying items and checking expiry
display_button = tk.Button(root, text="Display Items", command=display_items)
display_button.grid(row=4, column=0, padx=5, pady=5, sticky="we")

check_expiry_button = tk.Button(root, text="Check Expiry", command=check_expiry)
check_expiry_button.grid(row=4, column=1, padx=5, pady=5, sticky="we")

# Separator for better visual separation
separator2 = tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN)
separator2.grid(row=5, column=0, columnspan=2, sticky="we", padx=5, pady=5)

# Labels and Entry for selecting item to delete
tk.Label(root, text="Select Item ID to Delete:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
selected_id_entry = tk.Entry(root)
selected_id_entry.grid(row=6, column=1, padx=5, pady=5)

delete_button = tk.Button(root, text="Delete Item", command=delete_item)
delete_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="we")

# Adjusting column weights for better resizing
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

root.mainloop()
