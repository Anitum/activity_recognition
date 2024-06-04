import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
import threading
import tkinter as tk
from PIL import Image, ImageTk


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
            
 
class tkCamera(tkinter.Frame):

    def __init__(self, root, text="", video_source=0, width=None, height=None):
        super().__init__(root)
        
        self.root = root
        
        #self.root.title(root_title)
        self.video_source = video_source
        self.vid = MyVideoCapture(self.video_source, width, height)

        self.label = tkinter.Label(self, text=text)
        self.label.pack()
        
        self.canvas = tkinter.Canvas(self, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        self.btn_snapshot = tkinter.Button(self, text="Start", command=self.start)
        self.btn_snapshot.pack(anchor='center', side='left')
        
        self.btn_snapshot = tkinter.Button(self, text="Stop", command=self.stop)
        self.btn_snapshot.pack(anchor='center', side='left')
         
        # Button that lets the user take a snapshot
        self.btn_snapshot = tkinter.Button(self, text="Snapshot", command=self.snapshot)
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
    
    def snapshot(self):
        # Get a frame from the video source
        #ret, frame = self.vid.get_frame()
        #if ret:
        #    cv2.imwrite(time.strftime("frame-%d-%m-%Y-%H-%M-%S.jpg"), cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR))
        
        # Save current frame in widget - not get new one from camera - so it can save correct image when it stoped
        if self.image:
            self.image.save(time.strftime("frame-%d-%m-%Y-%H-%M-%S.jpg"))
            
    def update_frame(self):
        # widgets in tkinter already have method `update()` so I have to use different name -

        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        
        if ret:
            self.image = PIL.Image.fromarray(frame)
            self.photo = PIL.ImageTk.PhotoImage(image=self.image)
            self.canvas.create_image(0, 0, image=self.photo, anchor='nw')
        
        if self.running:
            self.root.after(self.delay, self.update_frame)


class App:

    def __init__(self, sources):
        self.root = tkinter.Tk()
        root_title = ("Tkinter and OpenCV")

         
        self.root.title(root_title)

        # dividing root in 3 x 1 grid
        self.root.grid_rowconfigure([0, 1, 2], weight=1)
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
        self.Running_txt = tk.Label(self.frame0, text="Select the Camera feed", font=("Arial", 16), padx=10, pady=10, justify="center")
        self.Running_txt.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)



        video_sources = sources
        self.root.title(root_title)
        
        self.vids = []

        columns = 2
        for number, source in enumerate(video_sources):
            text, stream = source
            vid = tkCamera(self.root, text, stream, 400, 300)
            x = number % columns
            y = number // columns
            vid.grid(row=y+1, column=x)
            self.vids.append(vid)
        
        self.root.protocol("WM_DELETE_root", self.on_closing)
        
    
    def on_closing(self, event=None):
        print('[App] stoping threads')
        for source in self.vids:
            source.vid.running = False
        print('[App] exit')
        self.root.destroy()

if __name__ == '__main__':     

        
    # Create a root and pass it to the Application object
   
    sources = [
        ('me', 0), 
        # ('Zakopane, Poland', 'https://imageserver.webcamera.pl/rec/krupowki-srodek/latest.mp4'),
        # ('Kraków, Poland', 'https://imageserver.webcamera.pl/rec/krakow4/latest.mp4'),
        # ('Warszawa, Poland', 'https://imageserver.webcamera.pl/rec/warszawa/latest.mp4'),
        # ('Baltic See, Poland', 'https://imageserver.webcamera.pl/rec/chlopy/latest.mp4'),
        # ('Mountains, Poland', 'https://imageserver.webcamera.pl/rec/skolnity/latest.mp4'),
    ]
    print(sources)
      
    a = App(sources)
    a.root.mainloop()
