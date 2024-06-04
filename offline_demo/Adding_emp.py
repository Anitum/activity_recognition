import tkinter as tk
from PIL import Image, ImageTk
import cv2
import csv
import time
import threading
import os

"""

ERROR:
invalid command name "131383654270784update_frame"
    while executing
"131383654270784update_frame"
    ("after" script)
      
WHILE CLOSING 

"""


class MyVideoCapture:

    def __init__(self, video_source=0, width=None, height=None, fps=None):
    
        self.video_source = video_source
        self.width = width
        self.height = height
        self.fps = fps
        
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("[MyVideoCapture] Unable to open video source", video_source)

        # Get video source width and height
        if not self.width:
            self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))    # convert float to int
        if not self.height:
            self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))  # convert float to int
        if not self.fps:
            self.fps = int(self.vid.get(cv2.CAP_PROP_FPS))  # convert float to int

        # default value at start        
        self.ret = False
        self.frame = None

        # start thread
        self.running = True
        self.thread = threading.Thread(target=self.process)
        self.thread.start()
        
    def process(self):
        while self.running:
            if not self.running:
                break
            ret, frame = self.vid.read()
            
            if ret:
                # process image
                frame = cv2.resize(frame, (self.width, self.height))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                print('[MyVideoCapture] stream end:', self.video_source)
                # TODO: reopen stream
                self.running = False
                break
                
            # assign new frame
            self.ret = ret
            self.frame = frame
            
            # sleep for next frame
            time.sleep(1/self.fps)
            # break the loop is object is destroyed
        
    def get_frame(self):
        return self.ret, self.frame
    
    # Release the video source when the object is destroyed
    def __del__(self):
        # stop thread
        if self.running:
            self.running = False
            self.thread.join()

        # relase stream
        if self.vid.isOpened():
            self.vid.release()
            
 
