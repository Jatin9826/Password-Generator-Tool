import tkinter as tk
from tkinter import messagebox, ttk
import random
import string
import pyperclip
import csv
from datetime import datetime

# Globals
theme = "light"
password_history = []

# Generate Password
def generate_password():
    try:
        length = int(length_entry.get())
        if length < 4:
            messagebox.showerror("Error", "Password length must be at least 4")
            return
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number")
        return

    use_digits = digits_var.get()
    use_special = special_var.get()
    avoid_ambiguous = ambiguous_var.get()

    characters = string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation

    if avoid_ambiguous:
        for ch in 'il1Lo0O':
            characters = characters.replace(ch, '')

    if not characters:
        messagebox.showerror("Error", "No characters selected to generate password.")
        return

    password = ''.join(random.choice(characters) for _ in range(length))
    password_var.set(password)

    update_strength(password)
    add_to_history(password)


# Copy to clipboard
def copy_to_clipboard():
    pwd = password_var.get()
    if pwd:
        pyperclip.copy(pwd)
        messagebox.showinfo("Copied", "Password copied to clipboard!")

# Save to file
def save_to_csv():
    pwd = password_var.get()
    if pwd:
        with open("passwords.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), pwd])
        messagebox.showinfo("Saved", "Password saved to passwords.csv")

# Password strength indicator
def update_strength(password):
    strength = "Weak"
    score = 0

    if len(password) >= 8:
        score += 1
    if any(ch in string.digits for ch in password):
        score += 1
    if any(ch in string.punctuation for ch in password):
        score += 1
    if any(ch.islower() for ch in password) and any(ch.isupper() for ch in password):
        score += 1

    if score == 4:
        strength = "Strong"
        strength_bar.config(style="green.Horizontal.TProgressbar")
    elif score == 3:
        strength = "Moderate"
        strength_bar.config(style="orange.Horizontal.TProgressbar")
    else:
        strength = "Weak"
        strength_bar.config(style="red.Horizontal.TProgressbar")

    strength_label.config(text=f"Strength: {strength}")
    strength_bar["value"] = score * 25

# Add password to log
def add_to_history(password):
    password_history.append(password)
    history_list.insert(tk.END, password)

# Theme Toggle
def toggle_theme():
    global theme
    if theme == "light":
        root.config(bg="#2e2e2e")
        theme = "dark"
        for widget in root.winfo_children():
            try:
                widget.config(bg="#2e2e2e", fg="white")
            except:
                pass
    else:
        root.config(bg="#f0f4f8")
        theme = "light"
        for widget in root.winfo_children():
            try:
                widget.config(bg="#f0f4f8", fg="black")
            except:
                pass

# Setup GUI
root = tk.Tk()
root.title("🔐 Advanced Password Generator")
root.geometry("500x500")
root.config(bg="#f0f4f8")

# Styles
style = ttk.Style()
style.configure("green.Horizontal.TProgressbar", foreground='green', background='green')
style.configure("orange.Horizontal.TProgressbar", foreground='orange', background='orange')
style.configure("red.Horizontal.TProgressbar", foreground='red', background='red')

tk.Label(root, text="🔐 Password Generator Tool", font=("Arial", 16, "bold"), bg="#f0f4f8").pack(pady=10)

tk.Label(root, text="Enter Password Length (e.g., 20, 40):", bg="#f0f4f8").pack()
length_entry = tk.Entry(root)
length_entry.pack()

# Options
digits_var = tk.BooleanVar(value=True)
special_var = tk.BooleanVar(value=True)
ambiguous_var = tk.BooleanVar(value=False)

tk.Checkbutton(root, text="Include Digits (0-9)", variable=digits_var, bg="#f0f4f8").pack()
tk.Checkbutton(root, text="Include Special Characters (!@#$)", variable=special_var, bg="#f0f4f8").pack()
tk.Checkbutton(root, text="Avoid Ambiguous Characters (i,1,L,o,0,O)", variable=ambiguous_var, bg="#f0f4f8").pack()

tk.Button(root, text="Generate Password", command=generate_password, bg="#4CAF50", fg="white").pack(pady=10)

password_var = tk.StringVar()
tk.Entry(root, textvariable=password_var, font=("Courier", 12), width=40, justify='center').pack(pady=5)

# Strength indicator
strength_label = tk.Label(root, text="Strength: ", bg="#f0f4f8", font=("Arial", 10, "italic"))
strength_label.pack()
strength_bar = ttk.Progressbar(root, length=300, mode='determinate')
strength_bar.pack(pady=5)

# Buttons
tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard).pack(pady=5)
tk.Button(root, text="Save to CSV", command=save_to_csv).pack(pady=5)
tk.Button(root, text="Toggle Theme", command=toggle_theme).pack(pady=5)

# Password History
tk.Label(root, text="Password History:", bg="#f0f4f8").pack()
history_list = tk.Listbox(root, height=5)
history_list.pack(pady=5, fill=tk.X, padx=20)

root.mainloop()
