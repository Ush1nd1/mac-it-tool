import os
import subprocess
import tkinter as tk

def run(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode().strip()
    except:
        return "Error"

def format_sizes(output):
    formatted = []

    for line in output.splitlines():
        parts = line.split("\t", 1)

        if len(parts) == 2:
            size, path = parts
            formatted.append(f"{size:>6}  {path}")
        else:
            formatted.append(line)

    return "\n".join(formatted)

def scan_storage():
    results.delete(1.0, tk.END)
    results.insert(tk.END, "📂 Largest Folders\n\n")
    results.insert(tk.END, "Note: Results include accessible folders only.\n")
    results.insert(tk.END, "Some locations may be excluded by macOS privacy permissions.\n\n")

    user_home = os.path.expanduser("~")

    folders = [
        "/Users",
        "/Applications",
        "/Library",
        f"{user_home}/Library"
    ]

    for folder in folders:
        display_name = folder.replace(user_home, "~")

        cmd = f"du -sh {folder}/* 2>/dev/null | sort -hr | head -3"
        output = run(cmd)
        formatted_output = format_sizes(output)

        results.insert(tk.END, f"Top in {display_name}:\n{formatted_output}\n\n")

    results.insert(tk.END, "\n🔬 Top User Library Subfolders\n\n")

    deep_paths = [
        f"{user_home}/Library/Application Support",
        f"{user_home}/Library/Containers",
        f"{user_home}/Library/Developer"
    ]

    for path in deep_paths:
        display_name = path.replace(user_home, "~")

        cmd = f'du -sh "{path}"/* 2>/dev/null | sort -hr | head -3'
        output = run(cmd)
        formatted_output = format_sizes(output)

        results.insert(tk.END, f"Top in {display_name}:\n{formatted_output}\n\n")


app = tk.Tk()
app.title("Mac Space Analyzer")
app.geometry("650x500")

title = tk.Label(app, text="Mac Space Analyzer", font=("Helvetica", 16, "bold"))
title.pack(pady=10)

btn_frame = tk.Frame(app)
btn_frame.pack(pady=5)

scan_btn = tk.Button(btn_frame, text="Scan Largest Folders", command=scan_storage)
scan_btn.grid(row=0, column=0, padx=5)

results_frame = tk.Frame(app)
results_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(results_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

results = tk.Text(
    results_frame,
    height=24,
    width=82,
    wrap=tk.NONE,
    yscrollcommand=scrollbar.set
)
results.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=results.yview)

app.mainloop()
