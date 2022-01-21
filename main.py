import tkinter
from tkinter import *
import pandas as pd
import csv
from tkinter import messagebox
import random
import pyperclip
import json

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    password_list += [random.choice(numbers) for x in range(nr_numbers)]
    password_list += [random.choice(letters) for x in range(nr_letters)]
    password_list += [random.choice(symbols) for x in range(nr_symbols)]
    random.shuffle(password_list)

    password = "".join(password_list)

    pass_entry.insert(0, password)
    pyperclip.copy(password)
    messagebox.showinfo(message="password saved to clipboard")

# ---------------------------- SAVE PASSWORD -------------------------------


def save_pass():
    website = website_entry.get()
    user_name = eu_entry.get()
    password = pass_entry.get()
    user_data = {website: {
        "username": user_name,
        "password": password
    }}

    if len(password) == 0 or len(user_name) == 0 or len(website) == 0:
        inout_error = messagebox.showerror(title="Input Error", message="All fields must be filled.")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"Please confirm the information you entered: \n Email: "
                                                              f"{user_name}\n Password: {password}")
        if is_ok:
            try:
                with open("data.json", 'r') as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", 'w') as data_file:
                    json.dump(user_data, data_file, indent=4)
            else:
                data.update(user_data)
                with open("data.json", 'w') as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                eu_entry.delete(0, END)
                pass_entry.delete(0, END)
                messagebox.showinfo(message="your data saved successfully")


# ----------------------------- Search ---------------------------------- #
def search():
    website = website_entry.get()
    try:
        with open("data.json", 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="File does not exist")
        website_entry.delete(0, END)
        eu_entry.delete(0, END)
        pass_entry.delete(0, END)
    else:
        if website in data:
            messagebox.showinfo(title=website, message=f"Username: {data[website]['username']} \nPassword: {data[website]['password']} \nYour password saved to clipboard.")
            pyperclip.copy(data[website]['password'])
        else:
            messagebox.showerror(title="Input Error", message=f"{website} does not exist in database.")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
canvas.grid(column=1, row=0)
lock_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_image)

website_label = Label(text="Website: ", font=("Courier", 12, "normal"), fg="blue")
website_label.grid(column=0, row=1)

eu_label = Label(text="Email/Username: ", font=("Courier", 12, "normal"), fg="blue")
eu_label.grid(column=0, row=2)

password_label = Label(text="Password: ", font=("Courier", 12, "normal"), fg="blue")
password_label.grid(column=0, row=3)

website_entry = Entry(width=21)
website_entry.focus()
website_entry.grid(column=1, row=1, columnspan=2, sticky="ew")

eu_entry = Entry(width=35)
eu_entry.grid(column=1, row=2, columnspan=2, sticky="ew")

pass_entry = Entry(width=21)
pass_entry.grid(column=1, row=3, sticky="ew")

gen_button = Button(text="Generate Password", font=("Courier", 8, "normal"), fg="blue", bg="gray", command=generate_password)
gen_button.grid(column=2, row=3, sticky="ew")

add_button = Button(text="Add", width=35, font=("Courier", 8, "normal"), fg="blue", bg="gray", command=save_pass)
add_button.grid(column=1, row=4, columnspan=2, sticky="ew")

search_button = Button(text="Search",font=("Courier", 8, "normal"), fg="blue", bg="gray", command=search)
search_button.grid(column=2, row=1, sticky="ew")

window.mainloop()
