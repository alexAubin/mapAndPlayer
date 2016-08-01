import sys
import pygame
from pygame.locals import *

###############################################################################

tileDict = {
    "#" : "assets/wall.png",
    "." : "assets/empty.png"
}

class Map() :

    def __init__(self, fileName) :

        self.loadMap(fileName)
        self.loadTiles()

    def loadMap(self, fileName) :

        self.map = []

        with open(fileName, "r") as f :
            for line in f.readlines() :
                self.map.append(line.rstrip())

    def loadTiles(self) :

        self.tiles = { }

        for tileSymbol in tileDict :

            tilePath = tileDict[tileSymbol]
            self.tiles[tileSymbol] = pygame.image.load(tilePath)

    def render(self) :

        for y, line in enumerate(self.map) :
            for x, char in enumerate(line) :
                screen.blit(self.tiles[char], (x * tileSize, y * tileSize))

    def isWall(self, x, y) :

        return (self.map[y][x] == "#")
    
###############################################################################

spritesDict = {
    "up"    : "assets/hero_up.png",
    "down"  : "assets/hero_down.png",
    "left"  : "assets/hero_left.png",
    "right" : "assets/hero_right.png"
}

class Hero() :

    def __init__(self, initialPosition) :

        self.loadSprites()
        self.currentDirection = "down" 
        (self.x, self.y) = initialPosition

    def loadSprites(self) :

        self.sprites = { }

        for sprite in spritesDict :

            spritePath = spritesDict[sprite]
            self.sprites[sprite] = pygame.image.load(spritePath)

    def look(self, direction) :

        self.currentDirection = direction

    def move(self, dx, dy) :

        nextTileIsAWall = theMap.isWall(self.x + dx, self.y + dy)

        if not (nextTileIsAWall) :
            self.x += dx
            self.y += dy

    def render(self) :

        currentSprite = self.sprites[self.currentDirection]
        
        screen.blit(currentSprite, (self.x * tileSize, self.y * tileSize))

###############################################################################

def eventHandler() :

    # Check if user clicked the close button
    for event in pygame.event.get():

        if (event.type == pygame.QUIT) :
            pygame.quit()
            sys.exit()

        if (event.type == pygame.KEYDOWN) :
            keysHandler(event.key)

def keysHandler(key) :

    if key == pygame.K_LEFT :
        theHero.look("left")
        theHero.move(-1, 0)
    if key == pygame.K_RIGHT :
        theHero.look("right")
        theHero.move(1, 0)
    if key == pygame.K_UP :
        theHero.look("up")
        theHero.move(0, -1)
    if key == pygame.K_DOWN :
        theHero.look("down")
        theHero.move(0, 1)

###############################################################################

# Initialize PyGame
pygame.init()

# Set up FPS clock
fps = 30
fpsClock = pygame.time.Clock()

# Map width (in tile units)
tileSize = 32
width  = 10
height = 10

# Setup the screen
windowLabel = "My Game"
screen = pygame.display.set_mode((width * tileSize, height * tileSize), 0, 32)
pygame.display.set_caption(windowLabel)
screen.fill( (0,0,0) )

# Init/load the map
theMap = Map("map.asc")

# Init/load hero
theHero = Hero((1,1))

theHero.move(0,1)

# Main loop
while (True) :

    # Effacer l'ecran
    screen.fill((10, 10, 10))

    # Gerer les events
    eventHandler()

    # Afficher la map puis le hero
    theMap.render()
    theHero.render()

    # Update screen
    pygame.display.update()
    fpsClock.tick(fps)

###############################################################################



