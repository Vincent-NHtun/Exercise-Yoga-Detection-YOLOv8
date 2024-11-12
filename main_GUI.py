import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from ultralytics import YOLO
from yoga_function import upload_video_yoga, start_detection_yoga, update_frame_yoga, stop_detection_yoga, process_pose_detection, process_animal_detection, process_pose_detection, start_pose_timer, update_timer_in_gui, stop_pose_timer, reset_count_yoga
from  workout_func import upload_video_workout, start_detection_workout, stop_detection_workout, update_frame_workout, reset_count_exercise, start_recursive_pose_click, handle_pose_click, stop_recursive_pose_click

class WorkoutTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Track Your Workout using YOLOv8")
        self.root.geometry("800x600")
        self.default_image = ImageTk.PhotoImage(Image.open("./images/cover.jpg").resize((650, 420)))
        
        self.current_pose = ""
        self.detection_started = False
        self.recursive_call = False
        
        self.stageJJ = ""
        self.stagePushUp = ""
        self.stageCurlUp = ""
        
        self.countPushUp = 0
        self.countJJ = 0
        self.countCurlUp = 0
        self.countSquat = 0
        
        self.nose = 0
        self.wrist_left= 0
        self.wrist_right = 0
        self.avg_angle_shoulderelbowwrist = 0
        self.avg_elbow_y = 0
        self.avg_angle_shoulderhipknee = 0
        self.avg_angle_hipshoulderelbow = 0
        self.avg_angle_hipkneeankle = 0
        
        self.class_labels = {
                    0: "Child",
                    1: "Easy Seat",
                    2: "Tree",
                    3: "Triangle",
                    4: "No Pose"
                }
        self.animals_class_labels = {
                    15: "cat",
                    16: "dog"
                }
        self.pose_start_time = {}  # To store the start time of each detected pose
        # self.pose_durations = {pose: 0 for pose in self.class_labels.values()}  # To store cumulative time of each pose
        self.exercise_count = {"Push Up": 0, "Curl Up": 0, "Jumping Jack": 0, "Squat": 0}

        self.style = ttk.Style()
        self.style.configure('TNotebook.Tab', padding=[50, 5], font=('Helvetica', 12))

        # Create Tab Control
        self.tab_control = ttk.Notebook(self.root)
        
        # Create two tabs
        self.workOutTab = ttk.Frame(self.tab_control)
        self.yogaTab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.workOutTab, text='Workout Tracker')
        self.tab_control.add(self.yogaTab, text='Yoga Detection')

        self.tab_control.pack(expand=1, fill="both")
        self.pose_durations = {pose: 0 for pose in self.class_labels.values()}

        self.create_workOutTab()
        self.create_yogaTab()
        
        # Load YOLOv8 model
        self.model = YOLO("./models/best.pt", task="pose")
        self.detect_model = YOLO("yolov8s.pt", task='detect')

        self.cap = None
        self.count = 0
        self.stage = None

        # For Yoga
        self.upload_video_yoga = upload_video_yoga.__get__(self)
        self.start_detection_yoga = start_detection_yoga.__get__(self)
        self.update_frame_yoga = update_frame_yoga.__get__(self)
        self.stop_detection_yoga = stop_detection_yoga.__get__(self)
        self.process_pose_detection = process_pose_detection.__get__(self)
        self.process_animal_detection = process_animal_detection.__get__(self)
        self.process_pose_detection = process_pose_detection.__get__(self)
        self.start_pose_timer = start_pose_timer.__get__(self)
        self.update_timer_in_gui = update_timer_in_gui.__get__(self)
        self.stop_pose_timer = stop_pose_timer.__get__(self)
        self.reset_count_yoga = reset_count_yoga.__get__(self)
        
        # For Workout
        self.upload_video_workout = upload_video_workout.__get__(self)
        self.start_detection_workout = start_detection_workout.__get__(self)
        self.stop_detection_workout = stop_detection_workout.__get__(self)
        self.update_frame_workout = update_frame_workout.__get__(self) 
        self.reset_count_exercise = reset_count_exercise.__get__(self) 
        self.start_recursive_pose_click = start_recursive_pose_click.__get__(self)
        self.stop_recursive_pose_click = stop_recursive_pose_click.__get__(self)
        self.handle_pose_click = handle_pose_click.__get__(self)

        
    #------------------------WORKOUT SECTION------------------------  
    def create_workOutTab(self):
        title_label = tk.Label(self.workOutTab, text="Track Your Workout using YOLOv8", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=10)

        # Create a frame for the left side (canvas, button, and label)
        left_frame = tk.Frame(self.workOutTab)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=20, pady=30)

        # Create a frame for the right side (pose buttons)
        right_frame = tk.Frame(self.workOutTab)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        #------------------------LEFT SIDE CONTENT------------------------
        self.exercise_canvas = tk.Canvas(left_frame, width=650, height=420, bg="gray")
        self.exercise_canvas.pack(pady=10)

        self.exercise_canvas.create_image(0, 0, anchor=tk.NW, image=self.default_image)

        camera_image = Image.open("./images/Livelogo.jpg").resize((30, 20))  
        camera_logo1 = ImageTk.PhotoImage(camera_image)
        self.camera_logo1 = camera_logo1

        button_frame1 = tk.Frame(left_frame)
        button_frame1.pack(pady=10)
        
        start_btn = tk.Button(button_frame1, text="  Live Detection", command=lambda: self.start_detection_workout(self.exercise_canvas), 
                      font=("Helvetica", 14, "bold"), bg="white", foreground="red", 
                      image=camera_logo1, compound=tk.LEFT) 
        start_btn.pack(side=tk.LEFT, padx=5)

        stop_btn = tk.Button(button_frame1, text="CLOSE", command=lambda: self.stop_detection_workout(self.exercise_canvas), 
                    font=("Helvetica", 12,"bold"), bg="white", foreground="darkblue")
        stop_btn.pack(side=tk.LEFT, padx=40)

        upload_btn = tk.Button(left_frame, text="Upload Videos", command=lambda:self.upload_video_workout(self.exercise_canvas), font=("Helvetica", 12), width=15, height=1)
        upload_btn.pack(pady=10)
        
        #------------------------RIGHT SIDE CONTENT------------------------
        poses_label = tk.Label(right_frame, text="Exercises Rep Count Available:", font=("Helvetica", 14))
        poses_label.grid(row=0, column=0, columnspan=4, pady=(30, 10))  # Reduced vertical padding

        self.exercise_images = {
            "Push Up": ImageTk.PhotoImage(Image.open("./images/pushup.jpg").resize((130, 130))),
            "Curl Up": ImageTk.PhotoImage(Image.open("./images/curlup.jpg").resize((130, 130))),
            "Jumping Jack": ImageTk.PhotoImage(Image.open("./images/jumpingjack.jpg").resize((130, 130))),
            "Squat": ImageTk.PhotoImage(Image.open("./images/squat.jpg").resize((130, 130)))
        }

        self.pose_buttons = {}
        col = 0
        for pose_name, img in self.exercise_images.items():
            btn = tk.Button(right_frame, text=pose_name, image=img, compound=tk.TOP, font=("Helvetica", 12),
                    command=lambda pose=pose_name: self.start_recursive_pose_click(pose))
            btn.grid(row=1, column=col, padx=10, pady=5)
            self.pose_buttons[pose_name] = btn
            col += 1

        # Alert Animal Detection
        alert_image = Image.open("./images/alert.png").resize((30, 30))  # Assuming you have an alert.jpg image
        alert_logo = ImageTk.PhotoImage(alert_image)
        self.alert_logo = alert_logo  # Keep a reference to avoid garbage collection

        self.animal_status_label = tk.Label(right_frame, text="", font=("Helvetica", 16, "bold"), fg="red", image=alert_logo, compound=tk.LEFT)
        self.animal_status_label.grid(row=2, column=0, columnspan=4, pady=(0, 0))
        self.animal_status_label.grid_remove()  # Hide initially
        
        #blank label
        self.blank_label = tk.Label(right_frame, text="", font=("Helvetica", 16, "bold"), fg="red") 
        self.blank_label.grid(row=3, column=0, columnspan=4, pady=(0, 0))
        
        # Define each row explicitly for each pose
        self.exercise_labels = {}  # Dictionary to store the timer label for each pose

        # Row for Push Up
        labelPushUpName = tk.Label(right_frame, text="Push Up: ", font=("Helvetica", 14), fg="green")
        labelPushUpCount = tk.Label(right_frame, text="0", font=("Helvetica", 14), fg="green")
        labelPushUpName.grid(row=4, column=1, pady=(5, 5))
        labelPushUpCount.grid(row=4, column=2, pady=(5, 5))

        # Row for Curl Up
        labelCurlUpName = tk.Label(right_frame, text="Curl Up: ", font=("Helvetica", 14), fg="green")
        labelCurlUpCount = tk.Label(right_frame, text="0", font=("Helvetica", 14), fg="green")
        labelCurlUpName.grid(row=5, column=1, pady=(5, 5))
        labelCurlUpCount.grid(row=5, column=2, pady=(5, 5))

        # Row for Jumpig Jack
        labelJumpingJackName = tk.Label(right_frame, text="Jumping Jack: ", font=("Helvetica", 14), fg="green")
        labelJumpingJackCount = tk.Label(right_frame, text="0", font=("Helvetica", 14), fg="green")
        labelJumpingJackName.grid(row=6, column=1, pady=(5, 5))
        labelJumpingJackCount.grid(row=6, column=2, pady=(5, 5))

        # Row for Squat
        labelSquatName = tk.Label(right_frame, text="Squat: ", font=("Helvetica", 14), fg="green")
        labelSquatCount = tk.Label(right_frame, text="0", font=("Helvetica", 14), fg="green")
        labelSquatName.grid(row=7, column=1, pady=(5, 5))
        labelSquatCount.grid(row=7, column=2, pady=(5, 5))

        # Store each labelTimer in the dictionary for updating later
        self.exercise_labels["PushUp"] = labelPushUpCount
        self.exercise_labels["CurlUp"] = labelCurlUpCount
        self.exercise_labels["JumpingJack"] = labelJumpingJackCount
        self.exercise_labels["Squat"] = labelSquatCount

        
        # Reset Button
        reset_btn = tk.Button(right_frame, text="Reset", command=lambda:self.reset_count_exercise(), 
                            font=("Helvetica", 12), bg="white", foreground="red", 
                            relief="flat", 
                            bd=2)  
        reset_btn.grid(row=9, column=0, columnspan=4, padx=10, pady=5)
        
        
    #------------------------YOGA SECTION------------------------
    def create_yogaTab(self):
        title_label = tk.Label(self.yogaTab, text="Track Your Yoga Poses using YOLOv8", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=10)

        # left side Frame
        left_frame = tk.Frame(self.yogaTab)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=20, pady=30)

        # right side Frame
        right_frame = tk.Frame(self.yogaTab)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=20, pady=10)

        #------------------------LEFT SIDE CONTENT------------------------
        self.yoga_canvas = tk.Canvas(left_frame, width=650, height=420, bg="gray")
        self.yoga_canvas.pack(pady=10)

        self.yoga_canvas.create_image(0, 0, anchor=tk.NW, image=self.default_image)

        camera_image = Image.open("./images/Livelogo.jpg").resize((30, 20))  
        camera_logo = ImageTk.PhotoImage(camera_image)
        self.camera_logo = camera_logo

        button_frame2 = tk.Frame(left_frame)
        button_frame2.pack(pady=10)

        start_btn = tk.Button(button_frame2, text="  Live Detection", command=lambda: self.start_detection_yoga(self.yoga_canvas), 
                            font=("Helvetica", 14, "bold"), bg="white", foreground="red", 
                            image=camera_logo, compound=tk.LEFT) 
        start_btn.pack(side=tk.LEFT, padx=5)

        stop_btn = tk.Button(button_frame2, text="CLOSE", command=lambda: self.stop_detection_yoga(self.yoga_canvas), 
                             font=("Helvetica", 12, "bold"), bg="white", foreground="darkblue")
        stop_btn.pack(side=tk.LEFT, padx=40)

        upload_btn = tk.Button(left_frame, text="Upload Videos", command=lambda:self.upload_video_yoga(self.yoga_canvas), font=("Helvetica", 12), width=15, height=1)
        upload_btn.pack(pady=10)
        
        #------------------------RIGHT SIDE CONTENT------------------------
        poses_label = tk.Label(right_frame, text="Yoga Poses Available:", font=("Helvetica", 14))
        poses_label.grid(row=0, column=0, columnspan=4, pady=(30, 10))  # Reduced vertical padding

        self.pose_images = {
            "Child": ImageTk.PhotoImage(Image.open("./images/child.jpg").resize((130, 130))),
            "Easy Seat": ImageTk.PhotoImage(Image.open("./images/easyseat.jpg").resize((130, 130))),
            "Tree": ImageTk.PhotoImage(Image.open("./images/tree.jpg").resize((130, 130))),
            "Triangle": ImageTk.PhotoImage(Image.open("./images/triangle.jpg").resize((130, 130)))
        }

        self.pose_buttons = {}
        col = 0
        for pose_name, img in self.pose_images.items():
            btn = tk.Label(right_frame, text=pose_name, image=img, compound=tk.TOP, font=("Helvetica", 12))
            btn.grid(row=1, column=col, padx=10, pady=10)
            self.pose_buttons[pose_name] = btn
            col += 1
            
        # Alert Animal Detection
        alert_image = Image.open("./images/alert.png").resize((30, 30))  # Assuming you have an alert.jpg image
        alert_logo = ImageTk.PhotoImage(alert_image)
        self.alert_logo = alert_logo  # Keep a reference to avoid garbage collection

        self.animal_status_label = tk.Label(right_frame, text="", font=("Helvetica", 16, "bold"), fg="red", image=alert_logo, compound=tk.LEFT)
        self.animal_status_label.grid(row=2, column=0, columnspan=4, pady=(0, 0))
        self.animal_status_label.grid_remove()  # Hide initially
        
        #blank label
        self.blank_label = tk.Label(right_frame, text="", font=("Helvetica", 16, "bold"), fg="red") 
        self.blank_label.grid(row=3, column=0, columnspan=4, pady=(0, 0))
        
        # Define each row explicitly for each pose
        self.pose_labels = {}  # Dictionary to store the timer label for each pose

        # Row for Child Pose
        labelChildPoseName = tk.Label(right_frame, text="Child: ", font=("Helvetica", 14), fg="green")
        labelChildTimer = tk.Label(right_frame, text="0:00:00", font=("Helvetica", 14), fg="green")
        labelChildMinutes = tk.Label(right_frame, text="   mins", font=("Helvetica", 14), fg="green")
        labelChildPoseName.grid(row=4, column=0, pady=(5, 5))
        labelChildTimer.grid(row=4, column=1, pady=(5, 5))
        labelChildMinutes.grid(row=4, column=2, columnspan=2, pady=(5, 5))

        # Row for Easy Seat Pose
        labelEasySeatPoseName = tk.Label(right_frame, text="Easy Seat: ", font=("Helvetica", 14), fg="green")
        labelEasySeatTimer = tk.Label(right_frame, text="0:00:00", font=("Helvetica", 14), fg="green")
        labelEasySeatMinutes = tk.Label(right_frame, text="   mins", font=("Helvetica", 14), fg="green")
        labelEasySeatPoseName.grid(row=5, column=0, pady=(5, 5))
        labelEasySeatTimer.grid(row=5, column=1, pady=(5, 5))
        labelEasySeatMinutes.grid(row=5, column=2, columnspan=2, pady=(5, 5))

        # Row for Tree Pose
        labelTreePoseName = tk.Label(right_frame, text="Tree: ", font=("Helvetica", 14), fg="green")
        labelTreeTimer = tk.Label(right_frame, text="0:00:00", font=("Helvetica", 14), fg="green")
        labelTreeMinutes = tk.Label(right_frame, text="   mins", font=("Helvetica", 14), fg="green")
        labelTreePoseName.grid(row=6, column=0, pady=(5, 5))
        labelTreeTimer.grid(row=6, column=1, pady=(5, 5))
        labelTreeMinutes.grid(row=6, column=2, columnspan=2, pady=(5, 5))

        # Row for Triangle Pose
        labelTrianglePoseName = tk.Label(right_frame, text="Triangle: ", font=("Helvetica", 14), fg="green")
        labelTriangleTimer = tk.Label(right_frame, text="0:00:00", font=("Helvetica", 14), fg="green")
        labelTriangleMinutes = tk.Label(right_frame, text="   mins", font=("Helvetica", 14), fg="green")
        labelTrianglePoseName.grid(row=7, column=0, pady=(5, 5))
        labelTriangleTimer.grid(row=7, column=1, pady=(5, 5))
        labelTriangleMinutes.grid(row=7, column=2, columnspan=2, pady=(5, 5))

        # Store each labelTimer in the dictionary for updating later
        self.pose_labels["Child"] = labelChildTimer
        self.pose_labels["Easy Seat"] = labelEasySeatTimer
        self.pose_labels["Tree"] = labelTreeTimer
        self.pose_labels["Triangle"] = labelTriangleTimer

        


        # REset Button
        reset_btn_yoga = tk.Button(right_frame, text="Reset", command=lambda:self.reset_count_yoga(), 
                            font=("Helvetica", 12), bg="white", foreground="red", 
                            relief="flat", 
                            bd=2)  
        reset_btn_yoga.grid(row=9, column=0, columnspan=4, padx=10, pady=15)
        
    


    

# Running the application
if __name__ == "__main__":
    root = tk.Tk()
    app = WorkoutTracker(root)
    root.mainloop()