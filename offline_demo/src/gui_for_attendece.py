import tkinter as tk

def select_offline_camera():
    print("Offline Camera Selected")

def select_online_camera():
    print("Online Camera Selected")

# Create the main window
root = tk.Tk()
root.title("Camera Selection")

# Create a label with large font
label = tk.Label(root, text="Please Connect Camera", font=("Helvetica", 24))
label.pack(pady=20)

# Create two buttons for selecting offline or online camera
offline_button = tk.Button(root, text="Offline Camera", command=select_offline_camera)
offline_button.pack(pady=10)

online_button = tk.Button(root, text="Online Camera", command=select_online_camera)
online_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
