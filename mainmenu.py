#main menu
import sys, pygame
from pygame.locals import *
import os
class List(object):
    def __init__(self, filename):
        self.data = []
        self.current = 0
        self.total = 0
        self.correct = 0
        self.score = 0
        self.selected = False
        self.failed = False
        self.wronganswer = 0
        self.colors = [white,white,white,white]

        #read List data from file
        f = open(filename, "r")
        List_data = f.readlines()
        f.close()

        #count and clean up list data
        for text_line in List_data:
            self.data.append(text_line.strip())
            self.total += 1
            print(self.total)

    def show_game(self):
        print_text(font1, 210, 5, "Menu List")
        print_text(font2, 190, 500-20, "Press Keys To Select", purple)

        for i in range(self.total-1):
            print_text(font2,20,170+30*i,self.data[i],self.colors[i])


    def handle_input(self,number):
        self.colors = [white,white,white,white]
        self.colors[number-1] = green
            

def print_text(font, x, y, text, color=(255,255,255), shadow=True):
    if shadow:
        imgText = font.render(text, True, (0,0,0))
        screen.blit(imgText, (x-2,y-2))
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x,y))
    

#main program begins
pygame.init()
screen = pygame.display.set_mode((600,500))
pygame.display.set_caption("The Game List")
font1 = pygame.font.Font(None, 40)
font2 = pygame.font.Font(None, 24)
white = 255,255,255
cyan = 0,255,255
yellow = 255,255,0
purple = 255,0,255
green = 0,255,0
red = 255,0,0

#load the trivia data file
list= List("gameList.txt")
current=1
space = pygame.image.load("./image/space.png").convert_alpha()
#repeating loop
while True:
    screen.blit(space, (0,0))
    for event in pygame.event.get():
        if event.type == QUIT:
            exit(0)
        elif event.type == KEYUP:
            if event.key == pygame.K_ESCAPE:
                exit(0)
            elif event.key == pygame.K_1:
                list.handle_input(1)
            elif event.key == pygame.K_2:
                list.handle_input(2)
            elif event.key == pygame.K_3:
                list.handle_input(3)
            elif event.key == pygame.K_4:
                list.handle_input(4)
            elif event.key == pygame.K_s:
                current+=1
                list.handle_input(current%(list.total-1))
            elif event.key == pygame.K_w:
                current-=1
                list.handle_input(current%(list.total-1))
            elif event.key == pygame.K_SPACE:
                if current==1:
                    os.system('python3 game.py')
                if current==2:
                    os.system('python3 escape_dragon.py')
                if current==3:
                    os.system('python3 ZombieMobGame.py')
    #display trivia data
    list.show_game()
    
    #update the display
    pygame.display.update()
    
