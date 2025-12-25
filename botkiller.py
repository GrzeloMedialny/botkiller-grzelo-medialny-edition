import psutil
import socket
import requests
import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import time
import os
import subprocess
from datetime import datetime

LOG_FILE = "botkiller_log.txt"
RISKY_COUNTRIES = ['RU', 'CN', 'KP', 'IR']
SCAN_INTERVAL = 300  # 5 minutes


def log_entry(entry):
    with open(LOG_FILE, "a") as log:
        log.write(f"{entry}\n")


def get_country(ip):
    try:
        response = requests.get(f"https://ipapi.co/{ip}/country/", timeout=3)
        return response.text.strip()
    except:
        return "?"


def block_ip(ip):
    try:
        command = f'netsh advfirewall firewall add rule name="Block {ip}" dir=out action=block remoteip={ip} enable=yes'
        subprocess.run(command, shell=True)
        return True
    except Exception as e:
        log_entry(f"Error blocking IP {ip}: {e}")
        return False


def scan_connections():
    output = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output.append(f"===== Scan at {timestamp} =====")
    conns = psutil.net_connections(kind='inet')

    for conn in conns:
        if conn.raddr:
            try:
                proc = psutil.Process(conn.pid).name()
            except:
                proc = "-"
            laddr = f"{conn.laddr.ip}:{conn.laddr.port}"
            raddr_ip = conn.raddr.ip
            raddr = f"{raddr_ip}:{conn.raddr.port}"
            pid = conn.pid or "-"
            country = get_country(raddr_ip)
            mark = "⚠️" if country in RISKY_COUNTRIES else ""
            entry = f"{proc:20} {pid:6} {laddr:22} {raddr:22} {country:3} {mark}"
            output.append(entry)
            log_entry(entry)
            if country in RISKY_COUNTRIES:
                block_ip(raddr_ip)
    return "\n".join(output)


def scan_and_display():
    result = scan_connections()
    text_area.config(state='normal')
    text_area.insert(tk.END, result + "\n\n")
    text_area.config(state='disabled')
    text_area.yview(tk.END)


def watcher():
    while True:
        scan_and_display()
        time.sleep(SCAN_INTERVAL)


def start_watcher():
    thread = threading.Thread(target=watcher, daemon=True)
    thread.start()

# === GUI === #
window = tk.Tk()
window.title("BotKiller v0.2 - Grzelo Medialny")
window.geometry("900x500")

frame = tk.Frame(window)
frame.pack(pady=10)

scan_button = tk.Button(frame, text="▶️ Skanuj teraz", command=scan_and_display, bg='red', fg='white')
scan_button.pack(side=tk.LEFT, padx=10)

start_button = tk.Button(frame, text="👁️ Uruchom watcher", command=start_watcher, bg='black', fg='lime')
start_button.pack(side=tk.LEFT, padx=10)

text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, state='disabled', bg='black', fg='lime', font=('Courier', 10))
text_area.pack(expand=True, fill='both', padx=10, pady=10)

log_entry("\n======================= START =======================")
scan_and_display()

window.mainloop()