class tkCamera(tk.Frame):

    def __init__(self, root, text="", video_source=0, width=None, height=None, source=None):
        super().__init__(root)
        
        self.root = root
        
        #self.root.title(root_title)
        self.video_source = video_source
        self.vid = MyVideoCapture(self.video_source, width, height)

        self.label = tk.Label(self, text=text)
        self.label.pack()
        
        self.canvas = tk.Canvas(self, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        self.btn_snapshot = tk.Button(self, text="Start", command=self.start)
        self.btn_snapshot.pack(anchor='center', side='left')
        
        self.btn_snapshot = tk.Button(self, text="Stop", command=self.stop)
        self.btn_snapshot.pack(anchor='center', side='left')
         
        # Button that lets the user take a snapshot
        self.btn_snapshot = tk.Button(self, text="Select", command=lambda: self.select(source))
        self.btn_snapshot.pack(anchor='center', side='left')
         
        # After it is called once, the update method will be automatically called every delay milliseconds
        # calculate delay using `FPS`
        self.delay = int(1000/self.vid.fps)

        print('[tkCamera] source:', self.video_source)
        print('[tkCamera] fps:', self.vid.fps, 'delay:', self.delay)
        
        self.image = None
        
        self.running = True
        self.update_frame()

    def start(self):
        if not self.running:
            self.running = True
            self.update_frame()

    def stop(self):
        if self.running:
           self.running = False
    
    def select(self,sour):
        print('Select {source}'.format(source=sour))
        # just append to the file 
        
        with open('offline_demo/assets/crt_data/cam_selected.csv', 'a') as file:
            name , path = sour
            writer = csv.writer(file)
            writer.writerow([name, path])
        
    def __del__(self):
        print('[tkCamera] stoping threads')
        self.running = False
        # stop update_frame
        self.update_frame()
        # stop MyVideoCapture
        self.vid.__del__()

            
    def update_frame(self):
        # widgets in tkinter already have method `update()` so I have to use different name -
        if not self.running:
            return

        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        
        if ret:
            self.image = Image.fromarray(frame)
            self.photo = ImageTk.PhotoImage(image=self.image)
            self.canvas.create_image(0, 0, image=self.photo, anchor='nw')
        
        if self.running:
            self.root.after(self.delay, self.update_frame)


class Adding_emp:

    def __init__(self, sources):
        self.selected = []
        
        # Read if there are already cam listed in the file if file not found or it is empty the write fiel 

        self.file_name = 'offline_demo/assets/crt_data/cam_selected.csv'
        
        # Check if the file exists
        if os.path.exists(self.file_name):
            self.read_existing_data()
        else:   
            self.write_headers_to_csv()


        self.root = tk.Tk()
        root_title = ("Adding employ")

         
        self.root.title(root_title)

        # dividing root in 4 x 1 grid
        self.root.grid_rowconfigure([0, 1, 2, 3, 4], weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # importing logo image
        self.logo = Image.open("offline_demo/assets/Logo.png")
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
        # this should just big enough to fit the logo
        self.logo_label.config(width=50, height=10)

        # making a label for contact us texr
        self.Running_txt = tk.Label(self.frame0, text="Adding Employ", font=("Arial", 16), padx=10, pady=10, justify="center")
        self.Running_txt.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        #making frame for 1 row 

        # making a frame for 0 th row
        self.frame1 = tk.Frame(self.root)
        self.frame1.grid(row=0, column=0, sticky="nsew")

        # dividing frame0 in 1 x 2 grid
        self.frame1.grid_rowconfigure([0,1], weight=1)
        self.frame1.grid_columnconfigure(0, weight=1)

        # adding lable 
        self.emp_name = tk.Label(self.frame0, image=self.logo)
        




        # video_sources = sources
        # self.root.title(root_title)
        
        # self.vids = []

        # columns = 2
        # for number, source in enumerate(video_sources):
        #     text, stream = source
        #     vid = tkCamera(self.root, text, stream, 400, 300,source)
        #     x = number % columns
        #     y = number // columns
        #     vid.grid(row=y+1, column=x)
        #     self.vids.append(vid)
        
        # #if i close the window it kills the threads and with ctrl+c it kills the threads and also if next or back button is pressed
        # self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        # self.root.bind("<Control-q>", self.on_closing)
        # self.root.bind("<Control-c>", self.on_closing)
        
        
        # self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        # self.root.bind("<Control-q>", self.on_closing)

        # self.lastrow = len(video_sources)+2

        # # adding next and previous button
        # self.next_btn = tk.Button(self.root, text="Next", command=self.next)
        # self.next_btn.grid(row=self.lastrow, column=0, sticky="nsew")
        # self.back_btn = tk.Button(self.root, text="Back", command=self.back)
        # self.back_btn.grid(row=self.lastrow, column=1, sticky="nsew")
    
    def next(self):
        # first check if something is selected or not 
        with open('offline_demo/assets/crt_data/cam_selected.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                self.selected.append(row)
        if len(self.selected) == 0:
            print('Please select atleast one camera feed')
            label = tk.Label(self.root, text="Please select atleast one camera feed", font=("Arial", 12), padx=10, pady=10, justify="center")
            label.grid(row=self.lastrow+1, column=0, columnspan=2, sticky="nsew")
    
        else:
            self.on_closing()
            import Running
            Run = Running.Running()
            Run.root.mainloop()



    
    def back(self):

        import term_and_condition
        self.on_closing()
        term = term_and_condition.tnc()
        term.root.mainloop()
        
        
    
    def on_closing(self, event=None):
        print('[App] stoping threads')
        for source in self.vids:
            source.vid.running = False
            source.vid.thread.join()
            source.vid.__del__()
        
    
        print('[App] exit')
        self.root.destroy()
    # Function to read existing data from CSV file
        
    def read_existing_data(self):
        with open(self.file_name, mode='r') as file:
            # if file have more than one line 
         
            reader = csv.reader(file)
            try:
                next(reader)  # Skip header row
                for row in reader:
                    self.selected.append((row[0], row[1]))
            except:
                self.write_headers_to_csv()


    # Call the function to write headers
    def write_headers_to_csv(self):
        with open(self.file_name, mode='w', newline='') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_NONE)
            writer.writerow(["Name", "Path"])
            

if __name__ == '__main__':     

        

    sources = []
    with open('offline_demo/assets/crt_data/cam_selected.csv', 'r') as file:
        # if file have more than one line
        reader = csv.reader(file)
        try:

            next(reader)  # Skip header row
            for row in reader:
                try:
                    row[1] = int(row[1])
                    sources.append((row[0], row[1]))
                except:
                    sources.append((row[0], row[1]))
        except:
            sources.append(('me', 0))
            print(1)


    print(sources)
      
    a = Adding_emp(sources)
    a.root.mainloop()
