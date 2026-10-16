import subprocess
import tkinter as tk
from tkinter import messagebox

def run(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode().strip()
    except Exception:
        return "Error"

def check_storage():
    try:
        total = int(run("diskutil info / | awk -F'[()]' '/Container Total Space:/ {print $2}'").replace(" Bytes", ""))
        free = int(run("diskutil info / | awk -F'[()]' '/Container Free Space:/ {print $2}'").replace(" Bytes", ""))
    except ValueError:
        messagebox.showerror("Storage Error", "Unable to retrieve storage information.")
        return

    if total <= 0 or free < 0 or free > total:
        messagebox.showerror("Storage Error", "Unable to read valid storage information.")
        return

    disk_percent = round((total - free) / total * 100, 2)

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
app.title("Mac Storage Alert")
app.geometry("350x180")

title = tk.Label(app, text="Mac Storage Alert", font=("Helvetica", 16, "bold"))
title.pack(pady=15)

btn = tk.Button(app, text="Check Storage", command=check_storage)
btn.pack(pady=10)

app.mainloop()
