import os
import subprocess
import tkinter as tk
from tkinter import messagebox

def run(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode().strip()
    except:
        return "Error"

# ---------------- SYSTEM INFO ----------------

def system_report():
    results.delete(1.0, tk.END)
    results.insert(tk.END, "===== Mac Health Report =====\n\n")

    os_version = run("sw_vers -productVersion")
    serial = run("system_profiler SPHardwareDataType | awk '/Serial/ {print $4}'")
    hostname = run("hostname")
    uptime = run("uptime")
    disk = run("df -h / | awk 'NR==2 {print $5}'")
    filevault = run("fdesetup status")

    results.insert(tk.END, f"macOS Version: {os_version}\n")
    results.insert(tk.END, f"Serial Number: {serial}\n")
    results.insert(tk.END, f"Hostname: {hostname}\n")
    results.insert(tk.END, f"Uptime: {uptime}\n")
    results.insert(tk.END, f"Disk Usage: {disk}\n")
    results.insert(tk.END, f"FileVault Status: {filevault}\n")

# ---------------- STORAGE ALERT ----------------

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

# ---------------- STORAGE SCAN ----------------

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

    # 🔬 Deep scan
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

# ---------------- SHOW PATHS ----------------

def show_biggest_locations():
    if not biggest_paths:
        messagebox.showwarning("No Data", "Run Scan Storage first.")
        return

    results.insert(tk.END, "\n📍 Largest Folder Locations\n\n")

    for path in biggest_paths[:10]:
        results.insert(tk.END, f"{path}\n")

# ---------------- GUI ----------------

biggest_paths = []

app = tk.Tk()
app.title("Mac IT Utility")
app.geometry("560x460")

title = tk.Label(app, text="Mac IT Utility", font=("Helvetica", 16, "bold"))
title.pack(pady=10)

btn_frame = tk.Frame(app)
btn_frame.pack(pady=5)

health_btn = tk.Button(btn_frame, text="System Health Report", command=system_report)
health_btn.grid(row=0, column=0, padx=5)

alert_btn = tk.Button(btn_frame, text="Check Storage Alert", command=check_storage)
alert_btn.grid(row=0, column=1, padx=5)

scan_btn = tk.Button(btn_frame, text="Scan Largest Folders", command=scan_storage)
scan_btn.grid(row=0, column=2, padx=5)

open_btn = tk.Button(btn_frame, text="Show Largest Folder Locations", command=show_biggest_locations)
open_btn.grid(row=0, column=3, padx=5)

results = tk.Text(app, height=20, width=72)
results.pack(pady=10)

app.mainloop()