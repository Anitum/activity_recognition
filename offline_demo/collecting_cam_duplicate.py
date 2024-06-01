import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import re
from PIL import Image, ImageTk


#TODO add a function to add local cameras and to read from local cam 


class CollectingCam:
    def __init__(self):

        self.source = [("me",0)]
        self.root = tk.Tk()
        self.root.title("Adding Cameras")

        # importing logo image
        self.logo = Image.open("GuiApp/build/assets/Logo.png")
        # resizing in proportion
        width, height = self.logo.size
        div_ration = 6
        self.logo = self.logo.resize((int(width/div_ration), int(height/div_ration)))
        self.logo = ImageTk.PhotoImage(self.logo)

        # making a frame for 0 th row
        self.frame0 = tk.Frame(self.root)
        self.frame0.grid(row=0, column=0, sticky="nsew")

        # dividing frame0 in 1 x 2 grid
        self.frame0.grid_rowconfigure(0, weight=1)
        self.frame0.grid_columnconfigure([0, 1], weight=1)

        # making a label for logo
        self.logo_label = tk.Label(self.frame0, image=self.logo)
        self.logo_label.grid(row=0, column=0, sticky="nsew")
        # this should just big enough to fit the logo
        self.logo_label.config(width=50, height=10)

        # making a label for contact us texr
        self.Running_txt = tk.Label(self.frame0, text="Adding Cameras", font=("Arial", 16), padx=10, pady=10, justify="center")
        self.Running_txt.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # adding text box for contact us
        self.contact_us = tk.Text(self.root, wrap=tk.WORD)


        # make frame1 for this row 
        self.frame1 = tk.Frame(self.root)
        self.frame1.grid(row=1, column=0, sticky="nsew")

        # adding text box for search for local cameras
        self.search_local = tk.Label(self.frame1, text="Search for local cameras........", anchor="c")
        self.search_local.config(width=50)
        self.search_local.grid(row=0, column=0, sticky="nsew", padx=10, pady=20)

        # adding text box for search for ip cameras
        self.search_ip = tk.Label(self.frame1, text="Search for ip cameras", anchor="c")
        self.search_ip.config(width=50)
        self.search_ip.grid(row=1, column=0, sticky="nsew", padx=10)

        # adding entry for ip cameras
        self.ip_entry = tk.Entry(self.frame1)
        self.ip_entry.config(width=50)
        self.ip_entry.grid(row=2, column=0, sticky="nsew",padx= 10, pady= 10)

        # adding button for add ip camera
        self.add_ip = tk.Button(self.frame1, text="Add IP Camera", command=self.add_ip,)
        self.add_ip.grid(row=3, column=0, sticky="ns", pady= 10)

        # printing table of added cameras
        self.table_label = tk.Label(self.frame1, text="Table of added cameras")
        self.table_label.config(width=50, height=2)
        self.table_label.grid(row=4, column=0, sticky="nsew")

        # Create Treeview for table display
        self.tree = ttk.Treeview(self.frame1, columns=("Name", "Path"), show="headings", height=5)
        self.tree.heading("Name", text="Name")
        self.tree.heading("Path", text="Path")
        self.tree.grid(row=5, column=0, sticky="nsew")

        # making a frame for 3 th row 
        self.frame3 = tk.Frame(self.root)
        self.frame3.grid(row=4, column=0, sticky="nsew")


        # adding "Next" button
        self.next_button = tk.Button(self.frame3, text="Next", command=self.next, width=23)
        self.next_button.grid(row=0, column=1, sticky="nsew")
        #back button
        self.back_button = tk.Button(self.frame3, text="Back", command=self.back,width=23)
        self.back_button.grid(row=0, column=0, sticky="nsew" )


        # ctrl + q to quit
        self.root.bind("<Control-q>", lambda e: self.root.quit())

    def back(self):
        self.root.quit()
        self.root.destroy()
        import Running
        running = Running.Running()
        running.root.mainloop()


    def add_ip(self):
        name = self.ip_entry.get()
        # ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
        # if not name:
        #     messagebox.showerror("Error", "Please enter a name for the camera.")
        #     return
        # if not re.match(ip_pattern, name):
        #     messagebox.showerror("Error", "Invalid IP address!")
        #     return

        self.source.append(name)
        self.display_sources()


    def display_sources(self):
        # Clear the existing table
        self.tree.delete(*self.tree.get_children())

        # Display the updated list of sources
        for idx, source in enumerate(self.source):
            self.tree.insert("", "end", values=(f"Camera {idx+1}", source))

    def next(self):
        self.root.quit()
        self.root.destroy()
        import setup_cams
        a = setup_cams.App(self.source)
        print(self.source)
        a.root.mainloop()

if __name__ == "__main__":
    running = CollectingCam()
    running.root.mainloop()
