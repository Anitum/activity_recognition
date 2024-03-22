import csv
import os
from datetime import datetime


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

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
csv_file = current_date + '.csv'

Downloaded_Attendance_path = r"D:\face_rec\Downloaded_Attendance.csv"
copy_csv_to_bigger_file(source_csv = csv_file , target_csv=Downloaded_Attendance_path)
