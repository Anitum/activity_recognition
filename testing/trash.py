

import csv

# Function to write headers to CSV file without quotes
def write_headers_to_csv():

    
    with open('GuiApp/build/assets/crt_data/cam_selected.csv', mode='w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONE)
        writer.writerow(["Name", "Path"])

# Call the function to write headers
write_headers_to_csv()
