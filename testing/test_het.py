
import face_recognition
import cv2
import numpy as np
import csv
import os
import json
from datetime import datetime

video_capture = cv2.VideoCapture(0)
#cv2.imshow("video",video_capture)

def add_teacher_info():
    name = input("Enter teacher's name: ")
    photo_path = input("Enter path to teacher's photo: ")

    # Get the current directory of the script
    current_directory = os.path.dirname(__file__)
    
    image = face_recognition.load_image_file(photo_path)

    # Find face encodings in the image
    face_encodings = face_recognition.face_encodings(image)

    if len(face_encodings) == 1:  # Assuming only one face is present in the image
        # Get the face encoding
        encoding = face_encodings[0]

        # Get the current directory of the script
        current_directory = os.path.dirname(__file__)

        # Relative path to the JSON file
        json_file_path = os.path.join(current_directory, "teachers_info.json")

        # Check if the JSON file exists
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as f:
                data = json.load(f)
        else:
            data = {"teachers": []}

        # Append new teacher information to the list of teachers
        teacher_info = {
            "name": name,
            "photo_path": photo_path,
            "entry_time": [],
            "known_face_encodings": encoding.tolist()  # Add face encoding to teacher info
        }
        data["teachers"].append(teacher_info)

        # Write updated data back to the JSON file
        with open(json_file_path, 'w') as f:
            json.dump(data, f, indent=4)
        
        print("Encoded!.")
    else:
        print("Error: Unable to detect a single face in the provided image.")
    return json_file_path


def delete_teacher_info(name):
    current_directory = os.path.dirname(__file__)
    json_file_path = os.path.join(current_directory, "teachers_info.json")

    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    if name in data:
        del data[name]
        print(f"Teacher '{name}' information deleted successfully.")
    else:
        print(f"Teacher '{name}' not found.")

    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=4)


#                          CODE STARTS FROM HERE                          #

pathhh = add_teacher_info()
# Example usage:
data = json.load(open(pathhh, 'r'))
known_teacher_names = [teacher["name"] for teacher in data["teachers"]]
known_teacher_encodings = [np.array(teacher["known_face_encodings"]) for teacher in data["teachers"]] 
#known_teacher_encodings = [teacher.get("known_face_encodings", []) for teacher in data["teachers"]]
# Now you can use the known_face_encodings and known_face_names lists

Teachers = known_teacher_names.copy()

face_locations = []
face_encodings = []
face_names = []
s=True
 
 
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
 
 

f = open(current_date+'.csv','w+',newline = '')
lnwriter = csv.writer(f)
 
while True:
    _,frame = video_capture.read()
    small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
    rgb_small_frame = small_frame[:,:,::-1]
    breakpoint()
    if s:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations)
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_teacher_encodings, face_encoding)
            name = ""
            face_distance = face_recognition.face_distance(known_teacher_encodings, face_encoding)
            best_match_index = np.argmin(face_distance)
            if matches[best_match_index]:
                name = Teachers[best_match_index]
 
            face_names.append(name)
            if name in Teachers:
                font = cv2.FONT_HERSHEY_SIMPLEX
                bottomLeftCornerOfText = (10,100)
                fontScale              = 1.5
                fontColor              = (255,0,0)
                thickness              = 3
                lineType               = 2
 
                cv2.putText(frame,name+' Present', 
                    bottomLeftCornerOfText, 
                    font, 
                    fontScale,
                    fontColor,
                    thickness,
                    lineType)
 

                Teachers.remove(name)
                print(Teachers)
                current_time = now.strftime("%H-%M-%S")
                lnwriter.writerow([name,current_time])
    cv2.imshow("attendence system",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
video_capture.release()
cv2.destroyAllWindows()
f.close()