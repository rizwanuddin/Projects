import tkinter as tk
from tkinter import messagebox
import json
from pathlib import Path

DATA_FILE = Path("passwords.json")

def load_data():
    """Load JSON file. Return dict with 'accounts' list."""
    if not DATA_FILE.exists():
        return {"accounts": []}
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        # If file is corrupted/unreadable, start fresh (or handle differently)
        return {"accounts": []}

def save_data(data):
    """Write the data dict to disk pretty-printed."""
    try:
        with DATA_FILE.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except OSError as e:
        messagebox.showerror("Save error", f"Could not save file:\n{e}")

def format_item(item):
    """How each entry appears in the listbox."""
    return f"{item['service']} — {item['username']}"

def main():
    data = load_data()  # data is a dict with key 'accounts'

    root = tk.Tk()
    root.geometry("520x420")
    root.resizable(False, False)
    root.title("Password Manager (JSON demo)")

    # --- Inputs ---
    frm_inputs = tk.Frame(root)
    frm_inputs.pack(pady=10, padx=10, fill="x")

    tk.Label(frm_inputs, text="Service:").grid(row=0, column=0, sticky="w")
    service_entry = tk.Entry(frm_inputs, width=30)
    service_entry.grid(row=0, column=1, padx=6, pady=2)

    tk.Label(frm_inputs, text="Username:").grid(row=1, column=0, sticky="w")
    user_entry = tk.Entry(frm_inputs, width=30)
    user_entry.grid(row=1, column=1, padx=6, pady=2)

    tk.Label(frm_inputs, text="Password:").grid(row=2, column=0, sticky="w")
    passwd_entry = tk.Entry(frm_inputs, width=30, show="*")
    passwd_entry.grid(row=2, column=1, padx=6, pady=2)

    # --- Buttons ---
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=6)

    listbox = tk.Listbox(root, width=60, height=10)
    listbox.pack(padx=10)

    # Helper: refresh listbox contents from `data`
    def refresh_listbox():
        listbox.delete(0, tk.END)
        for item in data.get("accounts", []):
            listbox.insert(tk.END, format_item(item))

    def add_entry_action():
        service = service_entry.get().strip()
        user = user_entry.get().strip()
        pwd = passwd_entry.get().strip()

        if not service or not user or not pwd:
            messagebox.showwarning("Missing fields", "Please fill Service, Username and Password.")
            return

        # Append new account object
        new_item = {"service": service, "username": user, "password": pwd}
        data.setdefault("accounts", []).append(new_item)
        save_data(data)
        refresh_listbox()

        # clear inputs for convenience
        service_entry.delete(0, tk.END)
        user_entry.delete(0, tk.END)
        passwd_entry.delete(0, tk.END)

    def delete_selected_action():
        sel = listbox.curselection()
        if not sel:
            messagebox.showinfo("Select", "Select an entry to delete.")
            return
        index = sel[0]
        acc = data["accounts"][index]
        confirm = messagebox.askyesno("Confirm delete",
                                      f"Delete {acc['service']} — {acc['username']}?")
        if confirm:
            data["accounts"].pop(index)
            save_data(data)
            refresh_listbox()

    def view_selected_action():
        sel = listbox.curselection()
        if not sel:
            messagebox.showinfo("Select", "Select an entry to view.")
            return
        index = sel[0]
        acc = data["accounts"][index]
        # show details in a small dialog (password shown — we will hide/encrypt later)
        messagebox.showinfo(f"{acc['service']} — {acc['username']}",
                            f"Service: {acc['service']}\nUsername: {acc['username']}\nPassword: {acc['password']}")

    add_btn = tk.Button(btn_frame, text="Add / Save", command=add_entry_action, width=12)
    add_btn.grid(row=0, column=0, padx=6)

    view_btn = tk.Button(btn_frame, text="View", command=view_selected_action, width=10)
    view_btn.grid(row=0, column=1, padx=6)

    delete_btn = tk.Button(btn_frame, text="Delete", command=delete_selected_action, width=10)
    delete_btn.grid(row=0, column=2, padx=6)

    # Load initial data into listbox
    refresh_listbox()

    root.mainloop()

if __name__ == "__main__":
    main()
