import tkinter as tk
from PIL import Image, ImageTk

class ContactUs:
    def __init__(self):

        
        self.root = tk.Tk()
        self.root.title("Contact us")

        # dividing root in 3 x 1 grid
        self.root.grid_rowconfigure([0, 1, 2], weight=1)
        self.root.grid_columnconfigure(0, weight=1)

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
        self.Running_txt = tk.Label(self.frame0, text="Contact Us", font=("Arial", 16), padx=10, pady=10, justify="center")
        self.Running_txt.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # adding text box for contact us
        self.contact_us = tk.Text(self.root, wrap=tk.WORD)

        # make it little small 
        self.contact_us.config(width=50, height=10)
        
        # writing multiline text
        self.contact_text = """For any queries or suggestions, please contact us at:


        Het Patel:      Phone: 1234567890, 
                        Email: het@gmail.com

        Mridul :        Phone: 1234567890, 
                        Email: mridul@gmail.com

        """
        self.contact_us.insert(tk.END, self.contact_text)
        
        self.contact_us.grid(row=1, column=0, sticky="nsew")

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

        





if __name__ == "__main__":
    running = ContactUs()
    running.root.mainloop()