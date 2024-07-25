import streamlit as st
import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
import os
from PIL import Image, ImageTk
import random
import string

class BankingApplication:
   
        
        
        
        
        # Hide registration frame initially

        
        # Hide transfer frame initially

    def load_balance(self):
        try:
            with open("BankData.txt", "r") as file:
                for line in file:
                    name, balance = line.strip().split(":")
                    if name == self.current_user:
                        self.balance = float(balance)
                        break
            self.update_balance_label()
        except FileNotFoundError:
            self.balance = 0.0
        except ValueError:
            self.balance = 0.0

    def save_balance(self):
        data = []
        if os.path.exists("BankData.txt"):
            with open("BankData.txt", "r") as file:
                data = file.readlines()
        
        with open("BankData.txt", "w") as file:
            user_found = False
            for line in data:
                name, balance = line.strip().split(":")
                if name == self.current_user:
                    file.write(f"{self.current_user}:{self.balance:.2f}\n")
                    user_found = True
                else:
                    file.write(line)
            if not user_found:
                file.write(f"{self.current_user}:{self.balance:.2f}\n")

    def log_transaction(self, name, transaction):
        with open("transactionLog.txt", "a") as file:
            file.write(f"{name}: {transaction}\n")

    def show_frame(self, frame):
        # Hide all frames before showing the new one
        for widget in self.master.winfo_children():
            widget.pack_forget()
        frame.pack()

    def show_transaction_screen(self):
        self.show_frame(self.transaction_frame)
        self.update_balance_label()

    def show_register_screen(self):
        self.navigation_stack.append(self.login_register_frame)
        self.show_frame(self.register_frame)

    def show_transaction_type_screen(self):
        self.navigation_stack.append(self.transaction_frame)
        self.show_frame(self.transaction_type_frame)

    def show_transfer_screen(self):
        self.navigation_stack.append(self.transaction_frame)
        self.show_frame(self.transfer_frame)

    def go_back(self):
        if self.navigation_stack:
            self.show_frame(self.navigation_stack.pop())

    def update_balance_label(self):
        self.balance_label.config(text="Balance: R{:.2f}".format(self.balance))

    def login(self):
        username = self.name_entry.get()
        password = self.password_entry.get()
        if self.is_user_registered(username, password):
            messagebox.showinfo("Login", "Login successful!")
            self.current_user = username
            self.load_balance()
            self.navigation_stack.append(self.login_register_frame)
            self.show_transaction_screen()
        else:
            messagebox.showerror("Login Error", "Invalid username or password.")

    def is_user_registered(self, name, password):
        try:
            with open("user_data.txt", "r") as file:
                for line in file:
                    stored_name, stored_surname, stored_password, stored_dob = line.strip().split(",")
                    if name == stored_name and password == stored_password:
                        return True
        except FileNotFoundError:
            messagebox.showerror("File Error", "User data file not found")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        return False

    def register(self):
        name = self.reg_name_entry.get()
        surname = self.surname_entry.get()
        password = self.password_entry_reg.get()
        dob_str = self.dob_entry.get()
        cell_number = self.cell_number.get()

        if name and surname and password and dob_str and  cell_number:
            try:
                dob = datetime.strptime(dob_str, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Register Error", "Invalid Date of Birth format. Please use YYYY-MM-DD.")
                return

            today = datetime.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

            if age >= 16:
                with open("user_data.txt", "a") as file:
                    file.write(f"{name},{surname},{password},{dob_str}\n")
                messagebox.showinfo("Register", "Registration successful!")
                self.reg_name_entry.delete(0, tk.END)
                self.surname_entry.delete(0, tk.END)
                self.password_entry_reg.delete(0, tk.END)
                self.dob_entry.delete(0, tk.END)
                self.go_back()
            else:
                messagebox.showerror("Register Error", "You must be at least 16 years old to register.")
        else:
            messagebox.showerror("Register Error", "Please fill in all fields.")

    def choose_transaction_type(self):
        self.transaction_type = self.transaction_type_entry.get().strip().lower()
        if self.transaction_type in ['deposit', 'withdrawal']:
            self.navigation_stack.append(self.transaction_type_frame)
            self.show_frame(self.amount_frame)
        else:
            messagebox.showerror("Input Error", "You provided an invalid input.")

    def perform_transaction(self):
        try:
            amount = float(self.amount_entry.get())
            if self.transaction_type == 'deposit':
                self.balance += amount
                transaction_details = f"Deposit: R{amount:.2f} on {datetime.now()}"
            elif self.transaction_type == 'withdrawal':
                if amount > self.balance:
                    messagebox.showerror("Transaction Error", "Insufficient funds for withdrawal.")
                    return
                self.balance -= amount
                transaction_details = f"Withdrawal: R{amount:.2f} on {datetime.now()}"
            self.log_transaction(self.current_user, transaction_details)
            self.update_balance_label()
            self.save_balance()
            messagebox.showinfo("Transaction Successful", f"Transaction successful! New balance: R{self.balance:.2f}")
        except ValueError:
            messagebox.showerror("Input Error", "You provided an invalid input.")
        self.amount_entry.delete(0, tk.END)
        self.go_back()

    def view_transactions(self):
        try:
            with open("transactionLog.txt", "r") as file:
                transactions = [line.strip() for line in file.readlines() if line.startswith(f"{self.current_user}:")]
                if transactions:
                    transaction_history = "\n".join(transactions)
                    messagebox.showinfo("Transaction Log", transaction_history)
                else:
                    messagebox.showinfo("Transaction Log", "No transactions found.")
        except FileNotFoundError:
            messagebox.showerror("Error", "Transaction log file not found.")

    def download_statement(self):
        try:
            with open("transactionLog.txt", "r") as file:
                transactions = [line.strip() for line in file.readlines() if line.startswith(f"{self.current_user}:")]
                if transactions:
                    transaction_history = "\n".join(transactions)
                    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
                    if file_path:
                        with open(file_path, "w") as statement_file:
                            statement_file.write(transaction_history)
                        messagebox.showinfo("Download Successful", f"Transaction statement saved to {file_path}")
                else:
                    messagebox.showinfo("Transaction Log", "No transactions found.")
        except FileNotFoundError:
            messagebox.showerror("Error", "Transaction log file not found.")

    def logout(self):
        self.current_user = None
        self.balance = 0.0
        self.navigation_stack = []
        self.show_frame(self.login_register_frame)

    def generate_password(self):
        length = 12
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        self.password_entry_reg.delete(0, tk.END)
        self.password_entry_reg.insert(0, password)

    def toggle_password_visibility(self):
        if self.password_visible:
            self.password_entry_reg.config(show="*")
            self.eye_button.config(text="👁️")
        else:
            self.password_entry_reg.config(show="")
            self.eye_button.config(text="🙈")
        self.password_visible = not self.password_visible

    def perform_transfer(self):
        recipient = self.recipient_entry.get()
        selected_bank = self.bank_var.get()
        try:
            amount = float(self.transfer_amount_entry.get())
            if amount <= self.balance:
                self.balance -= amount
                transaction_details = f"Transfer: R{amount:.2f} to {recipient} at {selected_bank} on {datetime.now()}"
                self.log_transaction(self.current_user, transaction_details)
                self.update_balance_label()
                self.save_balance()
                messagebox.showinfo("Transfer Successful", f"Transfer successful! New balance: R{self.balance:.2f}")
                self.recipient_entry.delete(0, tk.END)
                self.transfer_amount_entry.delete(0, tk.END)
                self.go_back()
            else:
                messagebox.showerror("Transfer Error", "Insufficient funds for transfer.")
        except ValueError:
            messagebox.showerror("Input Error", "You provided an invalid input.")

if __name__ == "__main__":
                    
    app = BankingApplication()
   
