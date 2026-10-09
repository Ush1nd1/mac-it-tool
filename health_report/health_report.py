import os
import subprocess
import tkinter as tk


def run(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode().strip()
    except:
        return "Error"

def get_storage_info():
    if os.path.exists("/System/Volumes/Data"):
        storage_path = "/System/Volumes/Data"
    else:
        storage_path = "/"

    container_total = run("diskutil info / | awk -F'[()]' '/Container Total Space:/ {print $2}'")
    container_total = container_total.replace(" Bytes", "")
    container_total = int(container_total)
    container_total_gb = round(container_total / 1_000_000_000, 2)
    container_free = run("diskutil info / | awk -F'[()]' '/Container Free Space:/ {print $2}'")
    container_free = container_free.replace(" Bytes", "")
    container_free = int(container_free)
    container_free_gb = round(container_free / 1_000_000_000, 2)
    container_used = container_total - container_free
    container_used_gb = round(container_used / 1_000_000_000, 2)
    container_percent_used = round(container_used / container_total * 100, 2)

    used_blocks = run(f"df {storage_path} | awk 'NR==2 {{print $3}}'")

    used_blocks = int(used_blocks)
    used_space_gb = round(used_blocks * 512 / 1_000_000_000, 2)

    return used_space_gb, container_total_gb, container_free_gb, container_used_gb, container_percent_used


def system_report():
    results.delete(1.0, tk.END)
    results.insert(tk.END, "===== Mac Health Report =====\n\n")

    os_version = run("sw_vers -productVersion")
    serial = run("system_profiler SPHardwareDataType | awk '/Serial/ {print $4}'")
    computer_name = run("scutil --get ComputerName")
    hostname = run("hostname")
    uptime = run("uptime")

    used_space_gb, container_total_gb, container_free_gb, container_used_gb, container_percent_used = get_storage_info()
    
    filevault = run("fdesetup status | head -1")
    filevault = filevault.replace("FileVault is ", "").replace(".", "")

    results.insert(tk.END, f"macOS Version: {os_version}\n")
    results.insert(tk.END, f"Serial Number: {serial}\n")
    results.insert(tk.END, f"Computer Name: {computer_name}\n")
    results.insert(tk.END, f"Hostname: {hostname}\n")
    results.insert(tk.END, f"Uptime: {uptime}\n")
    results.insert(tk.END, "\nStorage\n")
    results.insert(tk.END, "--------------------------------\n")

    # APFS Container Storage
    results.insert(tk.END, f"APFS Container Capacity: {container_total_gb} GB\n")
    results.insert(tk.END, f"APFS Container Used: {container_used_gb} GB\n")
    results.insert(tk.END, f"APFS Container Free: {container_free_gb} GB\n")
    results.insert(tk.END, f"APFS Container Usage: {container_percent_used}%\n")
    # Data Volume Storage
    results.insert(tk.END, "\nAdvanced Storage Details\n")
    results.insert(tk.END, "--------------------------------\n")
    results.insert(tk.END, f"Data Volume Used: {used_space_gb} GB\n")

    results.insert(tk.END, "\nSecurity\n")
    results.insert(tk.END, "--------------------------------\n")
    results.insert(tk.END, f"FileVault: {filevault}\n")

app = tk.Tk()
app.title("Mac Health Reporter")
app.geometry("525x400")

title = tk.Label(app, text="Mac Health Reporter", font=("Helvetica", 16, "bold"))
title.pack(pady=10)

btn = tk.Button(app, text="Run Health Report", command=system_report)
btn.pack(pady=5)

results_frame = tk.Frame(app)
results_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(results_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

results = tk.Text(results_frame, height=18, width=70, wrap=tk.WORD, yscrollcommand=scrollbar.set)
results.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=results.yview)

app.mainloop()
