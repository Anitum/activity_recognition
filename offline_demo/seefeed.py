import tkinter as tk
from PIL import Image, ImageTk
import csv
import cv2

class SeeFeed:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Camera Feed")
        self.lastrow = 1

        # Importing logo image
        self.logo = Image.open("offline_demo/assets/Logo.png")
        # Resizing in proportion
        width, height = self.logo.size
        div_ratio = 6
        self.logo = self.logo.resize((int(width/div_ratio), int(height/div_ratio)))
        self.logo = ImageTk.PhotoImage(self.logo)

        # Making a frame for the logo
        self.frame_logo = tk.Frame(self.root)
        self.frame_logo.grid(row=0, column=0, sticky="nsew")

        # Making a label for logo
        self.logo_label = tk.Label(self.frame_logo, image=self.logo)
        self.logo_label.grid(row=0, column=0, sticky="nsew")

        # Making a label for camera feed
        self.feed_label = tk.Label(self.frame_logo, text="Camera Feed", font=("Arial", 16), padx=10, pady=10, justify="center")
        self.feed_label.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Read camera indices and paths from CSV
        self.cameras = self.read_cameras("offline_demo/assets/crt_data/cam_index.csv")
        print(len(self.cameras))

        # Create frames for camera feeds
        self.create_camera_frames()

        # Adding buttons for navigation
        self.back_button = tk.Button(self.root, text="Back", command=self.back)
        self.back_button.grid(row=len(self.cameras)+1, column=0, sticky="nsew")

        # Ctrl + q to quit
        self.root.bind("<Control-q>", lambda e: self.root.quit())


    def read_cameras(self,path):
        cameras = []
        try:
            with open(path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    cameras.append((int(row['index']), row['path']))
        except FileNotFoundError:
            print("File not found!")
        return cameras
    

    def create_camera_frames(self):

        for index, path in self.cameras:
            # Create a frame for each camera feed
            frame = tk.Frame(self.root, borderwidth=2, relief="groove")
            frame.grid(row=index + 1, column=0, sticky="nsew")

            # Display camera index
            tk.Label(frame, text=f"Camera {index}", font=("Arial", 12)).pack()

            # Display camera feed using OpenCV
            self.display_camera_feed(frame, path)

    def display_camera_feed(self, frame, path):
        # Use OpenCV to capture camera feed
        cap = cv2.VideoCapture(0)

        def show_frame():
            ret, frame_img = cap.read()
            if ret:
                # Convert frame image to RGB format
                frame_img_rgb = cv2.cvtColor(frame_img, cv2.COLOR_BGR2RGB)

                # Convert frame image to PIL format
                img_pil = Image.fromarray(frame_img_rgb)

                # Resize image to fit the frame
                            
                photo_size = img_pil.size
                ration = 500/photo_size[0]
                img_pil = img_pil.resize((int(photo_size[0]*ration), int(photo_size[1]*ration)))
                

                # Convert PIL image to Tkinter-compatible format
                img_tk = ImageTk.PhotoImage(img_pil)

                # Update label with the new frame
                label.config(image=img_tk)
                label.image = img_tk
                label.after(100, show_frame)  # Update frame every 10 milliseconds
            else:
                print(f"Failed to read from camera {path}")

        # Create label to display camera feed
        label = tk.Label(frame)
        label.pack()

        # Start capturing and displaying frames
        show_frame()

    def back(self):
        self.root.quit()
        self.root.destroy()
        import Running
        running = Running.Running()
        running.root.mainloop()

if __name__ == "__main__":
    seefeed = SeeFeed()
    seefeed.root.mainloop()
