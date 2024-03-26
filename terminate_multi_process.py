import face_recognition
import cv2
import numpy as np
import csv
import os
import json
from datetime import datetime
from multiprocessing import Process
import time
import signal 


terminate_flag = False

def process_camera(i):
    global terminate_flag
    while not terminate_flag:
        video_capture = cv2.VideoCapture(i)         
        json_file_path = r"D:\\face_rec\\teachers_info.json"
        data = json.load(open(json_file_path, 'r'))
        known_teacher_names = []
        known_teacher_encodings = []
        known_ID = []
        desired_fps = 20

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
        Teachers.clear()
        while True:
            start_time = time.time() 
            ret, frame = video_capture.read()
            if not ret:
                print('Some error will loading frames')
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
                    if name not in Teachers :
                        with open(current_date+'.csv', 'r') as csv_file:
                            csv_reader = csv.reader(csv_file)
                            for row in csv_reader:
                                if not(row[0] == name and row[1] == 'ENTRY') or (row[0] == name and row[1] == 'EXIT'):
                                    current_time = now.strftime("%H:%M:%S")
                                    current_date = now.strftime("%Y-%m-%d")
                                    lnwriter.writerow([name,ID,'ENTRY', current_time, current_date])
                                    #csv_file = open(current_date+'.csv','w+',newline = '')
                                    lnwriter = csv.writer(csv_file)
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
                                        #csv_file = open(current_date+'.csv','w+',newline = '')
                                        lnwriter = csv.writer(csv_file)
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
            time.sleep(delay_ms)
            # Exit loop if 'q' is pressed
            if key == ord('q'):
                break
        
        # Release handle to the webcam and close CSV file
        video_capture.release()
        csv_file.close()
        cv2.destroyAllWindows()
        f.close()

    pass

def signal_handler(sig, frame):
    global terminate_flag
    print("Termination signal received.")
    terminate_flag = True

def start_camera_processes():
    signal.signal(signal.SIGINT, signal_handler)
    processes = []
    p = Process(target=process_camera, args=(0,))
    p.start()
    processes.append(p)

    print('process started for camera 0')
    for p in processes:
        p.join()

def terminate_application():
    global terminate_flag
    print("Termination initiated by user.")
    terminate_flag = True

if __name__ == "__main__":
    start_camera_processes()
