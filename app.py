# Updated AI Career Counselor App with Circular Splash Animation
import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time
from google import genai
from google.genai import types

# Set up Gemini API
client = genai.Client(api_key="AIzaSyBfasvVkK-gQ4sEcEeSXM_DytD05MvBK9U")
model = "gemini-2.0-flash-lite"
generate_content_config = types.GenerateContentConfig(response_mime_type="text/plain")

# Placeholder clearing function
def clear_on_focus(entry, default_text):
    def on_focus(event):
        if entry.get() == default_text:
            entry.delete(0, tk.END)
    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, default_text)
    entry.bind("<FocusIn>", on_focus)
    entry.bind("<FocusOut>", on_focus_out)

# Functions for app logic
def add_skill_row():
    row = tk.Frame(skill_frame, bg="#f9f9f9")
    row.pack(fill="x", pady=5)
    skill_entry = tk.Entry(row, font=("Segoe UI", 11), width=25, relief="groove", bd=2)
    skill_entry.insert(0, "Skill")
    clear_on_focus(skill_entry, "Skill")
    skill_entry.pack(side="left", padx=5)
    exp_entry = tk.Entry(row, font=("Segoe UI", 11), width=10, relief="groove", bd=2)
    exp_entry.insert(0, "Years")
    clear_on_focus(exp_entry, "Years")
    exp_entry.pack(side="left", padx=5)
    skill_entries.append((skill_entry, exp_entry))

def get_career_advice():
    loading_label.config(text="🔄 Loading career advice...")
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)
    result_text.config(state=tk.DISABLED)
    progressbar.start()
    threading.Thread(target=fetch_career_advice).start()

def fetch_career_advice():
    name = name_entry.get().strip()
    if not name:
        show_error("Please enter your name.")
        return
    skill_info = []
    for skill_entry, exp_entry in skill_entries:
        skill = skill_entry.get().strip()
        exp = exp_entry.get().strip()
        if not skill or not exp or skill == "Skill" or exp == "Years":
            continue
        try:
            skill_info.append(f"{skill} ({int(exp)} yrs)")
        except ValueError:
            show_error(f"Experience for '{skill}' should be a number.")
            return
    if not skill_info:
        show_error("Please enter at least one skill and experience.")
        return

    prompt = (
        f"You are a helpful career counselor. The user's name is {name}. "
        f"The user has skills: {', '.join(skill_info)}. "
        f"Provide a suitable career suggestion in one sentence."
    )
    contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]

    try:
        full_response = ""
        for chunk in client.models.generate_content_stream(model=model, contents=contents, config=generate_content_config):
            full_response += chunk.text
        root.after(0, update_ui_with_response, full_response)
    except Exception as e:
        root.after(0, show_error, str(e))

def update_ui_with_response(response_text):
    result_text.config(state=tk.NORMAL)
    result_text.insert("1.0", response_text)
    result_text.config(state=tk.DISABLED)
    loading_label.config(text="")
    progressbar.stop()

def show_error(msg):
    progressbar.stop()
    loading_label.config(text="")
    messagebox.showerror("Error", msg)

def launch_main_app():
    splash.destroy()
    build_main_ui()

# Build main UI
def build_main_ui():
    global root, name_entry, skill_frame, skill_entries, result_text, loading_label, progressbar
    root = tk.Tk()
    root.title("🌟 AI Career Counselor")
    root.geometry("800x650")
    root.configure(bg="#f0f4f7")

    tk.Label(root, text="🌟 AI Career Counselor", font=("Segoe UI", 18, "bold"), bg="#f0f4f7", fg="#222").pack(pady=(15, 5))
    tk.Label(root, text="Enter Your Name:", font=("Segoe UI", 12), bg="#f0f4f7").pack(anchor="w", padx=20)
    name_entry = tk.Entry(root, font=("Segoe UI", 12), relief="solid", bd=2)
    name_entry.pack(fill="x", padx=20, pady=(0, 10))

    tk.Label(root, text="Add Skills and Years of Experience:", font=("Segoe UI", 12), bg="#f0f4f7").pack(anchor="w", padx=20)
    skill_frame = tk.Frame(root, bg="#f0f4f7")
    skill_frame.pack(fill="x", padx=20, pady=(0, 10))
    skill_entries = []
    add_skill_row()

    tk.Button(root, text="+ Add More Skills", command=add_skill_row, bg="#ffffff", fg="#007acc", font=("Segoe UI", 10, "bold"), relief="raised", bd=2).pack(pady=(0, 15))
    tk.Button(root, text="🎯 Get Career Advice", command=get_career_advice, bg="#2196F3", fg="white", font=("Segoe UI", 12, "bold"), padx=10, pady=5, relief="flat").pack(pady=(0, 10))

    loading_label = tk.Label(root, text="", font=("Segoe UI", 11), bg="#f0f4f7", fg="gray")
    loading_label.pack()

    progressbar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=300, mode='indeterminate')
    progressbar.pack(pady=(5, 10))

    tk.Label(root, text="Career Counselor's Advice:", font=("Segoe UI", 13, "bold"), bg="#f0f4f7").pack(anchor="w", padx=20, pady=(10, 0))
    result_text = tk.Text(root, height=7, font=("Segoe UI", 11), wrap="word", bg="#ffffff", bd=2, relief="sunken")
    result_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    result_text.config(state=tk.DISABLED)

    root.mainloop()

# Splash screen with circular animation
def splash_animation():
    global splash
    splash = tk.Tk()
    splash.overrideredirect(True)
    splash.geometry("500x300+500+250")
    splash.configure(bg="#4CAF50")

    tk.Label(splash, text="🎉 Welcome to AI Career Counselor 🎉", font=("Segoe UI", 16, "bold"), fg="white", bg="#4CAF50").pack(pady=40)

    canvas = tk.Canvas(splash, width=100, height=100, bg="#4CAF50", highlightthickness=0)
    canvas.pack()
    arc = canvas.create_arc(10, 10, 90, 90, start=0, extent=30, width=6, outline="white", style="arc")

    animation_id = None

    def animate_circle(angle=0):
        nonlocal animation_id
        canvas.itemconfig(arc, start=angle)
        animation_id = splash.after(30, animate_circle, (angle + 10) % 360)

    def safe_launch_main_app():
        if animation_id:
            splash.after_cancel(animation_id)
        splash.destroy()
        build_main_ui()

    animate_circle()
    splash.after(1500, safe_launch_main_app)
    splash.mainloop()


# Launch splash animation
splash_animation()