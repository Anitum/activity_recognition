import tkinter as tk
import cv2
from threading import Thread

class CameraSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera Selection")

        # Get available cameras
        self.available_cameras = self.list_available_cameras()

        # Create a list to store selected cameras
        self.selected_cameras = []

        # Create checkboxes for camera selection
        for camera_index in self.available_cameras:
            checkbox = tk.Checkbutton(root, text=f"Camera {camera_index}", command=lambda idx=camera_index: self.toggle_camera(idx))
            checkbox.pack()

        # Create an area to display camera feed
        self.camera_feed_label = tk.Label(root)
        self.camera_feed_label.pack()

        # Create an entry for remote camera URL
        self.remote_url_entry = tk.Entry(root)
        self.remote_url_entry.insert(0, "http://your_remote_camera_url_here")
        self.remote_url_entry.pack()

        # Create a button to confirm the selection
        tk.Button(root, text="Select Camera", command=self.select_camera).pack()

    def list_available_cameras(self):
        """Detect available cameras and return their indices."""
        available_cameras = []
        for camera_index in range(10):  # You can adjust the range as needed
            cap = cv2.VideoCapture(camera_index)
            if cap.isOpened():
                available_cameras.append(camera_index)
                cap.release()
        return available_cameras

    def toggle_camera(self, camera_index):
        if camera_index in self.selected_cameras:
            self.selected_cameras.remove(camera_index)
        else:
            self.selected_cameras.append(camera_index)

    def select_camera(self):
        print(f"Selected cameras: {self.selected_cameras}")

        # Start threads to display camera feeds
        for camera_index in self.selected_cameras:
            t = Thread(target=self.display_camera_feed, args=(camera_index,))
            t.start()

    def display_camera_feed(self, camera_index):
        cap = cv2.VideoCapture(camera_index)
        while True:
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
                img = tk.PhotoImage(data=self._convert_frame_to_bytes(frame))
                self.camera_feed_label.config(image=img)
                self.camera_feed_label.photo = img
            else:
                print(f"Error reading frame from camera {camera_index}")
                break

    def _convert_frame_to_bytes(self, frame):
        _, img_encoded = cv2.imencode(".png", frame)
        return img_encoded.tobytes()

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraSelector(root)
    root.mainloop()
