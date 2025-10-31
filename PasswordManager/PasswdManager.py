import tkinter as tk
from tkinter import messagebox
import json
from pathlib import Path
from cryptography.fernet import Fernet

DATA_FILE = Path("passwords.json")
KEY_FILE = Path("key.key")

# ---------------- KEY MANAGEMENT ----------------
def generate_key():
    """Generate a new Fernet key and save it to a file."""
    key = Fernet.generate_key()
    with KEY_FILE.open("wb") as f:
        f.write(key)
    return key

def load_key():
    """Load an existing key or create a new one if it doesn't exist."""
    if not KEY_FILE.exists():
        return generate_key()
    with KEY_FILE.open("rb") as f:
        return f.read()

# Load the encryption key
fernet = Fernet(load_key())

# ---------------- DATA HANDLING ----------------
def load_data():
    """Load and decrypt JSON data."""
    if not DATA_FILE.exists():
        return {"accounts": []}

    try:
        with DATA_FILE.open("rb") as f:
            encrypted_data = f.read()
        if not encrypted_data:
            return {"accounts": []}

        # Decrypt and parse JSON
        decrypted = fernet.decrypt(encrypted_data).decode("utf-8")
        return json.loads(decrypted)
    except Exception as e:
        messagebox.showerror("Load Error", f"Could not read data:\n{e}")
        return {"accounts": []}

def save_data(data):
    """Encrypt and save JSON data to file."""
    try:
        json_data = json.dumps(data, indent=2, ensure_ascii=False)
        encrypted = fernet.encrypt(json_data.encode("utf-8"))
        with DATA_FILE.open("wb") as f:
            f.write(encrypted)
    except Exception as e:
        messagebox.showerror("Save Error", f"Could not save data:\n{e}")

# ---------------- GUI ----------------
def format_item(item):
    """How each entry appears in the listbox."""
    return f"{item['service']} — {item['username']}"

def main():
    data = load_data()

    root = tk.Tk()
    root.geometry("520x420")
    root.resizable(False, False)
    root.title("Password Manager (Encrypted)")

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

        new_item = {"service": service, "username": user, "password": pwd}
        data.setdefault("accounts", []).append(new_item)
        save_data(data)
        refresh_listbox()

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
        messagebox.showinfo(f"{acc['service']} — {acc['username']}",
                            f"Service: {acc['service']}\nUsername: {acc['username']}\nPassword: {acc['password']}")

    tk.Button(btn_frame, text="Add / Save", command=add_entry_action, width=12).grid(row=0, column=0, padx=6)
    tk.Button(btn_frame, text="View", command=view_selected_action, width=10).grid(row=0, column=1, padx=6)
    tk.Button(btn_frame, text="Delete", command=delete_selected_action, width=10).grid(row=0, column=2, padx=6)

    refresh_listbox()
    root.mainloop()

if __name__ == "__main__":
    main()
