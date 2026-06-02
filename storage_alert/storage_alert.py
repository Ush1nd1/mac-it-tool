import subprocess
import tkinter as tk
from tkinter import messagebox

def run(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode().strip()
    except:
        return "Error"

def check_storage():
    disk_percent = int(run("df -h / | awk 'NR==2 {print $5}'").replace('%',''))

    if disk_percent >= 90:
        alert = "🚨 CRITICAL: Drive almost full"
    elif disk_percent >= 75:
        alert = "🔴 HIGH USAGE: Cleanup needed soon"
    elif disk_percent >= 50:
        alert = "🟠 WARNING: Drive filling up"
    elif disk_percent >= 25:
        alert = "🟡 NOTICE: Storage usage rising"
    else:
        alert = "✅ Healthy storage level"

    messagebox.showinfo("Storage Status", f"Disk Usage: {disk_percent}%\n\n{alert}")

app = tk.Tk()
app.title("Storage Watch")
app.geometry("350x180")

title = tk.Label(app, text="Storage Watch", font=("Helvetica", 16, "bold"))
title.pack(pady=15)

btn = tk.Button(app, text="Check Storage", command=check_storage)
btn.pack(pady=10)

app.mainloop()
