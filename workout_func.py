import cv2
from tkinter import filedialog, messagebox
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import cv2
import mediapipe as mp

# Landmark indices
NOSE = 0

LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12

LEFT_ELBOW = 13
RIGHT_ELBOW = 14

LEFT_WRIST = 15
RIGHT_WRIST = 16

LEFT_HIP = 23
RIGHT_HIP = 24

LEFT_KNEE = 25
RIGHT_KNEE = 26

LEFT_ANKLE = 27
RIGHT_ANKLE = 28

#variables
# stageJJ = ""
# count_JJ = 0
# stagePushUp = ""
# count_PushUp = 0
# stageCurlUp = ""
# count_CurlUp = 0

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

def update_frame_workout(self, canvas):
    if self.cap:
        ret, frame = self.cap.read()
        
        if ret:
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(imgRGB)
            
            if results.pose_landmarks:
                mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            # Get Coordinates
            #CurlUp
            #PushUp
                nose = [results.pose_landmarks.landmark[NOSE].x, results.pose_landmarks.landmark[NOSE].y]
                wrist_left = [results.pose_landmarks.landmark[LEFT_WRIST].x, results.pose_landmarks.landmark[LEFT_WRIST].y]
                wrist_right = [results.pose_landmarks.landmark[RIGHT_WRIST].x, results.pose_landmarks.landmark[RIGHT_WRIST].y]
                #JJ
                shoulder_right = [results.pose_landmarks.landmark[RIGHT_SHOULDER].x, results.pose_landmarks.landmark[RIGHT_SHOULDER].y]
                shoulder_left = [results.pose_landmarks.landmark[LEFT_SHOULDER].x, results.pose_landmarks.landmark[LEFT_SHOULDER].y]
                hip_right = [results.pose_landmarks.landmark[RIGHT_HIP].x, results.pose_landmarks.landmark[RIGHT_HIP].y]
                hip_left = [results.pose_landmarks.landmark[LEFT_HIP].x, results.pose_landmarks.landmark[LEFT_HIP].y]
                elbow_right = [results.pose_landmarks.landmark[RIGHT_ELBOW].x, results.pose_landmarks.landmark[RIGHT_ELBOW].y]
                elbow_left = [results.pose_landmarks.landmark[LEFT_ELBOW].x, results.pose_landmarks.landmark[LEFT_ELBOW].y]
                knee_right = [results.pose_landmarks.landmark[RIGHT_KNEE].x, results.pose_landmarks.landmark[RIGHT_KNEE].y]
                knee_left = [results.pose_landmarks.landmark[LEFT_KNEE].x, results.pose_landmarks.landmark[LEFT_KNEE].y]
                
                # Calculate angle
                #PushUp
                angle_l_shoulderelbowwrist = calculate_angle(shoulder_left, elbow_left, wrist_left)
                angle_r_shoulderelbowwrist = calculate_angle(shoulder_right, elbow_right, wrist_right)
                avg_angle_shoulderelbowwrist = (angle_l_shoulderelbowwrist + angle_r_shoulderelbowwrist) / 2
                avg_elbow_y = (elbow_left[1] + elbow_right[1]) / 2
                #JJ
                angle_l_hipshoulderelbow = calculate_angle(hip_left, shoulder_left, elbow_left)
                angle_r_hipshoulderelbow = calculate_angle(hip_right, shoulder_right, elbow_right)
                avg_angle_hipshoulderelbow = (angle_l_hipshoulderelbow + angle_r_hipshoulderelbow) / 2
                
                angle_l_shoulderhipknee = calculate_angle(shoulder_left, hip_left, knee_left)
                angle_r_shoulderhipknee = calculate_angle(shoulder_right, hip_right, knee_right)
                avg_angle_shoulderhipknee = (angle_l_shoulderhipknee + angle_r_shoulderhipknee) / 2
                
                # Counter Logic
                #PushUp
                if avg_angle_shoulderelbowwrist < 70 and nose[1] > avg_elbow_y: 
                    if self.stagePushUp == "Up":
                        self.countPushUp += 1
                        self.stagePushUp = "Down"
                        update_count_exercise(self, "PushUp", self.countPushUp)
                if avg_angle_shoulderelbowwrist > 160 and nose[1] < avg_elbow_y:
                    self.stagePushUp = "Up"
                #JJ
                if avg_angle_hipshoulderelbow < 90 and avg_angle_shoulderhipknee > 170:
                    self.stageJJ = "Down"
 
                if avg_angle_hipshoulderelbow > 90 and avg_angle_shoulderhipknee < 170 and nose[1] > avg_elbow_y :
                    if self.stageJJ == "Down":
                        self.countJJ += 1
                        self.stageJJ = "Up"
                        update_count_exercise(self, "JumpingJack", self.countJJ)
            
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
    self.countJJ = 0
    self.countPushUp = 0
    self.countCurlUp = 0
    
    for label in self.exercise_labels:
        label = self.exercise_labels[label]
        label.config(text="0")
        
        
def update_count_exercise(self, exercise, count):
    label = self.exercise_labels[exercise]
    label.config(text=str(count))