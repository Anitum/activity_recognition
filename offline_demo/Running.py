import tkinter as tk
from PIL import Image, ImageTk
import csv

import face_recognition
import cv2
from datetime import datetime


class Running:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Running window")

        # dividing root in 6 x 1 grid
        self.root.grid_rowconfigure([0, 1, 2, 3, 4, 5], weight=1)
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

        # making a label for Running texr
        self.Running_txt = tk.Label(self.frame0, text="Running.......", font=("Arial", 16), padx=10, pady=10, justify="center")
        self.Running_txt.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # adding buttons see feed in row 1 
        self.see_feed = tk.Button(self.root, text="See Feed", command=self.seefeed)
        self.see_feed.grid(row=1, column=0, sticky="nsew")

        # adding buttons see history in row 2
        self.see_history = tk.Button(self.root, text="See History", command=self.seehistory)
        self.see_history.grid(row=3, column=0, sticky="nsew")



        # adding buttons add or remove employee in row 3
        self.add_remove_employee = tk.Button(self.root, text="Add/Remove Employee", command=self.add_remove_employee)
        self.add_remove_employee.grid(row=2, column=0, sticky="nsew")



        # adding buttons add or remove employee in row 3
        self.add_remove_employee = tk.Button(self.root, text="Add/Remove Cameras", command=self.add_remove_camera)
        self.add_remove_employee.grid(row=4, column=0, sticky="nsew")

        

        # adding buttons settings in row 4
        # self.settings = tk.Button(self.root, text="Settings", command=self.settings)
        # self.settings.grid(row=5, column=0, sticky="nsew")

        # adding buttons contact in row 5
        self.contact = tk.Button(self.root, text="Contact", command=self.contact)
        self.contact.grid(row=6, column=0, sticky="nsew")

        # ctrl + q to quit
        self.root.bind("<Control-q>", lambda e: self.root.quit())



    def add_remove_camera(self):
        self.root.destroy()
        import collecting_cam_duplicate
        collecting_cam = collecting_cam_duplicate.CollectingCam()
        collecting_cam.root.mainloop()
        print("Add or remove camera")
        

 
    def seefeed(self):
        self.root.destroy()
        # read files form selectd camera and show feed

        sources = []
        # with open('GuiApp/build/assets/crt_data/cam_selected.csv', 'r') as file:
        #     # if file have more than one line
        #     reader = csv.reader(file)
        #     try:

        #         next(reader)  # Skip header row
        #         for row in reader:
        #             try:
        #                 row[1] = int(row[1])
        #                 sources.append((row[0], row[1]))
        #             except:
        #                 sources.append((row[0], row[1]))
        #     except:
        #         sources.append(('me', 0))
        #         print(1)

        # import camp_capture
        # camp_capture = camp_capture.App(sources)
        # camp_capture.root.mainloop()
        # print("See feed")
        self.att()
    
    def seehistory(self):
        self.root.destroy()
        import history
        history = history.history()
        history.root.mainloop()
        print("See history")

    def add_remove_employee(self):
        # a pop up window asking for adding or removing employee

        
        popup = tk.Toplevel(self.root)
        popup.title("Add or Remove")
        popup.grid_columnconfigure(0, weight=1, uniform="buttons")
        popup.grid_columnconfigure(1, weight=1, uniform="buttons")

        label = tk.Label(popup, text="Do you want to add or remove?", padx=20, pady=10)
        label.grid(row=0, column=0, columnspan=2)

        add_button = tk.Button(popup, text="Add", command=self.add_emp, padx=10, pady=10)
        add_button.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        remove_button = tk.Button(popup, text="Remove", command=self.remove_emp)
        remove_button.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        print("Add or remove employee")
    
    def add_emp(self):
        print("Add employee")

    def remove_emp(self):
        self.root.destroy()
        import removing
        removing = removing.Removing()
        removing.root.mainloop()


    def settings(self):
        # self.root.destroy()
        # import settings
        # settings = settings.settings()
        # settings.root.mainloop()
        print("Settings")
    
    def contact(self):
        self.root.destroy()
        import contactus
        contactus = contactus.ContactUs()
        contactus.root.mainloop()


    def att(self):
        
        video_capture = cv2.VideoCapture(0)
    
        # Define known face encodings and names
        jobs_image = face_recognition.load_image_file("photos/jobs.jpg")
        jobs_encoding = face_recognition.face_encodings(jobs_image)[0]
    
        ratan_tata_image = face_recognition.load_image_file("photos/tata.jpg")
        ratan_tata_encoding = face_recognition.face_encodings(ratan_tata_image)[0]
    
        sadmona_image = face_recognition.load_image_file("photos/sam.jpg")
        sadmona_encoding = face_recognition.face_encodings(sadmona_image)[0]
    
        tesla_image = face_recognition.load_image_file("photos/musk.jpg")
        tesla_encoding = face_recognition.face_encodings(tesla_image)[0]
    
        known_face_encodings = [
            jobs_encoding,
            ratan_tata_encoding,
            sadmona_encoding,
            tesla_encoding
        ]
    
        known_face_names = [
            "jobs",
            "ratan tata",
            "sadmona",
            "tesla"
        ]
    
        # Create CSV file for attendance
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        csv_file_path = current_date + '.csv'
        csv_file = open(csv_file_path, 'w+', newline='')
        csv_writer = csv.writer(csv_file)
    
        while True:
            ret, frame = video_capture.read()
            if not ret:
                break
            
            # Find faces in the frame
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    
            for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
                # Check if the face matches any known faces
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
    
                if True in matches:
                    # Find the index of the first matching known face
                    matched_index = matches.index(True)
                    name = known_face_names[matched_index]
    
                    # Write attendance to CSV
                    current_time = now.strftime("%H:%M:%S")
                    csv_writer.writerow([name, current_time])
    
                # Draw rectangle and label on the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    
            # Display the resulting image
            cv2.imshow('Video', frame)
    
            # Exit loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        # Release handle to the webcam and close CSV file
        video_capture.release()
        csv_file.close()
    
        # Close all OpenCV windows
        cv2.destroyAllWindows()
    
    
    
    
    
    
    
    
    
if __name__ == "__main__":
    running = Running()
    running.root.mainloop()