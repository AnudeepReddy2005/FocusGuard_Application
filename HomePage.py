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

def open_registration():
    try:
        subprocess.Popen(["python", "registration.py"])
    except Exception as e:
        print(f"Error opening registration.py: {e}")

def open_task_page(username):
    try:
        subprocess.Popen(["python", "blocking_taskentering.py", username])
    except Exception as e:
        print(f"Error opening blocking_taskentering.py: {e}")

def open_report_login():
    try:
        subprocess.Popen(["python", "report_login.py"])
    except Exception as e:
        print(f"Error opening report_login.py: {e}")

def login_user():
    login_win = tk.Toplevel()
    login_win.title("Login - FocusGuard")
    login_win.geometry("400x300")
    login_win.configure(bg="#f0f4f7")
    login_win.resizable(False, False)

    tk.Label(login_win, text="🔐 Login to FocusGuard", font=("Helvetica", 16, "bold"),
             bg="#f0f4f7", fg="#2c3e50").pack(pady=15)

    tk.Label(login_win, text="Username:", bg="#f0f4f7", font=("Arial", 12)).pack()
    username_entry = tk.Entry(login_win, width=30)
    username_entry.pack(pady=5)

    tk.Label(login_win, text="Password:", bg="#f0f4f7", font=("Arial", 12)).pack()
    password_entry = tk.Entry(login_win, show="*", width=30)
    password_entry.pack(pady=5)

    def attempt_login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        profiles = load_profiles()

        if username in profiles and profiles[username]['password'] == password:
            messagebox.showinfo("✅ Success", f"Welcome {username}!")
            login_win.destroy()
            open_task_page(username)
        else:
            messagebox.showerror("❌ Error", "Invalid username or password.")

    tk.Button(login_win, text="Login", command=attempt_login, bg="#27ae60", fg="white",
              font=("Arial", 12, "bold"), width=20).pack(pady=15)

def main_menu():
    root = tk.Tk()
    root.title("Welcome to FocusGuard")
    root.configure(bg="#e6f2ff")

    # Make the window full screen
    root.state('zoomed')  # Windows
    root.attributes('-fullscreen', True)  # Cross-platform fullscreen

    # Allow exit fullscreen by pressing Escape
    def exit_fullscreen(event):
        root.attributes('-fullscreen', False)

    root.bind("<Escape>", exit_fullscreen)

    # Header
    header = tk.Frame(root, bg="#2c3e50", height=80)
    header.pack(fill="x")

    tk.Label(header, text="🎯 Welcome to FocusGuard", font=("Helvetica", 24, "bold"),
             fg="white", bg="#2c3e50").pack(pady=20)

    # Body
    body = tk.Frame(root, bg="#e6f2ff")
    body.pack(expand=True)

    tk.Label(body, text="What would you like to do?", font=("Arial", 18),
             bg="#e6f2ff", fg="#34495e").pack(pady=40)

    tk.Button(body, text="🔐 Login", width=25, height=2, bg="#3498db", fg="white",
              font=("Arial", 14, "bold"), command=login_user).pack(pady=15)

    tk.Button(body, text="📝 Register", width=25, height=2, bg="#1abc9c", fg="white",
              font=("Arial", 14, "bold"), command=open_registration).pack(pady=10)

    tk.Button(body, text="📊 View Report", width=25, height=2, bg="#9b59b6", fg="white",
              font=("Arial", 14, "bold"), command=open_report_login).pack(pady=10)

    tk.Label(body, text="🚀 Focus more. Get more done.", bg="#e6f2ff",
             fg="#7f8c8d", font=("Arial", 12, "italic")).pack(pady=40)

    root.mainloop()

if __name__ == "__main__":
    main_menu()
