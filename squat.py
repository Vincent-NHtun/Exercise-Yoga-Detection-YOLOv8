import cv2
import mediapipe as mp
import numpy as np

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

cap = cv2.VideoCapture(0)
count = 0
stage = None

# Function to calculate angle between three points
def calculate_angle(a, b, c):
    a = np.array(a)  
    b = np.array(b)  
    c = np.array(c)  
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle    

def squat(frame, count, stage):
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)

    if results.pose_landmarks:
        mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        landmarks = results.pose_landmarks.landmark

        # Define landmark positions for both views
        hip_left = [landmarks[mpPose.PoseLandmark.LEFT_HIP.value].x, landmarks[mpPose.PoseLandmark.LEFT_HIP.value].y]
        knee_left = [landmarks[mpPose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mpPose.PoseLandmark.LEFT_KNEE.value].y]
        ankle_left = [landmarks[mpPose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mpPose.PoseLandmark.LEFT_ANKLE.value].y]
        hip_right = [landmarks[mpPose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mpPose.PoseLandmark.RIGHT_HIP.value].y]
        knee_right = [landmarks[mpPose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mpPose.PoseLandmark.RIGHT_KNEE.value].y]
        ankle_right = [landmarks[mpPose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mpPose.PoseLandmark.RIGHT_ANKLE.value].y]

        # Calculate angles for both sides
        angle_left_kneehipankle = calculate_angle(hip_left, knee_left, ankle_left)
        angle_right_kneehipankle = calculate_angle(hip_right, knee_right, ankle_right)

        # Apply different logic based on the view
        # Side view logic
        # if angle_left_kneehipankle < 90 and angle_right_kneehipankle < 90:
        #     stage = "Down"
        # elif angle_left_kneehipankle > 160 and angle_right_kneehipankle > 160 and stage == "Down":
        #     count += 1
        #     stage = "Up"
            
        # Front view logic
        if angle_left_kneehipankle < 160 and angle_right_kneehipankle < 160:
            if stage != "Down":
                stage = "Down"
        elif angle_left_kneehipankle > 170 and angle_right_kneehipankle > 170 and stage == "Down":
            count += 1
            stage = "Up"
        
        # Display squat count
        #cv2.putText(frame, f'Squats: {count}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3, cv2.LINE_AA)

    return frame, count, stage