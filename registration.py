import tkinter as tk
from tkinter import messagebox
import json
import os

PROFILE_FILE = "user_profiles.json"

def load_profiles():
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_profile(profile):
    profiles = load_profiles()
    username = profile['name']
    profiles[username] = profile
    with open(PROFILE_FILE, 'w') as f:
        json.dump(profiles, f, indent=4)

def create_dynamic_field(parent, label_text):
    label = tk.Label(parent, text=label_text, font=('Arial', 11, 'bold'), bg="#ecf0f1")
    label.pack(pady=(10, 0))
    entry_list = []
    container = tk.Frame(parent, bg="#ecf0f1")
    container.pack()

    def add_entry():
        entry = tk.Entry(container, width=50)
        entry.pack(pady=3)
        entry_list.append(entry)
    
    add_entry()  # Default first entry
    tk.Button(parent, text=f"Add More {label_text}", command=add_entry,
              bg="#3498db", fg="white", font=('Arial', 10)).pack(pady=5)
    
    return entry_list

def registration_form():
    root = tk.Tk()
    root.title("FocusGuard - Registration")
    
    # Set a larger window size
    window_width = 600
    window_height = 800
    root.geometry(f"{window_width}x{window_height}")
    root.configure(bg="#ecf0f1")

    # Center the window using absolute positioning
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Create a canvas and add a scrollbar
    canvas = tk.Canvas(root, bg="#ecf0f1")
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    scrollable_frame = tk.Frame(canvas, bg="#ecf0f1")
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Header
    tk.Label(scrollable_frame, text="📝 FocusGuard Registration Form",
             font=('Helvetica', 18, 'bold'), bg="#ecf0f1", fg="#2c3e50").pack(pady=20)

    # Input fields (Centered in the window)
    def create_labeled_entry(label_text):
        input_frame = tk.Frame(scrollable_frame, bg="#ecf0f1")
        input_frame.pack(pady=10, anchor="center")
        tk.Label(input_frame, text=label_text, bg="#ecf0f1", font=('Arial', 12)).pack()
        entry = tk.Entry(input_frame, width=50)
        entry.pack(pady=5)
        return entry

    name_entry = create_labeled_entry("Your Name:")
    password_entry = create_labeled_entry("Password:")
    password_entry.config(show="*")
    father_entry = create_labeled_entry("Father's Name:")
    mother_entry = create_labeled_entry("Mother's Name:")

    # Dynamic fields
    goals_entries = create_dynamic_field(scrollable_frame, "Life Goals")
    problems_entries = create_dynamic_field(scrollable_frame, "Family Problems")
    insults_entries = create_dynamic_field(scrollable_frame, "Past Insults")
    quotes_entries = create_dynamic_field(scrollable_frame, "Motivational Quotes from Parents")

    def submit():
        name = name_entry.get().strip()
        password = password_entry.get().strip()
        father = father_entry.get().strip()
        mother = mother_entry.get().strip()

        if not all([name, password, father, mother]):
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        def extract(entries): return [e.get().strip() for e in entries if e.get().strip()]

        profile = {
            "name": name,
            "password": password,
            "father_name": father,
            "mother_name": mother,
            "life_goals": extract(goals_entries),
            "family_problems": extract(problems_entries),
            "past_insults": extract(insults_entries),
            "parent_quotes": extract(quotes_entries)
        }

        save_profile(profile)
        messagebox.showinfo("✅ Success", "Your profile has been saved successfully!")
        root.destroy()

    # Submit button (Centered)
    submit_frame = tk.Frame(scrollable_frame, bg="#ecf0f1")
    submit_frame.pack(pady=30)
    tk.Button(submit_frame, text="Submit", command=submit,
              bg="#27ae60", fg="white", font=('Arial', 12, 'bold'), width=20).pack()

    root.mainloop()

if __name__ == "__main__":
    registration_form()
