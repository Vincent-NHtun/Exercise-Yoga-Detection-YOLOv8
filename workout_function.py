import cv2
from tkinter import filedialog, messagebox
import tkinter as tk
from PIL import Image, ImageTk
from curlUp import curlUp
from jumpingJack import jumpingJack
from squat import squat

def upload_video_workout(self, canvas):
    # Upload a video and display it on the canvas
    video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
    if video_path:
        messagebox.showinfo("Video Upload", "Video uploaded successfully!")
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Could not open video file.")
            return

        self.update_frame_workout(canvas)  # Start updating frames on the canvas

def stop_detection_workout(self, canvas=None):
        # Stop the frame update thread 
        if hasattr(self, 'stop_event'):
            self.stop_event.set()
            self.thread.join()
            
        if self.cap and self.cap.isOpened():
            self.cap.release()
            self.cap = None    
            
        if canvas:
            canvas.create_image(0, 0, anchor=tk.NW, image=self.default_image)
            canvas.image = self.default_image

def start_detection_workout(self, canvas):
    self.cap = cv2.VideoCapture(0)  # Open the default camera
    if not self.cap.isOpened():
        messagebox.showerror("Error", "Could not open video device.")
        return
    
    self.update_frame_workout(canvas)

def update_frame_workout(self, canvas):
    if self.cap:
        ret, frame = self.cap.read()
        if ret:
            # frame, self.count, self.stage = curlUp(frame, self.count, self.stage)
            # labelCurlUp = self.exercise_labels["CurlUp"]
            # labelCurlUp.config(text=self.count)
            
            # frame, self.count, self.stage = jumpingJack(frame, self.count, self.stage)
            # labelJumpingJack = self.exercise_labels["JumpingJack"]
            # labelJumpingJack.config(text=self.count)
            
            frame, self.count, self.stage = squat(frame, self.count, self.stage)
            labelSquat = self.exercise_labels["Squat"]
            labelSquat.config(text=self.count)
            
            frame = cv2.resize(frame, (canvas.winfo_width(), canvas.winfo_height()))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img_tk = ImageTk.PhotoImage(image=img)
                
            canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            canvas.image = img_tk  # Avoid garbage collection
                
            self.root.after(33, lambda: self.update_frame_workout(canvas))
        else:
            self.cap.release() 
            
def reset_count_exercise(self):
    self.count = 0
    
    for label in self.exercise_labels:
        label = self.exercise_labels[label]
        label.config(text="0")