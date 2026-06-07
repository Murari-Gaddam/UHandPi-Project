
import sys
import cv2
import time
import math
import signal
import threading
import numpy as np
import mediapipe as mp
from calibration.camera import Camera 
from common.transform import vector_2d_angle
import random

board = None
agc =None
robot = ""
player = ""
score = {
    "Rwins":0,
    "Uwins":0,
    "Tie":0
}


if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)
   
gesture = None
mp_drawing = mp.solutions.drawing_utils
hand_detector = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_tracking_confidence=0.05,
            min_detection_confidence=0.6
        )


def init_move():
    agc.runAction('15_5_12345')



size = (640, 480)
__isRunning = False
_stop = False


def init():
    init_move()
    print("RockPaperScissors Init")
    
def start():
    global __isRunning
    __isRunning = True
    print("RockPaperScissors Start")
    
def stop():
    global __isRunning
    __isRunning = False 
    init_move()   
    print("RockPaperScissors Stop")

def exit():
    global __isRunning
    init_move()
    __isRunning = False
    print("RockPaperScissors Exit")

def get_hand_landmarks(img, landmarks):

    h, w, _ = img.shape
    landmarks = [(lm.x * w, lm.y * h) for lm in landmarks]
    return np.array(landmarks)

def hand_angle(landmarks):
    angle_list = []

    angle_ = vector_2d_angle(landmarks[3] - landmarks[4], landmarks[0] - landmarks[2])
    angle_list.append(angle_)

    angle_ = vector_2d_angle(landmarks[0] - landmarks[6], landmarks[7] - landmarks[8])
    angle_list.append(angle_)

    angle_ = vector_2d_angle(landmarks[0] - landmarks[10], landmarks[11] - landmarks[12])
    angle_list.append(angle_)

    angle_ = vector_2d_angle(landmarks[0] - landmarks[14], landmarks[15] - landmarks[16])
    angle_list.append(angle_)
  
    angle_ = vector_2d_angle(landmarks[0] - landmarks[18], landmarks[19] - landmarks[20])
    angle_list.append(angle_)
    angle_list = [abs(a) for a in angle_list]
    return angle_list

def h_gesture(angle_list):
    global user
    thr_angle = 65.
    thr_angle_thumb = 53.
    thr_angle_s = 49.
    gesture_str = "none"
    if (angle_list[0] > thr_angle_thumb) and (angle_list[1] > thr_angle) and (angle_list[2] > thr_angle) and (
            angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
        gesture_str = "rock"
    elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s) and (
            angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
        gesture_str = "scissors"
    elif (angle_list[0] < thr_angle_s) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s) and (
            angle_list[3] < thr_angle_s) and (angle_list[4] < thr_angle_s):
        gesture_str = "paper"
    else:
        "none"
    user = gesture_str
    return gesture_str

            
def move():
    global __isRunning, gesture , robot
    global _stop
    Hgesture = random.choice(["rock","scissors","paper"])
    while True:
        if __isRunning:
            Hgesture = random.choice(["rock","scissors","paper"])
            if Hgesture == 'scissors' :
                agc.runAction('0_0_0')
                                            
            elif Hgesture == 'rock' :
                agc.runAction('15_5_12345')

            elif Hgesture == 'paper' :
                agc.runAction('6_2_23')
            robot = Hgesture


        else:
            if _stop:
                init_move() 
                time.sleep(1.5)               
            time.sleep(0.01)
            
threading.Thread(target=move, args=(), daemon=True).start()

def Win ():
    global user , robot ,score
    if player == robot:
        result = "Draw"
        score["Tie"]+=1
    elif player == "rock" and robot == "scissors":
        result = "Player wins"
        score["Uwins"]+=1

    elif player == "paper" and robot == "rock":
        result = "Player wins"
        score["Uwins"]+=1

    elif player == "scissors" and robot == "paper":
        result = "Player wins"
        score["Uwins"]+=1
    else:
        result = "Robot wins"
        score["Rwins"]+=1

    return result

prev_time = 0
def run(img):
    global __isRunning, prev_time , score
    global gesture, l_gesture
    img_copy = img.copy()

    if not __isRunning: 
        return img 
    
    frame_resize = cv2.resize(img_copy, size, interpolation=cv2.INTER_NEAREST)
    frame_gb = cv2.GaussianBlur(frame_resize, (3, 3), 3)
    
    frame_rgb = cv2.cvtColor(frame_gb, cv2.COLOR_BGR2RGB)
    
    results = hand_detector.process(frame_rgb)
    result_image = frame_rgb.copy()
    if results is not None and results.multi_hand_landmarks:
        
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                result_image,
                hand_landmarks,
                mp.solutions.hands.HAND_CONNECTIONS)
            landmarks = get_hand_landmarks(img_copy, hand_landmarks.landmark)
            angle_list = (hand_angle(landmarks))
            gesture = (h_gesture(angle_list))
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time)
            prev_time = curr_time
            last_user = None

            if gesture != last_user and gesture != "none":

                winner = Win()

                last_user = gesture
            else:
                winner = "None"
            lines = [
                f"Player Move : {user}",
                f"Robot Move  : {robot}",
                f"Result      : {winner}",
                "---- Score ----",
                f"P : {score['Uwins']}  R : {score['Rwins']}  Tie : {score['Tie']}"
            ]

            y = 40

            for line in lines:
                cv2.putText(
                    result_image,
                    line,
                    (20, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

                y += 35
            
            cv2.putText(result_image, gesture, (10, img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    result_image = cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR)
    return  result_image 



def manual_stop(signum, frame):
    global __isRunning
    __isRunning = False
    init_move()

if __name__ == '__main__':
    from common.ros_robot_controller_sdk import Board
    from common.action_group_controller import ActionGroupController

    board = Board()
    agc = ActionGroupController(board)
    init()
    start()
    camera = Camera()
    camera.camera_open(correction=True)
    signal.signal(signal.SIGINT, manual_stop)
    while __isRunning:
        img = camera.frame
        if img is not None:
            frame = img.copy()
            Frame = run(frame) 
               
            result_image = cv2.resize(Frame, (320, 240))
            cv2.imshow('rock_paper_scissors', result_image)
            
            key = cv2.waitKey(1)
            if key == 27:
                break
        else:
            time.sleep(0.01)
    camera.camera_close()
    cv2.destroyAllWindows()

