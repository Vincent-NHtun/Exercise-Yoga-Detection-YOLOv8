import cv2
# import mediapipe as mp
import numpy as np

# mpDraw = mp.solutions.drawing_utils
# mpPose = mp.solutions.pose
# pose = mpPose.Pose()

# cap = cv2.VideoCapture(0)
count = 0
stage = None

# Landmark indices
LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12

LEFT_HIP = 23
RIGHT_HIP = 24

LEFT_ELBOW = 13
RIGHT_ELBOW = 14

LEFT_KNEE = 25
RIGHT_KNEE = 26

def calculate_angle(a, b, c):
    a = np.array(a)  
    b = np.array(b)  
    c = np.array(c)  

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle    

def jumpingJack(frame, results, count, stage):
    # imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # results = pose.process(imgRGB)

    if results.pose_landmarks:
        # Render Detection
        # mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        
        # Get Coordinates
        shoulder_right = [results.pose_landmarks.landmark[RIGHT_SHOULDER].x, results.pose_landmarks.landmark[RIGHT_SHOULDER].y]
        shoulder_left = [results.pose_landmarks.landmark[LEFT_SHOULDER].x, results.pose_landmarks.landmark[LEFT_SHOULDER].y]
        hip_right = [results.pose_landmarks.landmark[RIGHT_HIP].x, results.pose_landmarks.landmark[RIGHT_HIP].y]
        hip_left = [results.pose_landmarks.landmark[LEFT_HIP].x, results.pose_landmarks.landmark[LEFT_HIP].y]
        elbow_right = [results.pose_landmarks.landmark[RIGHT_ELBOW].x, results.pose_landmarks.landmark[RIGHT_ELBOW].y]
        elbow_left = [results.pose_landmarks.landmark[LEFT_ELBOW].x, results.pose_landmarks.landmark[LEFT_ELBOW].y]
        knee_right = [results.pose_landmarks.landmark[RIGHT_KNEE].x, results.pose_landmarks.landmark[RIGHT_KNEE].y]
        knee_left = [results.pose_landmarks.landmark[LEFT_KNEE].x, results.pose_landmarks.landmark[LEFT_KNEE].y]

        # Calculate angle
        angle_left_hipshoulderelbow = calculate_angle(hip_left, shoulder_left, elbow_left)
        angle_right_hipshoulderelbow = calculate_angle(hip_right, shoulder_right, elbow_right)
        
        angle_left_shoulderhipknee = calculate_angle(shoulder_left, hip_left, knee_left)
        angle_right_shoulderhipknee = calculate_angle(shoulder_right, hip_right, knee_right)

        # Counter Logic
        if angle_left_hipshoulderelbow < 90 and angle_right_hipshoulderelbow < 90 and angle_left_shoulderhipknee > 170 and angle_right_shoulderhipknee > 170 :
            if stage == "Up":
                stage = "Down"
                count += 1
        if angle_left_hipshoulderelbow > 90 and angle_right_hipshoulderelbow > 90 and angle_left_shoulderhipknee < 170 and angle_right_shoulderhipknee < 170 :
            stage = "Up"  
                
            # print(count)
            # cv2.putText(frame, f'Sit-ups: {count}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3, cv2.LINE_AA)

    return frame, count, stage

