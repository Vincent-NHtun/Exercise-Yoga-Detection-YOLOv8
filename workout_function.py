import cv2
from tkinter import filedialog, messagebox
import tkinter as tk
from PIL import Image, ImageTk
from curlUp import curlUp
from jumpingJack import jumpingJack
from pushUp import pushUp
import numpy as np
import cv2
import mediapipe as mp

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
    
def calculate_angle(a, b, c):
    a = np.array(a)  
    b = np.array(b)  
    c = np.array(c)  

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle 
  
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

def get_pose_data(frame):
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
    return results

def classify_exercise(results):
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        # Landmarks
        shoulders = [(landmarks[i].x, landmarks[i].y) for i in [11, 12]]  # Left and Right shoulder
        elbows = [(landmarks[i].x, landmarks[i].y) for i in [13, 14]]  # Left and Right elbow
        wrists = [(landmarks[i].x, landmarks[i].y) for i in [15, 16]]  # Left and Right wrist
        hips = [(landmarks[i].x, landmarks[i].y) for i in [23, 24]]  # Left and Right hip
        knees = [(landmarks[i].x, landmarks[i].y) for i in [25, 26]]  # Left and Right knee

        # Calculate angles
        arm_angles = [calculate_angle(shoulders[i], elbows[i], wrists[i]) for i in range(2)]
        hip_knee_angles = [calculate_angle(hips[i], knees[i], (landmarks[27 + i].x, landmarks[27 + i].y)) for i in range(2)]

        avg_arm_angle = np.mean(arm_angles)
        avg_hip_knee_angle = np.mean(hip_knee_angles)

        # Classification based on angles
        if avg_arm_angle < 90 and avg_hip_knee_angle > 160:
            return "PushUp"
        elif avg_arm_angle > 160 and all(150 < angle < 180 for angle in hip_knee_angles):
            return "JumpingJack"
        elif 110 < avg_arm_angle < 160 and all(angle < 150 for angle in hip_knee_angles):
            return "CurlUp"

    return None


def update_frame_workout(self, canvas):
    if self.cap:
        ret, frame = self.cap.read()
        
        if ret:
            results = get_pose_data(frame)
            exercise_type = classify_exercise(results)
            # print(exercise_type)
            
            if exercise_type == "PushUp":
                frame, results, self.count, self.stage = pushUp(frame, results, self.count, self.stage)
                update_count_exercise(self, "PushUp", self.count)
                
            elif exercise_type == "CurlUp":
                frame, results, self.count, self.stage = curlUp(frame, results, self.count, self.stage)
                update_count_exercise(self, "CurlUp", self.count)
                
            elif exercise_type == "JumpingJack":
                frame, results, self.count, self.stage = jumpingJack(frame, results, self.count, self.stage)
                update_count_exercise(self, "JumpingJack", self.count)
            
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
        
        
def update_count_exercise(self, exercise, count):
    label = self.exercise_labels[exercise]
    label.config(text=str(count))