import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime
import os

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
