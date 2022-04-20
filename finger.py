import cv2
from mediapipe import solutions
import time
import math
from pynput.keyboard import Key, Controller
# 初始化模拟键盘
keyboard = Controller()


# 该函数使用余弦定理计算两个向量间的夹角
def angleBetweenVector(vector_1, vector_2):
    vector_1_x=vector_1[0]
    vector_1_y=vector_1[1]
    vector_2_x=vector_2[0]
    vector_2_y=vector_2[1]
    angle= math.degrees(math.acos((vector_1_x*vector_2_x+vector_1_y*vector_2_y)/(((vector_1_x**2+vector_1_y**2)**0.5)*((vector_2_x**2+vector_2_y**2)**0.5))))
    if angle > 180.:
        angle = 65535.
    return angle

def hand_angle(hand_):
    # 列表存储各个手指的角度
    angle_list = []
    # 大拇指角度
    angle = angleBetweenVector(
        ((int(hand_[0][0])- int(hand_[2][0])),(int(hand_[0][1])-int(hand_[2][1]))),
        ((int(hand_[3][0])- int(hand_[4][0])),(int(hand_[3][1])- int(hand_[4][1])))
        )
    angle_list.append(angle)
    # 食指角度
    angle = angleBetweenVector(
        ((int(hand_[0][0])-int(hand_[6][0])),(int(hand_[0][1])- int(hand_[6][1]))),
        ((int(hand_[7][0])- int(hand_[8][0])),(int(hand_[7][1])- int(hand_[8][1])))
        )
    angle_list.append(angle)
    # 中指角度
    angle = angleBetweenVector(
        ((int(hand_[0][0])- int(hand_[10][0])),(int(hand_[0][1])- int(hand_[10][1]))),
        ((int(hand_[11][0])- int(hand_[12][0])),(int(hand_[11][1])- int(hand_[12][1])))
        )
    angle_list.append(angle)
    # 无名指角度
    angle = angleBetweenVector(
        ((int(hand_[0][0])- int(hand_[14][0])),(int(hand_[0][1])- int(hand_[14][1]))),
        ((int(hand_[15][0])- int(hand_[16][0])),(int(hand_[15][1])- int(hand_[16][1])))
        )
    angle_list.append(angle)
    # 小拇指角度
    angle = angleBetweenVector(
        ((int(hand_[0][0])- int(hand_[18][0])),(int(hand_[0][1])- int(hand_[18][1]))),
        ((int(hand_[19][0])- int(hand_[20][0])),(int(hand_[19][1])- int(hand_[20][1])))
        )
    angle_list.append(angle)
    return angle_list


def judge_gesture(angle_list, hand_point_2d):
    # 按键操作绑定：
    # 握拳：释放WASD
    # 数字五：按下空格
    # GoUP：按下W
    # GoDown：按下S
    # GoLeft：按下A
    # GoRight：按下D
    # 设置夹角阈值 来获得手势
    thr_angle = 65.
    thr_angle_thumb = 54.
    thr_angle_s = 50.
    gesture_str = None
    if 65535. not in angle_list:
        # 握拳手势 释放方向键
        if (angle_list[0]>thr_angle_thumb) and (angle_list[1]>thr_angle) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle):
            gesture_str = "fist"
            keyboard.release('w')
            keyboard.release('s')
            keyboard.release('d')
            keyboard.release('a')

        elif (angle_list[0]<thr_angle_s) and (angle_list[1]<thr_angle_s) and (angle_list[2]<thr_angle_s) and (angle_list[3]<thr_angle_s) and (angle_list[4]<thr_angle_s):
            gesture_str = "five"
            keyboard.press(Key.space)
            keyboard.release(Key.space)

        elif (angle_list[0]<thr_angle_s)  and (angle_list[1]>thr_angle) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) \
                and (angle_list[4]>thr_angle) and (hand_point_2d[4][1]<hand_point_2d[0][1]) \
                and (angleBetweenVector(((int(hand_point_2d[4][0])- int(hand_point_2d[0][0])),(int(hand_point_2d[4][1])- int(hand_point_2d[0][1]))), (255,0))>45) \
                and (angleBetweenVector(((int(hand_point_2d[4][0])- int(hand_point_2d[0][0])),(int(hand_point_2d[4][1])- int(hand_point_2d[0][1]))), (255,0))<125):
            gesture_str = "GoUp"
            keyboard.press('w')

        elif (angle_list[0]<thr_angle_s)  and (angle_list[1]>thr_angle) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and \
                (angle_list[4]>thr_angle) and (hand_point_2d[4][1]>hand_point_2d[0][1]) \
                and (angleBetweenVector(((int(hand_point_2d[4][0])- int(hand_point_2d[0][0])),(int(hand_point_2d[4][1])- int(hand_point_2d[0][1]))), (255,0))>45) \
                and (angleBetweenVector(((int(hand_point_2d[4][0])- int(hand_point_2d[0][0])),(int(hand_point_2d[4][1])- int(hand_point_2d[0][1]))), (255,0))<125):
            gesture_str = "GoDown"
            keyboard.press('s')

        elif (angle_list[0]<thr_angle_s)  and (angle_list[1]>thr_angle) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and \
                (angle_list[4]>thr_angle) and (angleBetweenVector(((int(hand_point_2d[4][0])- int(hand_point_2d[0][0])),(int(hand_point_2d[4][1])- int(hand_point_2d[0][1]))), (255,0))<45):
            gesture_str = "GoRight"
            keyboard.press('d')

        elif (angle_list[0]<thr_angle_s)  and (angle_list[1]>thr_angle)\
                and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle)\
                and (angle_list[4]>thr_angle) and (angleBetweenVector(((int(hand_point_2d[4][0]) - int(hand_point_2d[0][0])), (int(hand_point_2d[4][1])- int(hand_point_2d[0][1]))), (255,0))>125):
            gesture_str = "GoLeft"
            keyboard.press('a')
    return gesture_str


# ------主程序---------
# 开发板中一般端口为10或者11
cap = cv2.VideoCapture(0)
mpHands = solutions.hands
hands = mpHands.Hands()
mpDraw = solutions.drawing_utils
pTime = 0
count = 0
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            hand_point_2d = []
            for i in range(21):
                x = handLms.landmark[i].x*img.shape[1]
                y = handLms.landmark[i].y*img.shape[0]
                hand_point_2d.append((x,y))
            # 绘制关键点
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            if hand_point_2d:
                angle_list = hand_angle(hand_point_2d)
                gesture_str = judge_gesture(angle_list, hand_point_2d)
                # 绘制手势识别结果
                cv2.putText(img, gesture_str, (250, 50), 0, 1.3, (0, 0, 255), 3)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # 打印帧率
    cv2.putText(img, str(int(fps)), (25, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        print("程序退出...")
        break