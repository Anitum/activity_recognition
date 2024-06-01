import tkinter as tk
from PIL import Image, ImageTk


class Running:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Running window")

        # dividing root in 6 x 1 grid
        self.root.grid_rowconfigure([0, 1, 2, 3, 4, 5], weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # importing logo image
        self.logo = Image.open("offline_demo/data/Logo.png")
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

        # making a label for Running texr
        self.Running_txt = tk.Label(self.frame0, text="Running.......", font=("Arial", 16), padx=10, pady=10, justify="center")
        self.Running_txt.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # adding buttons see feed in row 1 
        self.see_feed = tk.Button(self.root, text="See Feed", command=self.seefeed)
        self.see_feed.grid(row=1, column=0, sticky="nsew")

        # adding buttons see history in row 2
        self.see_history = tk.Button(self.root, text="See History", command=self.seehistory)
        self.see_history.grid(row=2, column=0, sticky="nsew")

        # adding buttons add or remove employee in row 3
        self.add_remove_employee = tk.Button(self.root, text="Add/Remove Employee", command=self.add_remove_employee)
        self.add_remove_employee.grid(row=3, column=0, sticky="nsew")

        # adding buttons settings in row 4
        self.settings = tk.Button(self.root, text="Settings", command=self.settings)
        self.settings.grid(row=4, column=0, sticky="nsew")

        # adding buttons contact in row 5
        self.contact = tk.Button(self.root, text="Contact", command=self.contact)
        self.contact.grid(row=5, column=0, sticky="nsew")

        # ctrl + q to quit
        self.root.bind("<Control-q>", lambda e: self.root.quit())



        

 
    def seefeed(self):
        # self.root.destroy()
        # import feed
        # feed = feed.feed()
        # feed.root.mainloop()
        print("See feed")
    
    def seehistory(self):
        self.root.destroy()
        
        history = history.history()
        history.root.mainloop()
        print("See history")

    def add_remove_employee(self):
        # a pop up window asking for adding or removing employee

        
        popup = tk.Toplevel(self.root)
        popup.title("Add or Remove")
        popup.grid_columnconfigure(0, weight=1, uniform="buttons")
        popup.grid_columnconfigure(1, weight=1, uniform="buttons")

        label = tk.Label(popup, text="Do you want to add or remove?", padx=20, pady=10)
        label.grid(row=0, column=0, columnspan=2)

        add_button = tk.Button(popup, text="Add", command=self.add_emp, padx=10, pady=10)
        add_button.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        remove_button = tk.Button(popup, text="Remove", command=self.remove_emp)
        remove_button.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        print("Add or remove employee")
    
    def add_emp(self):
        print("Add employee")

    def remove_emp(self):
        self.root.destroy()
        
        removing = removing.Removing()
        removing.root.mainloop()


    def settings(self):
        # self.root.destroy()
        # import settings
        # settings = settings.settings()
        # settings.root.mainloop()
        print("Settings")
    
    def contact(self):
        self.root.destroy()
        contactus = contactus.ContactUs()
        contactus.root.mainloop()
        
 








if __name__ == "__main__":
    running = Running()
    running.root.mainloop()