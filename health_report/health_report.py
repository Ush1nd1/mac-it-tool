import subprocess
import tkinter as tk

def run(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode().strip()
    except:
        return "Error"

def system_report():
    results.delete(1.0, tk.END)
    results.insert(tk.END, "===== Mac Health Report =====\n\n")

    os_version = run("sw_vers -productVersion")
    serial = run("system_profiler SPHardwareDataType | awk '/Serial/ {print $4}'")
    hostname = run("hostname")
    uptime = run("uptime")
    
    disk_info = run("df -h /System/Volumes/Data | awk 'NR==2 {print $2, $3, $4, $5}'")
    disk_size, disk_used, disk_free, disk_percent_used = disk_info.split()
    
    filevault = run("fdesetup status")

    results.insert(tk.END, f"macOS Version: {os_version}\n")
    results.insert(tk.END, f"Serial Number: {serial}\n")
    results.insert(tk.END, f"Hostname: {hostname}\n")
    results.insert(tk.END, f"Uptime: {uptime}\n")
    results.insert(tk.END, f"Disk Size: {disk_size}\n")
    results.insert(tk.END, f"Used Space: {disk_used}\n")
    results.insert(tk.END, f"Free Space: {disk_free}\n")
    results.insert(tk.END, f"Percentage Used: {disk_percent_used}\n")
    results.insert(tk.END, f"FileVault Status: {filevault}\n")

app = tk.Tk()
app.title("Mac Health Reporter")
app.geometry("550x400")

title = tk.Label(app, text="Mac Health Reporter", font=("Helvetica", 16, "bold"))
title.pack(pady=10)

btn = tk.Button(app, text="Run Health Report", command=system_report)
btn.pack(pady=5)

results = tk.Text(app, height=18, width=70)
results.pack(pady=10)

app.mainloop()
