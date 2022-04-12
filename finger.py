"""# -*-            coding: utf-8 -*
import cv2
import numpy as np

# 创建一个video capture的实例
# VideCapture里面的序号
# 0 : 默认为笔记本上的摄像头(如果有的话) / USB摄像头 webcam
# 1 : USB摄像头2
# 2 ：USB摄像头3 以此类推
# -1：代表最新插入的USB设备
cap = cv2.VideoCapture(0)

# 查看Video Capture是否已经打开
print("摄像头是否已经打开 ？ {}".format(cap.isOpened()))
width = 640
height = 480
# 设置画面的尺寸
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# 创建一个名字叫做 “image_win” 的窗口
# 窗口属性 flags
#   * WINDOW_NORMAL：窗口可以放缩
#   * WINDOW_KEEPRATIO：窗口缩放的过程中保持比率
#   * WINDOW_GUI_EXPANDED： 使用新版本功能增强的GUI窗口
cv2.namedWindow('src_image', flags=cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_EXPANDED)
cv2.resizeWindow('src_image', int(width), height)

# 图像计数 从1开始
img_count = 1

while True:
    # 获取图像，如果画面读取成功 ret=True，frame是读取到的图片对象(numpy的ndarray格式)
    ret, frame = cap.read()

    if not ret:
        print("图像获取失败，请按照说明进行问题排查")
        # 读取失败？问题排查
        print("* 硬件问题     \t在就是检查一下USB线跟电脑USB接口")
        print("* 设备挂载问题  \t摄像头没有被挂载，如果是虚拟机需要手动勾选设备")
        print("* 接口兼容性问题\t或者USB2.0接口接了一个USB3.0的摄像头，也是不支持的。")
        print("* 驱动问题     \t有的摄像头可能存在驱动问题，需要安装相关驱动，或者查看摄像头是否有UVC免驱协议")
        break

    cv2.imshow('src_image', frame)
    # 等待按键事件发生 单位毫秒
    key = cv2.waitKey(2)
    if key == ord('q'):
        print("程序退出...")
        break
    elif key == ord('c'):
        # 如果c键按下，则进行图片保存
        # 写入图片 并命名图片为 图片序号.png
        cv2.imwrite("{}.png".format(img_count), frame)
        print("保存图片为  {}.png".format(img_count))
        # 图片编号计数自增1
        img_count += 1
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        cv2.imshow('src_image', frame)
        key = cv2.waitKey(2)
    # 将BGR彩图变换为灰度图
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray_image', gray_frame)

    # 二值化显示
    (thresh, gray) = cv2.threshold(gray_frame, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(gray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    color = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    img = cv2.drawContours(color, contours, -1, (255,255,255), 2)
    cv2.imshow('counter_image', color)
# 释放VideoCapture
cap.release()
# 销毁所有的窗口
cv2.destroyAllWindows()"""
import cv2
from mediapipe import solutions
import time
import math
from pynput.keyboard import Key, Controller

keyboard = Controller()
def angleBetweenVector(vector_1, vector_2):
    vector_1_x=vector_1[0]
    vector_1_y=vector_1[1]
    vector_2_x=vector_2[0]
    vector_2_y=vector_2[1]
    try:
        angle= math.degrees(math.acos((vector_1_x*vector_2_x+vector_1_y*vector_2_y)/(((vector_1_x**2+vector_1_y**2)**0.5)*((vector_2_x**2+vector_2_y**2)**0.5))))
    except:
        angle =65535.
    if angle > 180.:
        angle = 65535.
    return angle

