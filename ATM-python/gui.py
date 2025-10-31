import tkinter as tk
root = tk.Tk()
root.title("ATM Simulator")
root.resizable(False, False)
root.geometry("400x300")

label = tk.Label(root, text='Welcome To The ATM Simulator', font=("Arial", 16, "bold"), fg="white", bg="black")
label.pack(side="top", pady=10)

btn_check = tk.Button(root, text="1. Check Balance", width=25)
btn_check.pack(pady=5)

# Button 2 - Withdraw
btn_withdraw = tk.Button(root, text="2. Withdraw Cash", width=25)
btn_withdraw.pack(pady=5)

# Button 3 - Deposit
btn_deposit = tk.Button(root, text="3. Deposit Cash", width=25)
btn_deposit.pack(pady=5)

# Button 4 - Exit
btn_exit = tk.Button(root, text="4. Exit", width=25, command=root.destroy)
btn_exit.pack(pady=5)

entry = tk.Entry(root, width=10)
entry.pack(pady=5)

submit_btn = tk.Button(root, text="Submit", width=15, command=handle_choice)
submit_btn.pack(pady=10)


root.mainloop()