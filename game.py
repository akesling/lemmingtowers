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
NUM_LEMS = 10
lemsAlive = 0
TILE_WIDTH = 40

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

    def update(self, deltaT):
        if self.position[0] == SCREEN_SIZE[0] or self.position[1] == SCREEN_SIZE[1] or self.position[0] == 0 or self.position[1] == 0:
            self.speed = 0

        self.speed += (self.k_up + self.k_down)
        if self.speed > self.MAX_FORWARD_SPEED:
            self.speed = self.MAX_FORWARD_SPEED
        if self.speed < 0:
            self.speed = 0

#        self.direction = (self.k_right + self.k_left)
        x, y = self.position
        rad = self.direction * math.pi / 180
        x += self.speed * math.sin(rad)
        y += self.speed * math.cos(rad)
        self.position = (x, y)

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
    def __init__(self, position, image="images/default-tile_8.gif", orient="N"):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load(image)
        self.position = (position[0]*TILE_WIDTH + (TILE_WIDTH/2), \
            position[1]*TILE_WIDTH + (TILE_WIDTH/2))
        self.image = self.src_image
        self.rect = self.image.get_rect()
        self.orient = { "N":0,
            "S":180,
            "E":90,
            "W":270}[orient]
        self.image = pygame.transform.rotate(self.image, self.orient)

    def update(self, deltaT):
        self.position = self.position
        self.rect.center = self.position
	
    def rotate(self):
        self.image = pygame.transform.rotate(self.image, 90)
        self.orient = self.orient + 90
        if self.orient == 360:
            self.orient = 0
		

# Define the random direction chooser
random.seed(time.time())

# Define the tower/lemming groups that will be on the map
rect = screen.get_rect()
lemminggroup = pygame.sprite.RenderPlain()  # Add it to the lemming group
towergroup = pygame.sprite.RenderPlain()
tilegroup = pygame.sprite.RenderPlain()

# Randomly create towers
for i in range(0, 100):
    tilegroup.add(Tile((random.randint(0, 24), random.randint(0, 15)), "images/l.png"))


def updateBoard():
    lemminggroup.update(deltaT)  # Update the positions of our objects
    towergroup.update(deltaT)
    tilegroup.update(deltaT)

    # Redraw our object positions
    lemminggroup.draw(screen)
    towergroup.draw(screen)
    tilegroup.draw(screen)


def detectCollisions():
    # See if our lemming collided with anything
    for l in lemminggroup:
        if pygame.sprite.spritecollide(l, towergroup, False):  # Collision with a tower
            l.direction += random.choice((90, -90))  # Rotate either left or right



# Start the game loop
framecount = 0
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
