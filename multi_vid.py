import tkinter as tk
import cv2
from PIL import Image, ImageTk
import threading

class CameraFeedApp:
    def __init__(self, master, num_cams):
        self.master = master
        self.num_cams = num_cams
        self.camera_feeds = []
        self.create_widgets()

    def create_widgets(self):
        for i in range(self.num_cams):
            frame = tk.Frame(self.master, width=640, height=480)
            frame.grid(row=0, column=i)
            label = tk.Label(frame)
            label.grid(row=0, column=0)
            self.camera_feeds.append(label)

    def update_camera_feed(self, index, feed):
        success, frame = feed.read()
        if success:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            frame = ImageTk.PhotoImage(frame)
            self.camera_feeds[index].config(image=frame)
            self.camera_feeds[index].image = frame
        self.master.after(20, self.update_camera_feed, index, feed)

    def start_camera_feeds(self, video_sources):
        for i, source in enumerate(video_sources):
            feed = cv2.VideoCapture(source)
            t = threading.Thread(target=self.update_camera_feed, args=(i, feed))
            t.daemon = True
            t.start()

def main():
    num_cams = 2 # Change this to the number of camera feeds you want to display
    video_sources = [0, 0]  # Add your video sources here, for example: [0, 1, 2, ...]
    root = tk.Tk()
    app = CameraFeedApp(root, num_cams)
    app.start_camera_feeds(video_sources)
    root.mainloop()

if __name__ == "__main__":
    main()
