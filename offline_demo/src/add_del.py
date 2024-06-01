
import face_recognition
import cv2
import os
import json
import face_recognition
import cv2

video_capture = cv2.VideoCapture(0)
#cv2.imshow("video",video_capture)

def add_teacher_info(name,ID, photo_path,):
    #name = input("Enter teacher's name: ")
    #photo_path = input("Enter path to teacher's photo: ")

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
            "ID": ID,  # Add teacher's ID to teacher info
            "photo_path": photo_path,
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


def delete_teacher_info(name, ID):
    current_directory = os.path.dirname(__file__)
    json_file_path = os.path.join(current_directory, "teachers_info.json")

    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    teachers = data["teachers"]
    teacher_found = False

    for teacher in teachers:
        if teacher["name"] == name and teacher["ID"] == ID:
            teachers.remove(teacher)
            teacher_found = True
            break
    
    if teacher_found:
        print(f"Teacher '{name}' with ID '{ID}' information deleted successfully.")
    else:
        print(f"Teacher '{name}' with ID '{ID}' not found.")

    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=4)


#                          CODE STARTS FROM HERE                          #
rad = input("Enter 1 to add teacher info, 2 to delete teacher info: ")
if rad == '1':
    name = input("Enter teacher's name: ")
    ID = input("Enter teacher's ID: ")
    photo_path = input("Enter path to teacher's photo: ")
    add_teacher_info(name, ID, photo_path)
elif rad == '2':
    name = input("Enter teacher's name: ")
    ID = input("Enter teacher's ID: ")
    delete_teacher_info(name, ID)
elif rad == '3':
    print("Continue...")
else:
    print("Invalid input. Please enter 1 or 2.")
    exit()


