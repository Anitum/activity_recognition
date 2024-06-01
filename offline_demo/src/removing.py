import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import csv
import Running


#Todo: Reduce both time and space complexity of the code it is makeing two copy of empdata one as list and other as dict resolve it 
#Todo: Add a label below it is also not actuall removing the employee from the csv file 
#Todo: styling is also not done yet 


class Removing:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Removing employee")

        # reading all the employee from the csv file

        # dividing root in 4 x 1 grid
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=10)
        self.root.grid_rowconfigure(2, weight=2)
        self.root.grid_rowconfigure(2, weight=2)
        self.root.grid_columnconfigure(0, weight=10)
        

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
        self.frame0.grid_columnconfigure(0, weight=1)
        self.frame0.grid_columnconfigure(1, weight=1)

        # making a label for logo
        self.logo_label = tk.Label(self.frame0, image=self.logo)
        self.logo_label.grid(row=0, column=0, sticky="nsew")

        # making a label for Removing employee text
        self.remove_txt = tk.Label(self.frame0, text="Removing employee", font=("Arial", 16), padx=10, pady=10, justify="center")
        self.remove_txt.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # making a frame for 1st row and within it making a frame for listbox using pack 
        self.frame1 = tk.Frame(self.root)
        self.frame1.grid(row=1, column=0, sticky="nsew")


        self.data = []
        self.employee_data = []
        self.load_data()


        # Create an Entry widget for search
        self.search_entry = tk.Entry(self.frame1)
        self.search_entry.pack(side=tk.TOP, fill=tk.X)

        # Bind the search function to the Entry widget
        self.search_entry.bind("<KeyRelease>", self.on_search)

        # Create a Listbox widget
        self.list_box = tk.Listbox(self.frame1)
        self.list_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a Scrollbar widget
        self.scrollbar = tk.Scrollbar(self.frame1, orient=tk.VERTICAL, command=self.list_box.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Link the Scrollbar to the Listbox
        self.list_box.config(yscrollcommand=self.scrollbar.set)

        # Populate list box with data
        self.populate_list()

        # Bind list box selection to populate search bar
        self.list_box.bind("<<ListboxSelect>>", self.on_list_select)

        # adding remove button in row 2
        self.remove_button = tk.Button(self.root, text="Remove", command=self.remove)
        self.remove_button.grid(row=2, column=0, sticky="nsew")



        # adding buttons send in row 2
        self.send = tk.Button(self.root, text="back", command=self.back)
        
        self.send.grid(row=3, column=0, sticky="nsew")

        # ctrl + q to quit
        self.root.bind("<Control-q>", lambda e: self.root.quit())


    def back(self):
        self.root.quit()
        self.root.destroy()

        running = Running.Running()
        running.root.mainloop()

    def remove(self):
        selection = self.list_box.curselection()
        if selection:
            index = selection[0]
            selected_item = self.list_box.get(index)
            emp_id = selected_item.split(":")[0].strip()
            self.confirm_removal(emp_id)
            self.load_data()
            self.populate_list()
        else:
            # label for no selection below button 
            self.no_selection = tk.Label(self.root, text="No employee selected", font=("Arial", 12), padx=10, pady=10, justify="center")
            self.no_selection.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)


    def load_data(self):
        self.data.clear()
        self.employee_data.clear()
        with open("GuiApp/build/assets/crt_data/employees.csv", newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.data.append((row['emp_id'], row['name']))

                self.employee_data.append({
                'emp_id': row['emp_id'],
                'name': row['name'],
                'ph_no': row['ph_no'],
                'img_path': row['img_path']})


    def populate_list(self):
        self.list_box.delete(0, tk.END)
        for emp_id, name in self.data:
            self.list_box.insert(tk.END, f"{emp_id}: {name}")

    def on_search(self, event=None):
        search_text = self.search_entry.get().lower()
        self.list_box.delete(0, tk.END)
        for emp_id, name in self.data:
            if search_text in emp_id.lower() or search_text in name.lower():
                self.list_box.insert(tk.END, f"{emp_id}: {name}")

    def on_list_select(self, event):
        selection = self.list_box.curselection()
        if selection:
            index = selection[0]
            selected_item = self.list_box.get(index)
            emp_id = selected_item.split(":")[0].strip()
            self.search_entry.delete(0, tk.END)
            self.search_entry.insert(tk.END, emp_id)

    
    def confirm_removal(self, emp_id):
        # Find employee details
        emp_details = None
        
        for emp in self.employee_data:
            if emp['emp_id'] == emp_id:
                emp_details = emp
                break

        if emp_details is None:
            print("Employee not found!")
            return

        # Create a new window for confirmation
        confirm_window = tk.Toplevel(self.root)
        confirm_window.title("Confirm Removal")

        # Display employee details
        tk.Label(confirm_window, text=f"Employee ID: {emp_details['emp_id']}").pack()
        tk.Label(confirm_window, text=f"Name: {emp_details['name']}").pack()
        tk.Label(confirm_window, text=f"Phone Number: {emp_details['ph_no']}").pack()

        # Load and display employee photo
        photo_path = emp_details['img_path']
        try:
            photo = Image.open(photo_path)
            
            photo_size = photo.size
            ration = 500/photo_size[0]
            photo = photo.resize((int(photo_size[0]*ration), int(photo_size[1]*ration)))
            photo = ImageTk.PhotoImage(photo)
            photo_label = tk.Label(confirm_window, image=photo)
            photo_label.photo = photo  # To prevent garbage collection
            photo_label.pack()
        except Exception as e:
            print(f"Error loading photo: {e}")

        # Confirmation buttons
        tk.Button(confirm_window, text="Export Data", command=lambda: self.export_employee_data(emp_details)).pack()
        tk.Button(confirm_window, text="Confirm Removal", command=lambda: self.remove_employee(emp_id)).pack()
        tk.Button(confirm_window, text="Cancel", command=confirm_window.destroy).pack()

    def export_employee_data(self, emp_details):
        # Export employee data to a CSV file
        filename = f"employee_{emp_details['emp_id']}.csv"
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['emp_id', 'name', 'ph_no', 'img_path']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(emp_details)
        messagebox.showinfo("Export Complete", f"Employee data exported to {filename}")

    def remove_employee(self, emp_id):
        # Ask for export confirmation
        if messagebox.askyesno("Export Confirmation", "Do you want to export the data of this employee before removal?"):
            # Find employee details
            emp_details = None
            for emp in self.employee_data:
                if emp['emp_id'] == emp_id:
                    emp_details = emp
                    break
            if emp_details:
                self.export_employee_data(emp_details)

        # Remove employee from data (sample implementation)
        for emp in self.employee_data:
            if emp['emp_id'] == emp_id:
                self.employee_data.remove(emp)
                break
        print(f"Employee with ID {emp_id} removed successfully!")

if __name__ == "__main__":
    tnc = Removing()
    tnc.root.mainloop()
