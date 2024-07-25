import stream as streamlit
import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
import os
from PIL import Image, ImageTk
import random
import string

class BankingApplication:
    def __init__(self, master):
        self.master = master
        self.master.title("PocketGuard")
        self.master.geometry("700x600")
        
        self.current_user = None
        self.navigation_stack = []

        # Initialize balance
        self.balance = 0.0

        # Initialize login/register frame
        self.login_register_frame = tk.Frame(self.master, bg="white")
        self.login_register_frame.pack(fill=tk.BOTH, expand=True)
        
        # Load and place the logo
        self.logo_image = Image.open("Images/Pocketg1.jpg")
        self.logo_image = self.logo_image.resize((500, 500))
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(self.login_register_frame, image=self.logo_photo, bg="#30949D")
        self.logo_label.grid(row=0, column=6, columnspan=2, padx=10, pady=10, sticky='w')

        input_row = 1

        self.name_label = tk.Label(self.login_register_frame, text="Username:", font=("Helvetica", 12), bg="white", fg='black')
        self.name_label.grid(row=input_row, column=4, padx=10, pady=5, sticky='e')

        self.name_entry = tk.Entry(self.login_register_frame, font=("Helvetica", 12), highlightbackground="black", highlightthickness=2)
        self.name_entry.grid(row=input_row, column=6, padx=10, pady=5, sticky='w')

        input_row += 1

        self.password_label = tk.Label(self.login_register_frame, text="Password:", font=("Helvetica", 12), bg="white", fg='black')
        self.password_label.grid(row=input_row, column=4, padx=10, pady=5, sticky='e')

        self.password_entry = tk.Entry(self.login_register_frame, show="*", font=("Helvetica", 12), highlightbackground="black", highlightthickness=2)
        self.password_entry.grid(row=input_row, column=6, padx=10, pady=5, sticky='w')

        input_row += 1

        self.login_button = tk.Button(self.login_register_frame, text="Login", command=self.login, font=("Helvetica", 12))
        self.login_button.grid(row=input_row, column=6, columnspan=2, padx=10, pady=5)

        input_row += 1

        self.register_button = tk.Button(self.login_register_frame, text="Register", command=self.show_register_screen, font=("Helvetica", 12))
        self.register_button.grid(row=input_row, column=6, columnspan=2, padx=10, pady=5)
        
        # Initialize registration frame
        self.register_frame = tk.Frame(self.master, bg="white", highlightbackground="black", highlightthickness=2)

        self.register_bg_image = Image.open("Images/PG.jpg")
        self.register_bg_image = self.register_bg_image.resize((700, 600))
        self.register_bg_photo = ImageTk.PhotoImage(self.register_bg_image)
        self.register_bg_label = tk.Label(self.register_frame, image=self.register_bg_photo)
        self.register_bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.username_label = tk.Label(self.register_frame, text="Name:", font=("Helvetica", 12), bg="white")
        self.username_label.grid(row=0, column=0, padx=10, pady=5)

        self.reg_name_entry = tk.Entry(self.register_frame, font=("Helvetica", 12), bg="white", highlightbackground="black", highlightthickness=2)
        self.reg_name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.surname_label = tk.Label(self.register_frame, text="Surname:", font=("Helvetica", 12), bg="white")
        self.surname_label.grid(row=1, column=0, padx=10, pady=5)

        self.surname_entry = tk.Entry(self.register_frame, font=("Helvetica", 12), bg="white", highlightbackground="black", highlightthickness=2)
        self.surname_entry.grid(row=1, column=1, padx=10, pady=5)
        
        self.cell_number_label = tk.Label(self.register_frame, text = "Number:", font=("Helvetica", 12), bg="white")
        self.cell_number_label.grid(row=2, column=0, padx=10, pady=5)
        
        self.cell_number_label_entry = tk.Entry(self.register_frame, font=("Helvetica", 12), bg="white", highlightbackground="black", highlightthickness=2)
        self.cell_number_label_entry.grid(row=2, column=1, padx=10, pady=5)
                
        self.password_label_reg = tk.Label(self.register_frame, text="Password:", font=("Helvetica", 12), bg="white")
        self.password_label_reg.grid(row=3, column=0, padx=10, pady=5)

        self.password_entry_reg = tk.Entry(self.register_frame, show="*", font=("Helvetica", 12), highlightbackground="black", highlightthickness=2)
        self.password_entry_reg.grid(row=3, column=1, padx=10, pady=5)

        self.dob_label = tk.Label(self.register_frame, text="Date of Birth (YYYY-MM-DD):", font=("Helvetica", 12), bg="white")
        self.dob_label.grid(row=4, column=0, padx=10, pady=5)

        self.dob_entry = tk.Entry(self.register_frame, font=("Helvetica", 12), bg="white", highlightbackground="black", highlightthickness=2)
        self.dob_entry.grid(row=4, column=1, padx=10, pady=5)
        

        self.register_submit_button = tk.Button(self.register_frame, text="Register", command=self.register, font=("Helvetica", 12))
        self.register_submit_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5)
        
        # Password generator button
        self.generate_password_button = tk.Button(self.register_frame, text="Generate Password", command=self.generate_password, font=("Helvetica", 12))
        self.generate_password_button.grid(row=6, column=0, columnspan=2, padx=10, pady=5)
         
        # Back button for registration frame
        self.register_back_button = tk.Button(self.register_frame, text="Back", command=self.go_back, font=("Helvetica", 12))
        self.register_back_button.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

        self.eye_button = tk.Button(self.register_frame, text="👁️", command=self.toggle_password_visibility, bd=0, font=("Segoe UI Emoji", 10))
        self.eye_button.grid(row=3, column=2, padx=10, pady=5, sticky="w")

        self.password_visible = False
        
        # Hide registration frame initially
        self.register_frame.pack_forget()

        # Initialize transaction frame
        self.transaction_frame = tk.Frame(self.master, bg="white")

        self.balance_label = tk.Label(self.transaction_frame, text="Balance: R0.00", font=("Helvetica", 12), bg="white")
        self.balance_label.pack(padx=10, pady=5)

        self.view_transactions_button = tk.Button(self.transaction_frame, text="View Transactions", command=self.view_transactions, font=("Helvetica", 12))
        self.view_transactions_button.pack(padx=10, pady=5)

        self.download_statement_button = tk.Button(self.transaction_frame, text="Download Statement", command=self.download_statement, font=("Helvetica", 12))
        self.download_statement_button.pack(padx=10, pady=5)

        self.transaction_prompt_button = tk.Button(self.transaction_frame, text="Make a Transaction", command=self.show_transaction_type_screen, font=("Helvetica", 12))
        self.transaction_prompt_button.pack(padx=10, pady=5)
        
        self.transfer_prompt_button = tk.Button(self.transaction_frame, text="Transfer Money", command=self.show_transfer_screen, font=("Helvetica", 12))
        self.transfer_prompt_button.pack(padx=10, pady=5)

        self.logout_button = tk.Button(self.transaction_frame, text="Logout", command=self.logout, font=("Helvetica", 12))
        self.logout_button.pack(padx=10, pady=5)
        
        # Hide transaction frame initially
        self.transaction_frame.pack_forget()

        # Initialize transaction type frame
        self.transaction_type_frame = tk.Frame(self.master, bg="white")

        self.transaction_type_label = tk.Label(self.transaction_type_frame, text="Would you like to make a deposit or withdrawal? (Deposit/Withdrawal)", font=("Helvetica", 12), bg="white")
        self.transaction_type_label.pack()

        self.transaction_type_entry = tk.Entry(self.transaction_type_frame, font=("Helvetica", 12), highlightbackground="black", highlightthickness=2)
        self.transaction_type_entry.pack()

        self.transaction_type_button = tk.Button(self.transaction_type_frame, text="Submit", command=self.choose_transaction_type, font=("Helvetica", 12))
        self.transaction_type_button.pack(padx=10, pady=5)

        # Back button for transaction type frame
        self.transaction_type_back_button = tk.Button(self.transaction_type_frame, text="Back", command=self.go_back, font=("Helvetica", 12))
        self.transaction_type_back_button.pack(padx=10, pady=5)
        
        # Hide transaction type frame initially
        self.transaction_type_frame.pack_forget()

        # Initialize amount frame
        self.amount_frame = tk.Frame(self.master, bg="white")

        self.amount_label = tk.Label(self.amount_frame, text="Enter amount:", font=("Helvetica", 12), bg="white")
        self.amount_label.pack()

        self.amount_entry = tk.Entry(self.amount_frame, font=("Helvetica", 12), highlightbackground="black", highlightthickness=2)
        self.amount_entry.pack()

        self.amount_submit_button = tk.Button(self.amount_frame, text="Submit", command=self.perform_transaction, font=("Helvetica", 12))
        self.amount_submit_button.pack(padx=10, pady=5)

        # Back button for amount frame
        self.amount_back_button = tk.Button(self.amount_frame, text="Back", command=self.go_back, font=("Helvetica", 12))
        self.amount_back_button.pack(padx=10, pady=5)
        
        # Hide amount frame initially
        self.amount_frame.pack_forget()

        # Initialize transfer frame
        self.transfer_frame = tk.Frame(self.master, bg="white")

        self.transfer_label = tk.Label(self.transfer_frame, text="Transfer Money", font=("Helvetica", 14), bg="white")
        self.transfer_label.pack(padx=10, pady=5)

        self.recipient_label = tk.Label(self.transfer_frame, text="Recipient's Cell Number or Bank Account:", font=("Helvetica", 12), bg="white")
        self.recipient_label.pack(padx=10, pady=5)

        self.recipient_entry = tk.Entry(self.transfer_frame, font=("Helvetica", 12), highlightbackground="black", highlightthickness=2)
        self.recipient_entry.pack(padx=10, pady=5)

        self.bank_label = tk.Label(self.transfer_frame, text="Select Bank:", font=("Helvetica", 12), bg="white")
        self.bank_label.pack(padx=10, pady=5)

        self.bank_var = tk.StringVar()
        self.bank_options = ["Absa", "Capitec", "FNB", "Nedbank", "STD Bank"]
        self.bank_menu = tk.OptionMenu(self.transfer_frame, self.bank_var, *self.bank_options)
        self.bank_menu.config(font=("Helvetica", 12), bg="white", highlightbackground="black", highlightthickness=2)
        self.bank_menu.pack(padx=10, pady=5)

        self.transfer_amount_label = tk.Label(self.transfer_frame, text="Enter Amount to Transfer:", font=("Helvetica", 12), bg="white")
        self.transfer_amount_label.pack(padx=10, pady=5)

        self.transfer_amount_entry = tk.Entry(self.transfer_frame, font=("Helvetica", 12), highlightbackground="black", highlightthickness=2)
        self.transfer_amount_entry.pack(padx=10, pady=5)

        self.transfer_submit_button = tk.Button(self.transfer_frame, text="Transfer", command=self.perform_transfer, font=("Helvetica", 12))
        self.transfer_submit_button.pack(padx=10, pady=5)

        self.transfer_back_button = tk.Button(self.transfer_frame, text="Back", command=self.go_back, font=("Helvetica", 12))
        self.transfer_back_button.pack(padx=10, pady=5)
        
        # Hide transfer frame initially
        self.transfer_frame.pack_forget()

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
    root = tk.Tk()
    app = BankingApplication(root)
    root.mainloop()
