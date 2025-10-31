import tkinter as tk
from tkinter import messagebox

# === ATM Logic Functions ===
def show_balance():
    messagebox.showinfo("Balance", f"Your balance is ${balance[0]:.2f}")

def deposit():
    try:
        amount = float(entry.get())
        if amount < 0:
            messagebox.showerror("Error", "That's not a valid amount.")
        else:
            balance[0] += amount
            messagebox.showinfo("Success", f"Deposited ${amount:.2f}")
        entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Enter a valid number.")

def withdraw():
    try:
        amount = float(entry.get())
        if amount > balance[0]:
            messagebox.showerror("Error", "Insufficient funds.")
        elif amount < 0:
            messagebox.showerror("Error", "That's not a valid amount.")
        else:
            balance[0] -= amount
            messagebox.showinfo("Success", f"Withdrew ${amount:.2f}")
        entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Enter a valid number.")

def exit_app():
    messagebox.showinfo("Goodbye!", "Thank you! Have a nice day!")
    root.destroy()

# === GUI Setup ===
root = tk.Tk()
root.title("ATM Simulator")
root.resizable(False, False)
root.geometry("400x350")
root.configure(bg="black")

balance = [0]  # Use list for mutability inside nested functions

label = tk.Label(root, text='Welcome To The ATM Simulator',
                 font=("Arial", 16, "bold"), fg="white", bg="black")
label.pack(side="top", pady=15)

entry_label = tk.Label(root, text="Enter Amount (for Deposit/Withdraw):",
                       font=("Arial", 10), fg="white", bg="black")
entry_label.pack(pady=5)

entry = tk.Entry(root, width=15, font=("Arial", 12))
entry.pack(pady=5)

btn_check = tk.Button(root, text="1. Check Balance", width=25, command=show_balance)
btn_check.pack(pady=5)

btn_withdraw = tk.Button(root, text="2. Withdraw Cash", width=25, command=withdraw)
btn_withdraw.pack(pady=5)

btn_deposit = tk.Button(root, text="3. Deposit Cash", width=25, command=deposit)
btn_deposit.pack(pady=5)

btn_exit = tk.Button(root, text="4. Exit", width=25, command=exit_app)
btn_exit.pack(pady=5)

root.mainloop()
