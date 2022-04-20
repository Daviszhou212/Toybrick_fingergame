import math
import sys
import pygame
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption(("Orbit Demo"))
font = pygame.font.Font(None, 18)
vel=0.2
class Point(object):
    def __init__(self,x,y):
        self.__x=x
        self.y=y

    #X property
    def getx(self): return self.__x
    def setx(self, x): self.__x = x
    x = property(getx, setx)

    #Y property
    def gety(self): return self.__y
    def sety(self, y): self.__y = y
    y = property(gety, sety)

    def __str__(self):
        return "{X:" + "{:.0f}".format(self.__x) + \
            ",Y:" + "{:.0f}".format(self.__y) + "}"

#print_text function
def print_text(font, x, y, text, color=(255,255,255)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x,y))

#wrap_angle function
def wrap_angle(angle):
    return angle % 360

#load bitmaps
space=pygame.image.load("./image/space.png").convert_alpha()
planet=pygame.image.load("./image/planet2.png").convert_alpha()
ship=pygame.image.load("./image/military.png").convert_alpha()
width,height=ship.get_size()
ship=pygame.transform.smoothscale(ship, (width//2,height//2))

pos = Point(0,0)
old_pos = Point(0,0)
radius = 250
angle = 0.0


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit(0)
        elif event.type==KEYDOWN :
            if event.key==pygame.K_w:
                vel+=0.08
            elif event.key==pygame.K_s:
                vel-=0.08
    
    keys=pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        exit(0)
    
    #move the ship
    angle = wrap_angle(angle + vel)
    pos.x = math.sin( math.radians(angle) ) * radius
    pos.y = math.cos( math.radians(angle) ) * radius

    #rotate the ship
    delta_x = ( pos.x - old_pos.x )
    delta_y = ( pos.y - old_pos.y )
    rangle = math.atan2(delta_y, delta_x)
    rangled = wrap_angle( -math.degrees(rangle) )
    scratch_ship = pygame.transform.rotate(ship, rangled)

    screen.blit(space, (0,0))
    width,height=planet.get_size()
    screen.blit(planet, (400-width/2,300-height/2))
    
    #draw the ship
    width,height = scratch_ship.get_size()
    x = 400+pos.x-width//2
    y = 300+pos.y-height//2
    screen.blit(scratch_ship, (x,y))
    
    
    print_text(font, 0, 0, "Orbit: " + "{:.0f}".format(angle))
    print_text(font, 0, 20, "Rotation: " + "{:.2f}".format(rangle))
    print_text(font, 0, 40, "Position: " + str(pos))
    print_text(font, 0, 60, "Old Pos: " + str(old_pos))
    
    pygame.display.update()
    
    #remember position
    old_pos.x = pos.x
    old_pos.y = pos.y
