import tkinter as tk
from PIL import Image, ImageTk

class tnc:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Terms and Conditions")
        

        # dividing root in 3 x 3 grid
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=10)
        self.root.grid_rowconfigure(2, weight=2)    
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=10)
        self.root.grid_columnconfigure(2, weight=2)

        # importing logo image 
        self.logo = Image.open("offline_demo/assets/Logo.png") 
        # resizing in proportion 
        width, height = self.logo.size
        div_ration = 6
        self.logo = self.logo.resize((int(width/div_ration), int(height/div_ration)))
        self.logo = ImageTk.PhotoImage(self.logo)
        self.logo_label = tk.Label(self.root, image=self.logo)
        self.logo_label.grid(row=0, column=0, sticky="nsew")

        
        self.frametnc = tk.Frame(self.root, width=100, height=100)
        self.frametnc.grid(row=1, column=1, sticky="nsew")
        # dividing frametnc in 3 rows
        self.frametnc.grid_rowconfigure(0, weight=0)
        self.frametnc.grid_rowconfigure(1, weight=10)
        self.frametnc.grid_rowconfigure(2, weight=0)
        self.frametnc.grid_columnconfigure(0, weight=10)
        self.frametnc.grid_columnconfigure(1, weight=0)

        self.term_heading = tk.Label(self.frametnc, text="Terms and Conditions", font=("Arial", 12), padx=10, pady=10, justify="center")
        self.term_heading.grid(row=0, column=0, sticky="nsew")

        # reading terms and conditions from file 
        with open("offline_demo/terms_conditon.txt", "r") as file:
            self.terms = file.read()

            #putting it in scrollable text box and also give scroll bar
            self.scrollbar = tk.Scrollbar(self.frametnc)
            self.scrollbar.grid(row=1, column=1, sticky="nsew")
            self.text_area = tk.Text(self.frametnc, wrap=tk.WORD, yscrollcommand=self.scrollbar.set)
            self.text_area.grid(row=1, column=0, sticky="nsew")
            self.scrollbar.config(command=self.text_area.yview)
            self.text_area.insert(tk.END, self.terms)



        #TODO: Add option to do installion of the software at give location 
    

        self.welcome_txt = tk.Label(self.root, text="Welcome to VAS", font=("Arial", 16), padx=10, pady=10, justify="center")
        self.welcome_txt.grid(row=0, column=1, sticky="nsew")

        self.button_accept = tk.Button(self.root, text="Accept", command=self.accept)
        self.button_accept.grid(row=2, column=2, sticky="nw", padx=10, pady=10)

        # if crtl q is pressed, the program will quit
        self.root.bind('<Control-q>', lambda e: self.root.quit())


        # i am not using mainloop() here because i want to call this class in another file
        # self.root.mainloop()

    def accept(self):
        # print("Accepted")
        self.root.destroy()
        import collecting_cam
        collecting_cam = collecting_cam.CollectingCam()
        collecting_cam.root.mainloop()


if __name__ == "__main__":
    tnc = tnc()
    tnc.root.mainloop()
    