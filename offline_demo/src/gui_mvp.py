from tkinter import *
import cv2 as cv 

class setup_window:
    def __init__(self):
        self.root = Tk()
        self.root.title("Setup")

        # Create a label
        self.label = Label(self.root, text="Setup")
        self.label.pack()

        # Create a button
        self.button = Button(self.root, text="Start", command=self.root.quit)
        self.button.pack()


        self.root.mainloop()


if __name__ == "__main__":
    setupWin = setup_window()

        
