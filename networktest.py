import tkinter as tk
import socket
import subprocess
import re

# Function to get latency for an external IP
def get_latency(ip):
    try:
        result = subprocess.run(['ping', ip, '-n', '1'], capture_output=True, text=True)
        pos = result.stdout.find('time=')
        if pos == -1:
            return "Latency not found"
        return result.stdout[pos + 5:result.stdout.find('ms', pos)] + ' ms'
    except:
        return "Error"

# Function to get the IP address
def get_ip_address():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return "Error"

# Function to get the number of devices connected to the network
def get_connected_devices():
    try:
        result = subprocess.check_output("arp -a", shell=True, text=True)
        return len(set(re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', result)))
    except:
        return "Error"

# Function to update the GUI with current stats
def update_stats():
    latency_result.set("Latency: " + get_latency('8.8.8.8'))
    ip_address.set("IP Address: " + get_ip_address())
    devices_count.set("Devices connected: " + str(get_connected_devices()))

# Create and configure the main window
root = tk.Tk()
root.title("Network Performance Tool")

# Create Tkinter variables
latency_result = tk.StringVar()
ip_address = tk.StringVar()
devices_count = tk.StringVar()

# Create the GUI layout
tk.Label(root, text="Network Performance Tool", font=("Helvetica", 12)).grid(row=0, column=0, columnspan=2, pady=10)
tk.Label(root, textvariable=ip_address).grid(row=1, column=0, padx=10, pady=10)
tk.Label(root, textvariable=latency_result).grid(row=2, column=0, padx=10, pady=10)
tk.Label(root, textvariable=devices_count).grid(row=3, column=0, padx=10, pady=10)
tk.Button(root, text="Update", command=update_stats).grid(row=4, column=0, pady=10)

# Initialize stats
update_stats()

# Start the GUI event loop
root.mainloop()
