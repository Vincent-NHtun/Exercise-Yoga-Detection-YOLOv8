import cv2
import mediapipe as mp
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

NOSE = 0

def calculate_angle(a, b, c):
    a = np.array(a)  
    b = np.array(b)  
    c = np.array(c)  

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle    

def pushup(frame, results, count, stage):
    print("pushup")
    # imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # results = pose.process(imgRGB)

    if results.pose_landmarks:
        # mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        nose = [results.pose_landmarks.landmark[0].x, results.pose_landmarks.landmark[0].y]
        shoulder_right = [results.pose_landmarks.landmark[RIGHT_SHOULDER].x, results.pose_landmarks.landmark[RIGHT_SHOULDER].y]
        shoulder_left = [results.pose_landmarks.landmark[LEFT_SHOULDER].x, results.pose_landmarks.landmark[LEFT_SHOULDER].y]
        elbow_left = [results.pose_landmarks.landmark[LEFT_ELBOW].x, results.pose_landmarks.landmark[LEFT_ELBOW].y]
        elbow_right = [results.pose_landmarks.landmark[RIGHT_ELBOW].x, results.pose_landmarks.landmark[RIGHT_ELBOW].y]
        wrist_left = [results.pose_landmarks.landmark[LEFT_WRIST].x, results.pose_landmarks.landmark[LEFT_WRIST].y]
        wrist_right = [results.pose_landmarks.landmark[RIGHT_WRIST].x, results.pose_landmarks.landmark[RIGHT_WRIST].y]
        hip_right = [results.pose_landmarks.landmark[RIGHT_HIP].x, results.pose_landmarks.landmark[RIGHT_HIP].y]
        hip_left = [results.pose_landmarks.landmark[LEFT_HIP].x, results.pose_landmarks.landmark[LEFT_HIP].y]
        knee_right = [results.pose_landmarks.landmark[RIGHT_KNEE].x, results.pose_landmarks.landmark[RIGHT_KNEE].y]
        knee_left = [results.pose_landmarks.landmark[LEFT_KNEE].x, results.pose_landmarks.landmark[LEFT_KNEE].y]
        ankel_right = [results.pose_landmarks.landmark[RIGHT_ANKLE].x, results.pose_landmarks.landmark[RIGHT_ANKLE].y]
        ankel_left = [results.pose_landmarks.landmark[LEFT_ANKLE].x, results.pose_landmarks.landmark[LEFT_ANKLE].y]

        #calculating angles
        left_arm_angle = calculate_angle(shoulder_left, elbow_left, wrist_left)
        right_arm_angle = calculate_angle(shoulder_right, elbow_right, wrist_right)
        avg_arm_angle = (left_arm_angle + right_arm_angle) / 2
        avg_elbow_y = (elbow_left[1] + elbow_right[1]) / 2

        if stage:
            if (avg_arm_angle < 70) & (nose[1] > avg_elbow_y): 
                count += 1
                stage = False
        else:
            if (avg_arm_angle > 160) & (nose[1] < avg_elbow_y):
                stage = True
                
        print(count)
    return frame,count,stage

def curlup(frame, results, count, stage):
    print("curlup")
    # imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # results = pose.process(imgRGB)

    if results.pose_landmarks:
        # mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        shoulder_right = [results.pose_landmarks.landmark[RIGHT_SHOULDER].x, results.pose_landmarks.landmark[RIGHT_SHOULDER].y]
        shoulder_left = [results.pose_landmarks.landmark[LEFT_SHOULDER].x, results.pose_landmarks.landmark[LEFT_SHOULDER].y]
        hip_right = [results.pose_landmarks.landmark[RIGHT_HIP].x, results.pose_landmarks.landmark[RIGHT_HIP].y]
        hip_left = [results.pose_landmarks.landmark[LEFT_HIP].x, results.pose_landmarks.landmark[LEFT_HIP].y]
        knee_right = [results.pose_landmarks.landmark[RIGHT_KNEE].x, results.pose_landmarks.landmark[RIGHT_KNEE].y]
        knee_left = [results.pose_landmarks.landmark[LEFT_KNEE].x, results.pose_landmarks.landmark[LEFT_KNEE].y]
        ankel_right = [results.pose_landmarks.landmark[RIGHT_ANKLE].x, results.pose_landmarks.landmark[RIGHT_ANKLE].y]
        ankel_left = [results.pose_landmarks.landmark[LEFT_ANKLE].x, results.pose_landmarks.landmark[LEFT_ANKLE].y]

        angle_left = calculate_angle(shoulder_left, hip_left, knee_left)
        angle_right = calculate_angle(shoulder_right, hip_right, knee_right)
        
        angle_left_hipankle = calculate_angle(hip_left, knee_left, ankel_left)
        angle_right_hipankle = calculate_angle(hip_right, knee_right, ankel_right)
        # print(angle_left_hipankle, angle_right_hipankle)
        
        if (angle_left_hipankle > 40 or angle_right_hipankle > 40) and (angle_left_hipankle < 80 or angle_right_hipankle < 80):
            if (angle_left > 110 or angle_right > 110) :
                    stage = "Down"
            if ((angle_left < 50 and stage == "Down") or (angle_right < 50 and stage == "Down")):
                count += 1
                stage = "Up"  
                
            # print(count)
            cv2.putText(frame, f'Sit-ups: {count}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3, cv2.LINE_AA)

    return frame, count, stage






