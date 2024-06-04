import tkinter as tk
from PIL import Image, ImageTk
import csv
from tkinter import ttk

#Todo: Add a scrollbar to the table
#Todo: Add a search bar to the table
#Todo: Add a filter to the table
#Todo: Add a button to export the data to a csv file

class history:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Contact us")

        # dividing root in 3 x 1 grid
        self.root.grid_rowconfigure([0, 1, 2], weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # importing logo image
        self.logo = Image.open("offline_demo/assets/Logo.png")
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
 
        self.load_data(r"offline_demo/assets/crt_data/history_data.csv")
        self.display_table()
        # making a label for contact us texr
        self.Running_txt = tk.Label(self.frame0, text="History", font=("Arial", 16), padx=10, pady=10, justify="center")
        self.Running_txt.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)



        # adding buttons send in row 2
        self.send = tk.Button(self.root, text="back", command=self.back)
        
        self.send.grid(row=2, column=0, sticky="nsew")

        # ctrl + q to quit
        self.root.bind("<Control-q>", lambda e: self.root.quit())


    def back(self):
        self.root.quit()
        self.root.destroy()
        import Running
        running = Running.Running()
        running.root.mainloop()
    
    def load_data(self, path):
        self.history_data = []
        try:
            with open(path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.history_data.append(row)
        except FileNotFoundError:
            print("File not found!")

    def display_table(self):
        columns = ['emp_id', 'name', 'date', 'time_stamp', 'status']
        self.table = ttk.Treeview(self.root, columns=columns, show='headings')
        for col in columns:
            self.table.heading(col, text=col)
        for data in self.history_data:
            self.table.insert("", "end", values=(data['emp_id'], data['name'], data['date'], data['time_stamp'], data['status']))
        self.table.grid(row=1, column=0, sticky="nsew")



        





if __name__ == "__main__":
    running = history()
    running.root.mainloop()