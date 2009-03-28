import math
import pygame
from pygame.locals import *
import random
import sys
import time

# Game settings
SCREEN_SIZE = (1024, 768)
screen = pygame.display.set_mode(SCREEN_SIZE)
BACKGROUND = (0, 0, 0)
clock = pygame.time.Clock()
FRAMERATE = 30
NUM_LEMS = 1
lemsAlive = 0
TILE_WIDTH = 40

def importLevel():
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		print "Must provide a level"
		exit();

	tiles = []

	level = open(filename, "r")
	for space in level:
		space = map((lambda x: x.split(',')), space.strip().split(':'))
		space[0] = map(int, space[0])
		tiles.append(space)
	
	for tile in tiles:
		if tile[1][0] in ('RPath', 'IPath', 'LPath', 'TPath'):
			tilegroup.add(Tile(tile[0], tile[1][0], tile[2][0]))
	
def mouseControl():
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            for tile in tilegroup:
                if (tile.position[0]-20 < mousePos[0] < tile.position[0]+20 \
                and tile.position[1]-20 < mousePos[1] < tile.position[1]+20):
                    tile.rotate()

class Lemming(pygame.sprite.Sprite):
    MAX_FORWARD_SPEED = 10
    TURN_SPEED = 5
    ACCELERATION = 2

    def __init__(self, position, image="images/lemming.png"):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load(image)
        self.position = position
        self.speed = 2
        self.direction = 0
        self.k_left = self.k_right = self.k_up = self.k_down = 0
        self.shouldMove = 1

    def update(self, deltaT):
        if self.position[0] >= SCREEN_SIZE[0] or self.position[1] >= SCREEN_SIZE[1] or self.position[0] <= 0 or self.position[1] <= 0:
            self.direction += random.choice((90, -90))  # Rotate either left or right

        if self.shouldMove == 1:
            x, y = self.position
            rad = self.direction * math.pi / 180
            x += self.speed * math.sin(rad)
            y += self.speed * math.cos(rad)
            self.position = (x, y)
            print "Moving..."
        else:
            print "Not moving..."
            self.shouldMove = 1

        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position



class Tower(pygame.sprite.Sprite):
    def __init__(self, position, image="images/tower.png"):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load(image)
        self.position = (position[0]*TILE_WIDTH + (TILE_WIDTH/2), \
            position[1]*TILE_WIDTH + (TILE_WIDTH/2))
        self.image = self.src_image
        self.rect = self.image.get_rect()

    def update(self, deltaT):
        self.position = self.position
        self.rect.center = self.position


class Tile(pygame.sprite.Sprite):
    def __init__(self, position, tile_type="default", orient="N"):
        pygame.sprite.Sprite.__init__(self)
        
        self.position = (position[0]*TILE_WIDTH + (TILE_WIDTH/2), \
            position[1]*TILE_WIDTH + (TILE_WIDTH/2))
         
        self.type = tile_type
        image = { "Default":"tiles/landscape/default.gif",
            "LPath":"tiles/landscape/lpath.png",
            "TPath":"tiles/landscape/tpath.png",
            "XPath":"tiles/landscape/xpath.png",
            "IPath":"tiles/landscape/ipath.png"}[self.type]
        
        self.src_image = pygame.image.load(image)
        self.image = self.src_image
        self.orient = { 
            "N":0,
            "S":180,
            "E":90,
            "W":270 
        }[orient]
        self.image = pygame.transform.rotate(self.image, self.orient)
        self.rect = self.image.get_rect()

    def update(self, deltaT):
        self.position = self.position
        self.rect.center = self.position

    def rotate(self):
        self.image = pygame.transform.rotate(self.image, 90)
        self.orient = self.orient + 90
        if self.orient == 360:
            self.orient = 0



def updateBoard():
    towergroup.update(deltaT)
    tilegroup.update(deltaT)
    lemminggroup.update(deltaT)  # Update the positions of our objects

    # Redraw our object positions
    towergroup.draw(screen)
    tilegroup.draw(screen)
    lemminggroup.draw(screen)



def detectCollisions():
    # See if our lemming collided with anything
    for l in lemminggroup:
        if pygame.sprite.spritecollide(l, towergroup, False):  # Collision with a tower
            l.direction += random.choice((90, -90))  # Rotate either left or right
            print l.direction
            l.shouldMove = 0
            l.position



# Define the random direction chooser
random.seed(time.time())

# Define the tower/lemming groups that will be on the map
rect = screen.get_rect()
towergroup = pygame.sprite.RenderPlain()
tilegroup = pygame.sprite.RenderPlain()
lemminggroup = pygame.sprite.RenderPlain()  # Add it to the lemming group


#for i in range(0, 100):  # Randomly create towers
#    towergroup.add(Tower((random.randint(0, 24), random.randint(0, 15))))
#for i in range(0, 100):  # Randomly create tiles
#    tilegroup.add(Tile((random.randint(0, 24), random.randint(0, 15)), "l"))



# Start the game loop
framecount = 0
importLevel()
while 1:
    framecount = (framecount + 1) % FRAMERATE

    # Create more lemmings if we don't have enough
    if framecount == 1 and lemsAlive < NUM_LEMS:
        lemminggroup.add(Lemming((100, 100)))  # Add it to the lemming group
        lemsAlive += 1

    # Update everything and redraw the board
    deltaT = clock.tick(30)  # Controll the framerate (which controls game speed)
    screen.fill(BACKGROUND)  # Background color
    updateBoard()
    detectCollisions()
    pygame.display.flip()
    mouseControl() #Rotate tiles on mouse click
