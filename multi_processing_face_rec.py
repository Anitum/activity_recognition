import face_recognition
import cv2
import numpy as np
import csv
import os
import json
from datetime import datetime
from multiprocessing import Process
import time

def copy_csv_to_bigger_file(source_csv, target_csv):
    # Open the source CSV file for reading
    with open(source_csv, 'r', newline='') as source_file:
        reader = csv.reader(source_file)
        data_to_copy = list(reader)  # Read all data from the source CSV into a list
    
    # Open the target CSV file for appending
    with open(target_csv, 'a', newline='') as target_file:
        writer = csv.writer(target_file)
        
        # Write the data from the source CSV to the target CSV
        writer.writerows(data_to_copy)

def process_camera(i):
    video_capture = cv2.VideoCapture(i)         
    json_file_path = r"D:\\face_rec\\teachers_info.json"
    data = json.load(open(json_file_path, 'r'))
    known_teacher_names = []
    known_teacher_encodings = []
    known_ID = []
    desired_fps = 10

    for teacher in data["teachers"]:
        known_teacher_names.append(teacher["name"])
        known_ID.append(teacher["ID"])
        known_teacher_encodings.append(np.array(teacher["known_face_encodings"]))

    Teachers = known_teacher_names.copy()

    face_locations = []
    face_encodings = []
    
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    f = open(current_date+'.csv','w+',newline = '')
    lnwriter = csv.writer(f)

    while True:
        start_time = time.time() 
        ret, frame = video_capture.read()
        if not ret:
            break

        # Find faces in the frame
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
            # Check if the face matches any known faces
            matches = face_recognition.compare_faces(known_teacher_encodings, face_encoding)
            name = "Unknown"
            
            if True in matches:
                # Find the index of the first matching known face
                matched_index = matches.index(True)
                name = known_teacher_names[matched_index]
                ID  = known_ID[matched_index]
                
                # Check if the teacher has already been marked within the last hour
                if name not in Teachers:
                    # Write attendance to CSV
                    current_time = now.strftime("%H:%M:%S")
                    current_date = now.strftime("%Y-%m-%d")
                    lnwriter.writerow([name,ID,'ENTRY', current_time, current_date])
                    Teachers.append(name)
                
                # ''' ( EXIT Functionality - hold for now, computationally heavy )
                if name in Teachers:
                    # Check if the teacher has already been marked within the last hour
                    with open(current_date+'.csv', 'r') as csv_file:
                        csv_reader = csv.reader(csv_file)
                        for row in csv_reader:
                            if row[0] == name and row[1] == 'ENTRY':
                                entry_time = datetime.strptime(row[2], "%H:%M:%S")
                                time_difference = now - entry_time
                                if time_difference.total_seconds() >= 3600:
                                    current_time = now.strftime("%H:%M:%S")
                                    current_date = now.strftime("%Y-%m-%d")
                                    lnwriter.writerow([name,ID, 'EXIT', current_time, current_date])
                                    Teachers.remove(name)
                                    break
                                
            # Draw rectangle and label on the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        # Display the resulting image
        cv2.imshow(f'Video-{i}', frame)  
        
        processing_time = time.time() - start_time
        delay_ms = max(1, int((1 / desired_fps - processing_time) * 1000))
        key = cv2.waitKey(delay_ms) & 0xFF

        # Exit loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    Teachers.clear()
    # Release handle to the webcam and close CSV file
    csv_file = open(current_date+'.csv','w+',newline = '')
    lnwriter = csv.writer(csv_file)

    video_capture.release()
    csv_file.close()

    video_capture.release()
    cv2.destroyAllWindows()
    f.close()

def start_camera_processes():
    processes = []
    selecting = 'y'
    #while selecting == 'y' or selecting == 'Y':
    i = (input("Please select the camera number 0 or the IP of the camera: "))
    p = Process(target=process_camera, args=(int(i),))
    p.start()
    processes.append(p)
    #selecting = input("Do you want to select another camera? (y/n) : ")
    i = 'http://172.17.75.22:4747/video'
    p = Process(target=process_camera, args=(i,))
    p.start()
    processes.append(p)


    for p in processes:
        p.join()

if __name__ == "__main__":
    start_camera_processes()


now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
per_day = (current_date+'.csv')
Downloaded_Attendance_path = r"D:\face_rec\Downloaded_Attendance.csv"
copy_csv_to_bigger_file(source_csv= per_day, target_csv=Downloaded_Attendance_path)
