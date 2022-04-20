# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 14:03:09 2021

@author: Administrator
"""
import pygame
import sys
import numpy as np
from pygame.locals import *
import json
import select
import socket

# 界面初始化
screen = pygame.display.set_mode((660, 650))
pygame.display.set_caption('井字棋！')
pygame.init()
# 图片导入
img_background = pygame.image.load('./image/back.jpg').convert()
img_circle = pygame.image.load('./image/circle.jpg').convert()
img_circle = pygame.transform.scale(img_circle,(150,150))
img_circle = img_circle.convert()
img_cross = pygame.image.load('./image/cross.jpg')
img_cross = pygame.transform.scale(img_cross,(150,150))
img_cross = img_cross.convert()
# 用于传送的数据
msg = []
# 棋盘定义
chessboard = [[[50,50],[250,50],[450,50]],[[50,250],[250,250],[450,250]],[[50,450],[250,450],[450,450]]]
# 棋盘格子是否落子
chess_exist = [[0 for i in range(3)] for j in range(3)]
# 圈、叉初始化
cross, circle = [], []
# 棋子类型
chess_kind = 1
cross_x, corss_y, circle_x, circle_y = [], [], [], []  # white_chess_x
last_y = 0
last_x = 0
last_i = 50
last_j = 50


# 绘制棋盘
def draw_background():
    screen.blit(img_background, (-100, 0))
    pygame.display.update()


# 绘制标记当前位置的三角形
def drawTriangle(i, j):
    global last_i
    global last_j
    x = chessboard[i][j][0]
    y = chessboard[i][j][1]
    points = [(last_i + 50, last_j), (last_i + 88, last_j), (last_i + 69, last_j + 26)]
    pygame.draw.polygon(screen, "white", points, 0)
    points = [(x + 50, y), (x + 88, y), (x + 69, y + 26)]
    pygame.draw.polygon(screen, "RED", points, 0)
    last_i = x
    last_j = y
    return


# 利用按键下棋
def set_chess():
    flag = 0
    # 上一次的目标位置
    global last_x
    global last_y
    current_x = last_x
    current_y = last_y
    if event.type == KEYDOWN:
        if event.key == K_d:
            current_y = current_y + 1
            # 控制坐标，不能超出边界
            if current_y>2:
                current_y = 2
        if event.key == K_a:
            current_y = current_y - 1
            if current_y<0:
                current_y = 0
        if event.key == K_s:
            current_x = current_x + 1
            if current_x>2:
                current_x = 2
        if event.key == K_w:
            current_x = current_x - 1
            if current_x<0:
                current_x = 0
        if event.key == K_SPACE:
            flag = 1
    # 更新全局变量，保存该次位置
    last_x = current_x
    last_y = current_y
    drawTriangle(last_x, last_y)
    # 当前位置没有棋子占用
    if flag == 1 and chess_exist[current_x][current_y] == 0:
        # 添加列表项 保存位置
        circle.append([current_x, current_y])
        circle_x.append(circle[-1][0])
        circle_y.append(circle[-1][1])
        # 将坐标位置打包
        msg.extend((current_x, current_y))
        chess_exist[current_x][current_y] = 1
        pygame.display.update()
        # 成功落子
        return 1


def draw_chess():
    for i in circle:
        screen.blit(img_circle, (50 + i[1] * 200, 50 + i[0] * 200))
    for i in cross:
        screen.blit(img_cross, (50 + i[1] * 200, 50 + i[0] * 200))
    pygame.display.update()


# 枚举叉赢的情况
def cross_win():
    # 同一行有三个相同棋子
    win_case = chess_exist.count([2, 2, 2])
    if win_case == 1:
        return 1
    chessexist = np.mat(chess_exist)
    # 对角线有三个相同棋子
    Diagonal = [chessexist[i, i] for i in range(3)]
    win_case = Diagonal.count([2])
    if win_case == 3:
        return 1
    another_Diagonal = [chessexist[2 - i, i] for i in range(3)]
    win_case = another_Diagonal.count([2])
    if win_case == 3:
        return 1
    # 同一列有三个相同棋子
    column = chessexist.T.tolist()
    win_case = column.count([2, 2, 2])
    if win_case == 1:
        return 1
    return 0


# 枚举圈赢的情况
def circle_win():
    win_case = chess_exist.count([1, 1, 1])
    if win_case == 1:
        return 1
    chessexist = np.mat(chess_exist)
    Diagonal = [chessexist[i, i] for i in range(3)]
    win_case = Diagonal.count([1])
    if win_case == 3:
        return 1
    another_Diagonal = [chessexist[2 - i, i] for i in range(3)]
    win_case = another_Diagonal.count([1])
    if win_case == 3:
        return 1
    column = chessexist.T.tolist()
    win_case = column.count([1, 1, 1])
    if win_case == 1:
        return 1
    return 0


def gameover():
    if cross_win()==1:
        return 0
    if circle_win()==1:
        return 1
    return 2


def draw_text(text, x, y, size, fontColor=(0,0,0), backgroudColor=(255,255,255)):
    pygame.font.init()
    fontObj = pygame.font.SysFont('SimHei', size)
    textSurfaceObj = fontObj.render(text, True, fontColor, backgroudColor)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (x, y)
    screen.blit(textSurfaceObj, textRectObj)
    pygame.display.update()

# ----------------------主程序----------------------------
# 绘制棋盘并更新显示
draw_background()
pygame.display.update()

# 利用一次通信来获得本机的IP地址
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
finally:
    s.close()
# 定义服务器
print("当前IP地址为：",ip)
HOST = ip
PORT = 10000
BUFSIZE = 1024
ADDR = (HOST, PORT)
# 定义服务器连接
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 允许重用ip和端口号
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# 绑定地址到套接字
server.bind(ADDR)
# 开始监听
server.listen(1)
inputs = [server]
settable = 1
link = False
while True:
    # 其中rs是等待读取的对象，
    # ws是等待写入的对象，
    # es是等待异常的对象，
    rs, ws, es = select.select(inputs, [], [], 0)
    for r in rs:
        if r is server:
            link = True
            print('new ser')
            tcpclient, addr = server.accept()
            inputs.append(tcpclient)
        else:
            data, addr = r.recvfrom(BUFSIZE)
            disconnected = not data
            draw_text('你的回合', 300, 20, 15)
            if disconnected:
                inputs.remove(r)
                draw_text('对手掉线', 300, 20, 15)
                while True:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
            else:
                # 加载获得的数据
                data = json.loads(data)
                settable = 1
                # 将坐标添加至该种棋子的坐标列表中
                cross.append(data)
                # 标记该处已被占用
                chess_exist[data[0]][data[1]] = 2
                cross_x.append(data[0])
                corss_y.append(data[1])
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            server.close()
        if link == True:
            if settable == 1:
                if set_chess() == 1:
                    draw_text('对手回合', 300, 20, 15)
                    settable = 0
                    # 打包将要传输数据
                    msg_ready = json.dumps(msg)
                    print(msg_ready)
                    # 发送数据
                    tcpclient.sendto(msg_ready.encode(), ADDR)
                    # 清空待发送的数据
                    msg = []
    draw_chess()
    # 赢了
    if gameover() == 1:
        draw_text('WIN！', 350, 320, 55,(255, 0, 0), (255, 255, 255))
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
    # 输了
    elif gameover() == 0:
        draw_text('LOSE！', 350, 320, 55,(255, 0, 0), (255, 255, 255))
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
tcpclient.close()
server.close()


