import tkinter as tk
import json
import os
import sys
import requests

LOG_FILE = "session_attempts_log.json"
GEMINI_API_KEY = "AIzaSyAsQ4zfwj2ncjtKy1nBTHF2JLFahU-Abiw"  # Replace with your actual Gemini API key
MODEL = "gemini-1.5-flash-001"  # ✅ Use a supported model name

def load_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            return json.load(f)
    return {}

def analyze_productivity(app_open_count):
    prompt = f"While working, I opened distracting apps {app_open_count} times. How is my productivity and what can I improve?"

    url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.ok:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"⚠ Error from Gemini: {response.status_code} - {response.text}"
    except Exception as e:
        return f"⚠ Exception occurred: {str(e)}"

def show_user_logs(username):
    logs = load_logs()
    user_logs = logs.get(username, [])

    root = tk.Tk()
    root.title(f"{username}'s Report - FocusGuard")
    root.geometry("700x500")
    root.configure(bg="#ffffff")

    tk.Label(root, text=f"📋 Session Report for {username}", font=("Helvetica", 16, "bold"),
             bg="#ffffff", fg="#2c3e50").pack(pady=20)

    total_opens = 0
    sessions_display = []

    for i, session in enumerate(user_logs, start=1):
        if session:
            for process, minutes in session.items():
                total_opens += minutes
                sessions_display.append(f"Session {i}: {process} opened {minutes} times")

    if not sessions_display:
        tk.Label(root, text="No valid session records found.", font=("Arial", 12),
                 bg="#ffffff", fg="gray").pack(pady=10)
    else:
        text_frame = tk.Frame(root, bg="white")
        text_frame.pack(expand=True, fill='both', padx=20, pady=10)

        text_box = tk.Text(text_frame, wrap="word", font=("Arial", 11), bg="#f4f4f4")
        text_box.pack(expand=True, fill="both")

        for line in sessions_display:
            text_box.insert(tk.END, line + "\n\n")

        text_box.insert(tk.END, "\nAnalyzing your productivity with Google Gemini...\n\n")
        feedback = analyze_productivity(total_opens)
        text_box.insert(tk.END, "📢 Gemini's Suggestions:\n" + feedback)

        text_box.config(state="disabled")

    tk.Button(root, text="Close", command=root.destroy, bg="#c0392b", fg="white",
              font=("Arial", 12, "bold")).pack(pady=10)

    root.mainloop()

# ✅ Fixed entry point check
if __name__ == "__main__":
    if len(sys.argv) > 1:
        username = sys.argv[1]
        show_user_logs(username)
    else:
        print("No username provided to report_view.py")
