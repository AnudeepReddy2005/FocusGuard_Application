import tkinter as tk
from tkinter import messagebox
import time
import threading
import psutil
import os
import json

PROFILE_FILE = "user_profiles.json"
BLOCKED_APPS_LOG = "blocked_apps_log.json"
SESSION_LOG_FILE = "session_attempts_log.json"
stop_blocking = threading.Event()

# Load/save helpers
def load_profiles():
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, 'r') as f:
            return json.load(f)
    return {}

def load_blocked_apps_log():
    if os.path.exists(BLOCKED_APPS_LOG):
        with open(BLOCKED_APPS_LOG, 'r') as f:
            return json.load(f)
    return {}

def save_blocked_apps_log(log):
    with open(BLOCKED_APPS_LOG, 'w') as f:
        json.dump(log, f, indent=4)

def load_session_attempts():
    if os.path.exists(SESSION_LOG_FILE):
        with open(SESSION_LOG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_session_attempts(log):
    with open(SESSION_LOG_FILE, 'w') as f:
        json.dump(log, f, indent=4)

def save_profile(profile):
    profiles = load_profiles()
    username = profile['name']
    profiles[username] = profile
    with open(PROFILE_FILE, 'w') as f:
        json.dump(profiles, f, indent=4)

# Blocking logic with session tracking
def block_apps(apps, root, username, session_log):
    profiles = load_profiles()
    profile = profiles.get(username, {})
    blocked_apps_log = load_blocked_apps_log()

    def show_custom_popup(app_name):
        popup = tk.Toplevel(root)
        popup.title("Blocked App Warning")
        popup.geometry("420x400")
        popup.configure(bg="#2c3e50")
        popup.resizable(False, False)
        popup.grab_set()

        # Centering
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        position_top = int(screen_height / 2 - 400 / 2)
        position_right = int(screen_width / 2 - 420 / 2)
        popup.geometry(f'420x400+{position_right}+{position_top}')

        tk.Label(popup, text=f"Hey {username}!", font=("Helvetica", 16, "bold"), fg="#e74c3c", bg="#2c3e50").pack(pady=(15, 5))
        tk.Label(popup, text=f"Do you wanna open '{app_name}'?\nDid you forget your dreams and goals?",
                 font=("Arial", 12), fg="#ecf0f1", bg="#2c3e50", wraplength=380, justify="center").pack(pady=10)

        def list_info(title, items):
            if items:
                tk.Label(popup, text=title, font=("Arial", 12, "bold"), fg="#1abc9c", bg="#2c3e50").pack(pady=(10, 0))
                for item in items:
                    tk.Label(popup, text=f"• {item}", font=("Arial", 11), fg="#bdc3c7", bg="#2c3e50",
                             wraplength=380, justify="left", anchor="w").pack(anchor="w", padx=20)

        list_info("Your Life Goals:", profile.get('life_goals', []))
        list_info("Family Problems:", profile.get('family_problems', []))
        list_info("Past Insults:", profile.get('past_insults', []))

        tk.Button(popup, text="Stay Focused", command=popup.destroy,
                  bg="#e74c3c", fg="white", font=("Arial", 12, 'bold')).pack(pady=20)

    while not stop_blocking.is_set():
        running = [p.name() for p in psutil.process_iter()]
        for app in apps:
            if app in running:
                try:
                    for proc in psutil.process_iter():
                        if proc.name() == app:
                            proc.terminate()
                            print(f"Blocked {app}")

                            # Update global log
                            blocked_apps_log[app] = blocked_apps_log.get(app, 0) + 1
                            save_blocked_apps_log(blocked_apps_log)

                            # Update session log
                            session_log[app] = session_log.get(app, 0) + 1

                            root.after(0, lambda app_name=app: show_custom_popup(app_name))
                except Exception as e:
                    print(f"Error blocking {app}: {e}")
        time.sleep(5)

# Task input form
def task_input_form(username):
    root = tk.Tk()
    root.title(f"{username}'s Task Planner")
    root.geometry("600x600")
    root.resizable(False, False)
    root.configure(bg="#34495e")

    tk.Label(root, text=f"Welcome, {username}!", font=("Helvetica", 16, 'bold'), fg="#fff", bg="#34495e").pack(pady=20)

    task_frame = tk.Frame(root, bg="#34495e")
    task_frame.pack(pady=10)
    task_entries = []

    def add_task():
        row = tk.Frame(task_frame, bg="#34495e")
        name = tk.Entry(row, width=30, font=("Arial", 12))
        minutes = tk.Entry(row, width=10, font=("Arial", 12))
        name.pack(side="left", padx=5)
        minutes.pack(side="left", padx=5)
        row.pack(pady=5)
        task_entries.append((name, minutes))

    add_task()
    tk.Button(root, text="Add Task", command=add_task, bg="#e74c3c", fg="white", font=("Arial", 12, 'bold')).pack(pady=10)

    app_frame = tk.Frame(root, bg="#34495e")
    app_frame.pack(pady=20)
    app_entries = []

    def add_app():
        entry = tk.Entry(app_frame, width=30, font=("Arial", 12))
        entry.pack(pady=5)
        app_entries.append(entry)

    tk.Label(root, text="Apps to block (e.g. chrome.exe)", font=("Arial", 12), fg="#fff", bg="#34495e").pack()
    add_app()
    tk.Button(root, text="Add App", command=add_app, bg="#e74c3c", fg="white", font=("Arial", 12, 'bold')).pack(pady=10)

    def submit():
        tasks = []
        for name, mins in task_entries:
            if name.get() and mins.get().isdigit():
                tasks.append({"task": name.get(), "time_minutes": int(mins.get())})

        apps = [e.get() for e in app_entries if e.get()]
        if not tasks:
            messagebox.showerror("Error", "Enter at least one valid task.")
            return

        root.destroy()
        task_timer_form(username, tasks, apps)

    tk.Button(root, text="Submit", command=submit, bg="#27ae60", fg="white", font=("Arial", 14, 'bold')).pack(pady=30)
    root.mainloop()

# Focus timer with logging
def task_timer_form(username, tasks, apps):
    total_seconds = sum(t['time_minutes'] for t in tasks) * 60
    session_log = {}

    root = tk.Tk()
    root.title("Focus Timer")
    root.geometry("400x400")
    root.resizable(False, False)
    root.configure(bg="#34495e")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - 400 / 2)
    position_right = int(screen_width / 2 - 400 / 2)
    root.geometry(f'400x400+{position_right}+{position_top}')

    tk.Label(root, text="Focus Mode", font=("Helvetica", 18, 'bold'), fg="#fff", bg="#34495e").pack(pady=20)
    timer_label = tk.Label(root, font=("Helvetica", 24), fg="#e74c3c", bg="#34495e")
    timer_label.pack(pady=10)

    task_frame = tk.Frame(root, bg="#34495e")
    task_frame.pack(pady=10)
    task_vars = []
    tk.Label(task_frame, text="Your Tasks:", font=("Arial", 12, "bold"), fg="#fff", bg="#34495e").pack()

    for t in tasks:
        var = tk.BooleanVar()
        cb = tk.Checkbutton(task_frame, text=t['task'], variable=var, font=("Arial", 12), fg="#fff", bg="#34495e", selectcolor="#e74c3c")
        cb.pack(anchor='w')
        task_vars.append(var)

    stop_blocking.clear()
    t = threading.Thread(target=block_apps, args=(apps, root, username, session_log), daemon=True)
    t.start()

    def end_session():
        attempts_data = load_session_attempts()
        attempts_data[username] = attempts_data.get(username, [])
        attempts_data[username].append(session_log)
        save_session_attempts(attempts_data)

    def update_timer():
        nonlocal total_seconds
        while total_seconds > 0 and not stop_blocking.is_set():
            m, s = divmod(total_seconds, 60)
            timer_label.config(text=f"{m:02}:{s:02}")
            time.sleep(1)
            total_seconds -= 1
        timer_label.config(text="Time's up!")
        messagebox.showinfo("Done", "Focus session ended.")
        stop_blocking.set()
        end_session()
        root.quit()

    def complete():
        done = sum(var.get() for var in task_vars)
        messagebox.showinfo("Summary", f"Completed {done} of {len(tasks)} tasks.")
        stop_blocking.set()
        end_session()
        root.quit()

    def unblock_apps():
        profiles = load_profiles()
        profile = profiles.get(username, {})
        msg = f"{profile['name']}\nGoals: {', '.join(profile.get('life_goals', []))}\nDo you want to unblock all apps?"
        if messagebox.askokcancel("Unblock Apps", msg):
            stop_blocking.set()
            end_session()
            root.quit()

    tk.Button(root, text="Mark Completed", command=complete, bg="#27ae60", fg="white", font=("Arial", 14, 'bold')).pack(pady=20)
    tk.Button(root, text="Unblock Apps", command=unblock_apps, bg="#e74c3c", fg="white", font=("Arial", 14, 'bold')).pack(pady=10)

    threading.Thread(target=update_timer, daemon=True).start()
    root.mainloop()

# Entry point
def registration_form():
    print("⚠ Registration form logic should be added here.")
    # Placeholder - implement your own form logic if needed

if __name__ == "__main__":
    if not os.path.exists(PROFILE_FILE):
        registration_form()
    else:
        profiles = load_profiles()
        if profiles:
            username = list(profiles.keys())[0]
            task_input_form(username)
        else:
            registration_form()
