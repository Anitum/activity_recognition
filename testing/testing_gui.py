import tkinter as tk
from tkinter import ttk
import cv2
import PIL.Image, PIL.ImageTk  # Import these for displaying images in Tkinter

class CameraFeedSelectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera Feed Selection")
        
        # Create heading
        heading_label = tk.Label(root, text="Setup", font=('Helvetica', 16, 'bold'))
        heading_label.pack(pady=10)

        
        # List available camera feeds
        self.available_feeds = self.get_available_camera_feeds()
        
        # If no camera feeds found, display a message
        if not self.available_feeds:
            no_feed_label = tk.Label(self.root, text="No camera feeds found", font=('Helvetica', 12))
            no_feed_label.pack(pady=5)
        
        

        # Entry for URL input
        self.cam_feed()

    
        # Create button to confirm selection
        confirm_button = ttk.Button(self.root, text="Confirm", command=self.confirm_selection)
        confirm_button.pack(pady=10)


    def cam_feed(self):

        
        # Create frame to hold camera feed
        self.camera_frame = tk.Frame(self.root)
        self.camera_frame.pack()
        
        # Initialize camera feed display
        self.camera_label = tk.Label(self.camera_frame)
        self.camera_label.pack()
        self.update_camera_feed()  # Call the function to update camera feed
        
        # Create frame to hold camera feed selection
        self.feed_frame = ttk.Frame(self.root)
        self.feed_frame.pack(padx=10, pady=5)
        
        
        # Create checkboxes for camera feeds
        self.feed_checkboxes = []
        for feed in self.available_feeds:
            var = tk.BooleanVar()
            checkbox = ttk.Checkbutton(self.feed_frame, text=feed, variable=var)
            checkbox.pack(anchor=tk.W)
            self.feed_checkboxes.append((feed, var))

        heading_label = tk.Label(self.root, text="For remote camera enter URL below", font=('Helvetica', 11))
        heading_label.pack(pady=10)

        self.url_entry = ttk.Entry(self.root, width=40)
        self.url_entry.insert(tk.END, "Enter URL here")
        self.url_entry.pack()

        # Create button to confirm selection
        confirm_button = ttk.Button(self.root, text="Add Remote Camera", command=self.confirm_selection)
        confirm_button.pack()
        
        
    def get_available_camera_feeds(self):
        # Use OpenCV to get a list of available camera feeds
        available_feeds = []
        for i in range(10):  # Check up to 10 cameras (adjust as needed)
            try:
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    available_feeds.append(f"Camera {i}")
                    cap.release()
            except cv2.error as e:
                print(f"Error accessing camera {i}: {e}")
        return available_feeds
    
    def update_camera_feed(self):
        # Update camera feed in the label
        ret, frame = self.get_frame_from_camera()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.camera_label.config(image=self.photo)
            self.camera_label.image = self.photo
        self.root.after(10, self.update_camera_feed)  # Update every 10 milliseconds
    
    def get_frame_from_camera(self):
        # Capture frame from camera
        cap = cv2.VideoCapture(0)  # Assuming camera index 0
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) if ret else (ret, None)
        else:
            return False, None
    
    def confirm_selection(self):
        selected_feeds = [feed for feed, var in self.feed_checkboxes if var.get()]
        print("Selected camera feeds:", selected_feeds)
        # You can perform further processing with the selected feeds here

def main():
    root = tk.Tk()
    app = CameraFeedSelectionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
