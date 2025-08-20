import tkinter as tk
from tkinter import messagebox
import json
import os
import subprocess

PROFILE_FILE = "user_profiles.json"

def load_profiles():
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, 'r') as f:
            return json.load(f)
    return {}

def open_report_view(username):
    try:
        subprocess.Popen(["python", "report_view.py", username])
    except Exception as e:
        print(f"Error opening report_view.py: {e}")

def report_login():
    root = tk.Tk()
    root.title("Report Login - FocusGuard")
    root.geometry("400x300")
    root.configure(bg="#f9f9f9")
    root.resizable(False, False)

    tk.Label(root, text="📊 Report Login", font=("Helvetica", 16, "bold"),
             bg="#f9f9f9", fg="#2c3e50").pack(pady=20)

    tk.Label(root, text="Username:", bg="#f9f9f9", font=("Arial", 12)).pack()
    username_entry = tk.Entry(root, width=30)
    username_entry.pack(pady=5)

    tk.Label(root, text="Password:", bg="#f9f9f9", font=("Arial", 12)).pack()
    password_entry = tk.Entry(root, show="*", width=30)
    password_entry.pack(pady=5)

    def attempt_login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        profiles = load_profiles()

        if username in profiles and profiles[username]['password'] == password:
            messagebox.showinfo("✅ Access Granted", f"Welcome {username}!")
            root.destroy()
            open_report_view(username)
        else:
            messagebox.showerror("❌ Access Denied", "Invalid username or password.")

    tk.Button(root, text="Login", command=attempt_login, bg="#2980b9", fg="white",
              font=("Arial", 12, "bold"), width=20).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    report_login()
