import cv2
from tkinter import filedialog, messagebox
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import cv2
import mediapipe as mp

# Landmark indices
NOSE = 0
LEFT_MOUTH = 9
RIGHT_MOUTH = 10
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

def upload_video_workout(self, canvas):
    # Upload a video and display it on the canvas
    video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
    if video_path:
        messagebox.showinfo("Video Upload", "Video uploaded successfully!")
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Could not open video file.")
            return
        self.detection_started = True
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
            
        self.detection_started = False
        self.selected_button.config(bg="SystemButtonFace")
        self.selected_button = None
    
def start_detection_workout(self, canvas):
    self.cap = cv2.VideoCapture(0)  # Open the default camera
    if not self.cap.isOpened():
        messagebox.showerror("Error", "Could not open video device.")
        return
    self.detection_started = True 
    self.update_frame_workout(canvas)
    self.selected_button.config(bg="SystemButtonFace")
    self.selected_button = None
    
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
                ankle_right = [results.pose_landmarks.landmark[RIGHT_ANKLE].x, results.pose_landmarks.landmark[RIGHT_ANKLE].y]
                ankle_left = [results.pose_landmarks.landmark[LEFT_ANKLE].x, results.pose_landmarks.landmark[LEFT_ANKLE].y]
                self.ankleRightX = results.pose_landmarks.landmark[RIGHT_ANKLE].x
                self.ankleLeftX = results.pose_landmarks.landmark[LEFT_ANKLE].x
            #PushUp
                self.nose = [results.pose_landmarks.landmark[NOSE].x, results.pose_landmarks.landmark[NOSE].y]
                self.mouth_left = [results.pose_landmarks.landmark[LEFT_MOUTH].x, results.pose_landmarks.landmark[LEFT_MOUTH].y]
                self.mouth_right = [results.pose_landmarks.landmark[RIGHT_MOUTH].x, results.pose_landmarks.landmark[RIGHT_MOUTH].y]
                self.wrist_left = [results.pose_landmarks.landmark[LEFT_WRIST].x, results.pose_landmarks.landmark[LEFT_WRIST].y]
                self.wrist_right = [results.pose_landmarks.landmark[RIGHT_WRIST].x, results.pose_landmarks.landmark[RIGHT_WRIST].y]
                
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
            #CurlUp
                angle_l_hipkneeankle = calculate_angle(hip_left, knee_left, ankle_left)
                angle_r_hipkneeankle = calculate_angle(hip_right, knee_right, ankle_right)
                self.avg_angle_hipkneeankle = (angle_l_hipkneeankle + angle_r_hipkneeankle) / 2
            #PushUp
                angle_l_shoulderelbowwrist = calculate_angle(shoulder_left, elbow_left, self.wrist_left)
                angle_r_shoulderelbowwrist = calculate_angle(shoulder_right, elbow_right, self.wrist_right)
                self.avg_angle_shoulderelbowwrist = (angle_l_shoulderelbowwrist + angle_r_shoulderelbowwrist) / 2
                self.avg_elbow_y = (elbow_left[1] + elbow_right[1]) / 2
            #JJ
                angle_l_hipshoulderelbow = calculate_angle(elbow_left, shoulder_left, hip_left)
                angle_r_hipshoulderelbow = calculate_angle(elbow_right, shoulder_right, hip_right)
                self.avg_angle_hipshoulderelbow = (angle_l_hipshoulderelbow + angle_r_hipshoulderelbow) / 2
                
                angle_l_shoulderhipknee = calculate_angle(shoulder_left, hip_left, knee_left)
                angle_r_shoulderhipknee = calculate_angle(shoulder_right, hip_right, knee_right)
                self.avg_angle_shoulderhipknee = (angle_l_shoulderhipknee + angle_r_shoulderhipknee) / 2

            frame = cv2.resize(frame, (canvas.winfo_width(), canvas.winfo_height()))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img_tk = ImageTk.PhotoImage(image=img)
                
            canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            canvas.image = img_tk  # Avoid garbage collection
                
            self.root.after(33, lambda: self.update_frame_workout(canvas))
        else:
            self.cap.release() 

def start_recursive_pose_click(self, pose_name):
    if not self.detection_started:
        print("Open the LIVE video feed or upload video to start detection.")
        return
    if self.current_pose != "":
        self.stop_recursive_pose_click()
    self.current_pose = pose_name
    self.recursive_call = True
    self.handle_pose_click(pose_name)
    