def hand_angle(hand_):
    # 列表存储各个手指的角度
    angle_list = []
    # 大拇指角度
    angle_ = angleBetweenVector(
        ((int(hand_[0][0])- int(hand_[2][0])),(int(hand_[0][1])-int(hand_[2][1]))),
        ((int(hand_[3][0])- int(hand_[4][0])),(int(hand_[3][1])- int(hand_[4][1])))
        )
    angle_list.append(angle_)
    # 食指角度
    angle_ = angleBetweenVector(
        ((int(hand_[0][0])-int(hand_[6][0])),(int(hand_[0][1])- int(hand_[6][1]))),
        ((int(hand_[7][0])- int(hand_[8][0])),(int(hand_[7][1])- int(hand_[8][1])))
        )
    angle_list.append(angle_)
    #---------------------------- middle 中指角度
    angle_ = angleBetweenVector(
        ((int(hand_[0][0])- int(hand_[10][0])),(int(hand_[0][1])- int(hand_[10][1]))),
        ((int(hand_[11][0])- int(hand_[12][0])),(int(hand_[11][1])- int(hand_[12][1])))
        )
    angle_list.append(angle_)
    #---------------------------- ring 无名指角度
    angle_ = angleBetweenVector(
        ((int(hand_[0][0])- int(hand_[14][0])),(int(hand_[0][1])- int(hand_[14][1]))),
        ((int(hand_[15][0])- int(hand_[16][0])),(int(hand_[15][1])- int(hand_[16][1])))
        )
    angle_list.append(angle_)
    #---------------------------- pink 小拇指角度
    angle_ = angleBetweenVector(
        ((int(hand_[0][0])- int(hand_[18][0])),(int(hand_[0][1])- int(hand_[18][1]))),
        ((int(hand_[19][0])- int(hand_[20][0])),(int(hand_[19][1])- int(hand_[20][1])))
        )
    angle_list.append(angle_)
    return angle_list


def h_gesture(angle_list, hand_point_2d):
    '''
        # 二维约束的方法定义手势
        # fist five gun love one six three thumbup yeah
    '''
    thr_angle = 65.
    thr_angle_thumb = 53.
    thr_angle_s = 49.
    gesture_str = None
    if 65535. not in angle_list:
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

        elif (angle_list[0]<thr_angle_s)  and (angle_list[1]>thr_angle) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle) and (hand_point_2d[4][1]<hand_point_2d[0][1]) and (angleBetweenVector(((int(hand_point_2d[4][0])- int(hand_point_2d[0][0])),(int(hand_point_2d[4][1])- int(hand_point_2d[0][1]))), (255,0))>45) and (angleBetweenVector(((int(hand_point_2d[4][0])- int(hand_point_2d[0][0])),(int(hand_point_2d[4][1])- int(hand_point_2d[0][1]))), (255,0))<125):
            gesture_str = "GoUp"
            keyboard.press('w')

        elif (angle_list[0]<thr_angle_s)  and (angle_list[1]>thr_angle) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle) and (hand_point_2d[4][1]>hand_point_2d[0][1]) and (angleBetweenVector(((int(hand_point_2d[4][0])- int(hand_point_2d[0][0])),(int(hand_point_2d[4][1])- int(hand_point_2d[0][1]))), (255,0))>45) and (angleBetweenVector(((int(hand_point_2d[4][0])- int(hand_point_2d[0][0])),(int(hand_point_2d[4][1])- int(hand_point_2d[0][1]))), (255,0))<125):
            gesture_str = "GoDown"
            keyboard.press('s')

        elif (angle_list[0]<thr_angle_s)  and (angle_list[1]>thr_angle) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle) and (angleBetweenVector(((int(hand_point_2d[4][0])- int(hand_point_2d[0][0])),(int(hand_point_2d[4][1])- int(hand_point_2d[0][1]))), (255,0))<45):
            gesture_str = "GoRight"
            keyboard.press('d')

        elif (angle_list[0]<thr_angle_s)  and (angle_list[1]>thr_angle) and (angle_list[2]>thr_angle) and (angle_list[3]>thr_angle) and (angle_list[4]>thr_angle) and (angleBetweenVector(((int(hand_point_2d[4][0])- int(hand_point_2d[0][0])),(int(hand_point_2d[4][1])- int(hand_point_2d[0][1]))), (255,0))>125):
            gesture_str = "GoLeft"
            keyboard.press('a')




    return gesture_str



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
    print(results)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            hand_point_2d = []
            for i in range(21):
                x = handLms.landmark[i].x*img.shape[1]
                y = handLms.landmark[i].y*img.shape[0]
                hand_point_2d.append((x,y))
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            if hand_point_2d:
                angle_list = hand_angle(hand_point_2d)
                gesture_str = h_gesture(angle_list, hand_point_2d)
                # cv2.putText(img, gesture_str, (250, 50), 0, 1.3, (0, 0, 255), 3)
                print(angleBetweenVector(((int(hand_point_2d[4][0])- int(hand_point_2d[0][0])),(int(hand_point_2d[4][1])- int(hand_point_2d[0][1]))), (255,0)))
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # cv2.putText(img, str(int(fps)), (25, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        print("程序退出...")
        break