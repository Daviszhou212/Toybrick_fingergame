# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 14:03:09 2021

@author: Administrator
"""
import numpy as np
import pygame
import sys
from pygame.locals import *
from collections import Counter
from socket import *
from time import ctime
import json
import select
import socket
import time

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
# 黑白棋子初始化
cross, circle = [], []
# 棋子类型
chess_kind = 1  # 1为黑棋，0为白棋
cross_x, cross_y, circle_x, circle_y = [], [], [], []  # white_chess_x


def draw_Chessboard():
    screen.blit(img_background, (-100, 0))
    pygame.display.update()


# 默认棋子类型为0
def set_chess():
    if event.type == MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        for i in range(len(chessboard)):
            for j in range(len(chessboard[i])):
                if chessboard[i][j][0] < pos[0] < chessboard[i][j][0] + 200 and chessboard[i][j][1] < pos[1] < \
                        chessboard[i][j][1] + 200:
                    if chess_exist[i][j] == 0:
                        cross.append([i, j])
                        cross_x.append(cross[-1][0])
                        cross_y.append(cross[-1][1])
                        msg.extend((i, j))
                        chess_exist[i][j] = 2
                        pygame.display.update()
                        print(chess_exist)
                        return 1


def draw_chess():
    for i in circle:
        screen.blit(img_circle, (50 + i[1] * 200, 50 + i[0] * 200))
    for i in cross:
        screen.blit(img_cross, (50 + i[1] * 200, 50 + i[0] * 200))
    pygame.display.update()


# 枚举叉赢的情况
def cross_win():
    win_case = chess_exist.count([2, 2, 2])
    if win_case == 1:
        return 1
    chessexist = np.mat(chess_exist)
    Diagonal = [chessexist[i, i] for i in range(3)]
    win_case = Diagonal.count([2])
    if win_case == 3:
        return 1
    another_Diagonal = [chessexist[2 - i, i] for i in range(3)]
    win_case = another_Diagonal.count([2])
    if win_case == 3:
        return 1
    column = chessexist.T.tolist()
    win_case = column.count([2, 2, 2])
    if win_case == 1:
        return 1
    return 0


#
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
        return 1
    if circle_win()==1:
        return 0
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
draw_Chessboard()
settable = 0
# 定义客户端名称
HOST = '10.162.19.220'
PORT = 10000
BUFSIZE = 1024
ADDR = (HOST, PORT)
# 连接服务器
Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Client.connect(ADDR)
inputs = [Client]
while True:
    rs, ws, es = select.select(inputs, [], [], 0)
    for r in rs:
        if r is Client:
            data, addr = r.recvfrom(BUFSIZE)
            print(data)
            draw_text('你的回合', 300, 20, 15)
            data = json.loads(data)
            print(data)
            settable = 1
            circle.append(data)
            chess_exist[data[0]][data[1]] = 1
            circle_x.append(data[0])
            circle_y.append(data[1])
    for event in pygame.event.get():
        if event.type == QUIT:
            Client.close()
            pygame.quit()
            sys.exit()
        if settable == 1:
            if set_chess() == 1:
                draw_text('对手回合', 300, 20, 15)
                settable = 0
                msg1 = json.dumps(msg)
                Client.sendto(msg1.encode(), ADDR)
                msg = []
    draw_chess()
    if gameover() == 1:
        draw_text('WIN！', 350, 320, 55,(255, 0, 0), (255, 255, 255))
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
    elif gameover() == 0:
        draw_text('LOSE！', 350, 320, 55,(255, 0, 0), (255, 255, 255))
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