def stop_recursive_pose_click(self):
    self.recursive_call = False
    self.current_pose = ""
    
def handle_pose_click(self, pose_name):
    if not self.detection_started:
        print("Open the LIVE video feed or upload video to start detection.")
        return
    # Handle the pose click event
    if self.recursive_call and self.current_pose == pose_name: # to break the recursion when the user clicks on another pose
        
        print(f"Pose clicked: {pose_name}")
        
        #Squat
        if pose_name == "Squat":
            # print(f"countSquat: {self.countSquat}")
            # print(f"stageSquat: {self.stageSquat}")
            # print(f"avg_angle_hipkneeankle: {self.avg_angle_hipkneeankle}")
            if self.avg_angle_hipkneeankle > 150 and abs(self.ankleRightX - self.ankleLeftX) > 0.1:
                if self.stageSquat != "Up":
                    self.stageSquat = "Up"
            if (self.avg_angle_hipkneeankle < 150 and self.avg_angle_hipkneeankle > 45) and abs(self.ankleRightX - self.ankleLeftX) > 0.1:
                if self.stageSquat == "Up":
                    self.countSquat += 1
                    self.exercise_labels["Squat"].config(text=self.countSquat)
                    self.stageSquat = "Down"
                    
        #CurlUp
        if pose_name == "Curl Up":
            # print(f"stageCurlUp: {self.stageCurlUp}")
            # print(f"countCurlUp: {self.countCurlUp}")
            # print(f"avg_angle_hipkneeankle: {self.avg_angle_hipkneeankle}")
            # print(f"avg_angle_shoulderhipknee: {self.avg_angle_shoulderhipknee}")
            if (self.avg_angle_hipkneeankle > 30) and (self.avg_angle_hipkneeankle < 100):
                if (self.avg_angle_shoulderhipknee > 100) :
                        self.stageCurlUp = "Down"
                if ((self.avg_angle_shoulderhipknee < 50 and self.stageCurlUp == "Down")):
                    self.countCurlUp += 1
                    self.stageCurlUp = "Up"
                    self.exercise_labels["CurlUp"].config(text=self.countCurlUp)
        #PushUp   
        if pose_name == "Push Up":
            # print(f"stagePushUp: {self.stagePushUp}")
            # print(f"countPushUp: {self.countPushUp}")
            # print(f"avg_angle_shoulderelbowwrist: {self.avg_angle_shoulderelbowwrist}")
            # print(f"avg_elbow_y: {self.avg_elbow_y}")
            if self.avg_angle_shoulderelbowwrist < 70 and ( self.nose[1] > self.avg_elbow_y or self.nose[1] > self.mouth_left[1] or self.nose[1] > self.mouth_left[1]): 
                self.stagePushUp = "Down"
            if self.avg_angle_shoulderelbowwrist > 160 and ( self.nose[1] < self.avg_elbow_y or self.nose[1] < self.mouth_right[1] or self.nose[1] < self.mouth_right[1]):
                if self.stagePushUp == "Down":
                    self.countPushUp += 1
                    self.stagePushUp = "Up"
                    self.exercise_labels["PushUp"].config(text=self.countPushUp)
        #JJ
        if pose_name == "Jumping Jack":
            # print(f"stageJJ: {self.stageJJ}")
            # print(f"countJJ: {self.countJJ}")
            # print(f"avg_angle_hipshoulderelbow: {self.avg_angle_hipshoulderelbow}")
            # print(f"avg_angle_shoulderhipknee: {self.avg_angle_shoulderhipknee}")
            if self.avg_angle_hipshoulderelbow < 90 and self.avg_angle_shoulderhipknee > 170:
                self.stageJJ = "Down"
            if self.avg_angle_hipshoulderelbow > 90 and self.avg_angle_shoulderhipknee < 170 and (self.nose[1] > self.wrist_left[1] or self.nose[1] > self.wrist_right[1]):
                if self.stageJJ == "Down":
                    self.countJJ += 1
                    self.exercise_labels["JumpingJack"].config(text=self.countJJ)
                    self.stageJJ = "Up"

        self.root.after(33, lambda: self.handle_pose_click(pose_name))

def reset_count_exercise(self):
    self.countJJ = 0
    self.countPushUp = 0
    self.countCurlUp = 0
    self.countSquat = 0
    
    for label in self.exercise_labels:
        label = self.exercise_labels[label]
        label.config(text="0")
        