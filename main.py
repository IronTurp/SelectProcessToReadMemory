import ctypes
import psutil
import tkinter as tk

# Define a struct to represent the player's position data
class PlayerPosition(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
        ("z", ctypes.c_float)
    ]

# Create a Tkinter GUI window with a listbox and button
root = tk.Tk()
root.title("Select process")
process_listbox = tk.Listbox(root, width=40)
for proc in psutil.process_iter(['pid', 'name']):
    process_listbox.insert(tk.END, f"{proc.info['name']} (PID: {proc.info['pid']})")
select_button = tk.Button(root, text="Select", command=root.quit)
process_listbox.pack()
select_button.pack()

# Wait for the user to select a process
root.mainloop()

# Get the selected process ID
selected_process = psutil.process_iter('pid', 'name').nth(process_listbox.curselection()[0])
pid = selected_process.info['pid']

# Open the selected process by PID
process = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, pid)

# Read the memory address where the player's position data is stored
address = 0x12345678  # replace with the memory address of the player's position data
buffer = ctypes.create_string_buffer(ctypes.sizeof(PlayerPosition))

# Read the bytes from memory into the buffer
ctypes.windll.kernel32.ReadProcessMemory(process, address, buffer, ctypes.sizeof(PlayerPosition), None)

# Convert the bytes to a PlayerPosition object
player_position = PlayerPosition.from_buffer(buffer)

# Print the player's position data
print(f"Player position: x={player_position.x}, y={player_position.y}, z={player_position.z}")
