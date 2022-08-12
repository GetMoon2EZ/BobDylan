import pygame
from pygame.locals import *
import sys

def epaisseur(n):
    if n<40:
        return 3
    elif 40<=n<100:
        return 1
    elif 100<=n<500:
        return 1
    elif n>=500:
        return -1

pygame.init()
 
DISPLAYSURF = pygame.display.set_mode((1920,1080), FULLSCREEN)    #set the display mode, window title and FPS clock
pygame.display.set_caption('Map Rendering Demo')
FPSCLOCK = pygame.time.Clock()

n=10
 
TILEWIDTH = (1920/n)*0.8  #holds the tile width and height
TILEHEIGHT = TILEWIDTH/2
TILEHEIGHT_HALF = TILEHEIGHT /2
TILEWIDTH_HALF = TILEWIDTH /2

'''background = pygame.image.load('wall.png').convert_alpha()
background = pygame.transform.scale(background,( 150, 150))'''

for x in range(n):
    for y in range(n):

        cart_x = x * TILEWIDTH_HALF
        cart_y = y*2 * TILEHEIGHT_HALF  
        iso_x = (cart_x - cart_y) 
        iso_y = (cart_x + cart_y)/2
        centered_x = DISPLAYSURF.get_rect().centerx + iso_x - TILEWIDTH_HALF
        centered_y = DISPLAYSURF.get_rect().centery/2.98 + iso_y
        pygame.draw.polygon( DISPLAYSURF , (0,190,0) , [ (centered_x,centered_y)  , (centered_x+TILEWIDTH_HALF,centered_y-TILEHEIGHT_HALF) , (centered_x+TILEWIDTH,centered_y) , (centered_x+TILEWIDTH_HALF,centered_y+TILEHEIGHT_HALF) ])
        pygame.draw.polygon( DISPLAYSURF , (60,60,40) , [ (centered_x,centered_y)  , (centered_x+TILEWIDTH_HALF,centered_y-TILEHEIGHT_HALF) , (centered_x+TILEWIDTH,centered_y) , (centered_x+TILEWIDTH_HALF,centered_y+TILEHEIGHT_HALF) ] , epaisseur(n))
        #DISPLAYSURF.blit(background, (centered_x, centered_y))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
 
    pygame.display.flip()
    FPSCLOCK.tick(30)