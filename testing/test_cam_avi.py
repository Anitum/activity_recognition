import cv2
import contextlib

def check_available_cameras():
    available_cameras = []
    
    # Check for camera indices from 0 to 9
    for i in range(10):
        with contextlib.suppress(UserWarning):
            cap = cv2.VideoCapture(i)
            
            # Check if camera is opened
            if cap.isOpened():
                # Release the camera capture object
                cap.release()
                available_cameras.append(i)
    
    return available_cameras

# Example usage:
if __name__ == "__main__":
    available_cameras = check_available_cameras()
    if available_cameras:
        print("Available camera feeds found:")
        for cam_index in available_cameras:
            print(f"Camera Index: {cam_index}")
    else:
        print("No camera feeds found.")