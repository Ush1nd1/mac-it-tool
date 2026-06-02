import os
import subprocess
import tkinter as tk
from tkinter import messagebox

def run(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode().strip()
    except:
        return "Error"

biggest_paths = []

def scan_storage():
    results.delete(1.0, tk.END)
    results.insert(tk.END, "📂 Largest Folders\n\n")

    user_home = os.path.expanduser("~")

    folders = [
        "/Users",
        "/Applications",
        "/Library",
        f"{user_home}/Library"
    ]

    biggest_paths.clear()

    for folder in folders:
        display_name = folder.replace(user_home, "~")

        cmd = f"du -sh {folder}/* 2>/dev/null | sort -hr | head -3"
        output = run(cmd)

        results.insert(tk.END, f"Top in {display_name}:\n{output}\n\n")

        for line in output.split("\n"):
            try:
                path = line.split("\t")[1]
                biggest_paths.append(path)
            except:
                pass

    results.insert(tk.END, "\n🔬 Top User Library Subfolders\n\n")

    deep_paths = [
        f"{user_home}/Library/Application Support",
        f"{user_home}/Library/Containers",
        f"{user_home}/Library/Developer"
    ]

    for path in deep_paths:
        display_name = path.replace(user_home, "~")

        cmd = f"du -sh {path}/* 2>/dev/null | sort -hr | head -3"
        output = run(cmd)

        results.insert(tk.END, f"Top in {display_name}:\n{output}\n\n")

def show_biggest_locations():
    if not biggest_paths:
        messagebox.showwarning("No Data", "Run Scan Storage first.")
        return

    results.insert(tk.END, "\n📍 Largest Folder Locations\n\n")

    for path in biggest_paths[:10]:
        results.insert(tk.END, f"{path}\n")

app = tk.Tk()
app.title("Mac Space Analyzer")
app.geometry("650x500")

title = tk.Label(app, text="Mac Space Analyzer", font=("Helvetica", 16, "bold"))
title.pack(pady=10)

btn_frame = tk.Frame(app)
btn_frame.pack(pady=5)

scan_btn = tk.Button(btn_frame, text="Scan Largest Folders", command=scan_storage)
scan_btn.grid(row=0, column=0, padx=5)

location_btn = tk.Button(btn_frame, text="Show Folder Locations", command=show_biggest_locations)
location_btn.grid(row=0, column=1, padx=5)

results = tk.Text(app, height=24, width=82)
results.pack(pady=10)

app.mainloop()
