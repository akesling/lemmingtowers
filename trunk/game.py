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
        if tile[1][0] in ('IPath', 'LPath', 'TPath', 'IRiver', 'LRiver', 'TRiver'):
            tilegroup.add(Tile(tile[0], tile[1][0], tile[2][0]))
        if tile[1][0] in ('XPath', 'Default', 'Tower', 'Pit'):
            tilegroup.add(Tile(tile[0], tile[1][0]))
    
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

    def rotate(self):
        self.direction += random.choice((90, -90))  # Rotate either left or right

    def backtrack(self):  # Go back two spaces if we entered the wrong tile
        x, y = self.position
        rad = self.direction * math.pi / 180
        x -= self.speed * math.sin(rad)
        y -= self.speed * math.cos(rad)

    def update(self, deltaT):
        if self.position[0] >= SCREEN_SIZE[0] or self.position[1] >= SCREEN_SIZE[1] or self.position[0] <= 0 or self.position[1] <= 0:
            self.rotate()

        if self.shouldMove == 1:  # Don't move into a space if it's an invalid space!
            x, y = self.position
            rad = self.direction * math.pi / 180
            x += self.speed * math.sin(rad)
            y += self.speed * math.cos(rad)
            self.position = (x, y)

            if self.position

#            print "Moving..."
        else:
#            print "Not moving..."
            self.shouldMove = 1

        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position



def getTile(x, y):
    gridValue = (int(x/40), int(y/40))
    for tile in tilegroup:
        if int(x/40) <= tile.position <= (int(x/40)+40):
            return tile



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
            "Pit":"tiles/pit.gif",
            "Tower":"tiles/tower.gif",
            "IRiver":"tiles/landscape/iriver.gif",
            "LRiver":"tiles/landscape/lriver.gif",
            "TRiver":"tiles/landscape/triver.gif",
            "LPath":"tiles/landscape/lpath.png",
            "TPath":"tiles/landscape/tpath.png",
            "XPath":"tiles/landscape/xpath.png",
            "IPath":"tiles/landscape/ipath.png"}[self.type]
        
        self.src_image = pygame.image.load(image)
        self.image = self.src_image
        self.rect = self.image.get_rect()
        

        self.validEntrances = ()
        if self.type == "LPath":
            self.validEntrances = ["N", "E"]
        elif self.type == "TPath":
            self.validEntrances = ["N", "E", "W"]
        elif self.type == "XPath":
            self.validEntrances = ["N", "E", "S", "W"]
        else:
            self.validEntrances = ["N", "S"]

        self.orient = { 
            "N":0,
            "E":90,
            "S":180,
            "W":270
        }[orient]
        for i in range(0, self.orient/90):  # Rotate right until we're in the specified orientation
            self.rotate()

    def canEnter(self, origin):
        if origin == 0:
            origin = "N"
        elif origin == 90:
            origin = "E"
        elif origin == 180:
            origin = "S"
        else:
            origin = "W"

        if origin in self.validEntrances:
            return True
        else:
            return False

    def update(self, deltaT):
        self.position = self.position
        self.rect.center = self.position

    def rotate(self):
        self.image = pygame.transform.rotate(self.image, 90)
        self.orient = self.orient + 90
        if self.orient == 360:
            self.orient = 0

        # Account for rotation in the list of valid entrances
        for entrance in self.validEntrances:
            if entrance == "N":
                entrance = "E"
            elif entrance == "E":
                entrance = "S"
            elif entrance == "S":
                entrance = "W"
            else:
                entrance = "N"



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
    deltaT = clock.tick(30)  # Control the framerate (which controls game speed)
    screen.fill(BACKGROUND)  # Background color
    updateBoard()
    detectCollisions()
    pygame.display.flip()
    mouseControl() #Rotate tiles on mouse click
