import sys
import pygame
from pygame.locals import *

###############################################################################
bg = "assets/bg.png"

tileDict = {
    "-" : "assets/wall-width.png",
    "|" : "assets/wall-height.png",
    "T" : "assets/wall-all.png",
    "'" : "assets/wall-top.png",
    "F" : "assets/wall-righttopbot.png",
    "7" : "assets/wall-lefttopbot.png",
    "L" : "assets/wall-righttop.png",
    "/" : "assets/wall-lefttop.png",

    "." : "assets/empty.png"
}

class Map() :

    # méthode exécutée à l'appel de la classe Map
    # avec un nom de fichier en argument
    def __init__(self, fileName) :
        # exécute la méthode loadMap() avec le nom du fichier en argument
        self.loadMap(fileName)
        # exécute aussi la méthode loadTiles()
        self.loadTiles()

    # méthode stockant les chaînes de caractère venant du fichier de la map
    # dans une liste 'map'
    def loadMap(self, fileName) :
        # définition de la liste 'map'
        self.map = []

        # ouvre le fichier en mode 'read only' et lui assigne la variable 'f'
        with open(fileName, "r") as f :
            # on appelle 'line' chaque ligne de texte extraite du fichier avec
            # la fonction readlines()
            for line in f.readlines() :
                # on ajoute à la liste 'map' ces lignes les unes après les
                # autres en enlevant le caractère de retour à la ligne
                self.map.append(line.rstrip())

    # méthode chargeant les images des tiles dans un dictionnaire
    def loadTiles(self) :

        # définition du dictionnaire 'tiles'
        self.tiles = { }

        # on parcourt le dictionnaire 'tileDict' et on nomme tileSymbol chaque
        # élément du dictionnaire en ayant la possibilité de faire quelque chose avec
        # à chaque fois
        for tileSymbol in tileDict :
            # on récupère le chemin vers l'image stocké dans le dictionnaire
            # 'tileDict' et on le stocke dans la variable 'tilePath'
            tilePath = tileDict[tileSymbol]
            # on ajoute à 'tiles' le chemin vers chaque image
            self.tiles[tileSymbol] = pygame.image.load(tilePath).convert_alpha()

    # méthode pour faire le rendu de la carte
    def render(self) :

        for y, line in enumerate(self.map) :
            for x, char in enumerate(line) :
                ecran.blit(self.tiles[char], (x * tailleTile, y * tailleTile))

    # méthode pour déterminer si le prochain tile est traversable
    # on donne la position du dit tile en argument (x, y)
    def isWalkable(self, x, y) :
        # on regarde, dans la liste 'map', si le prochain tile sera un '.'
        if self.map[y][x] == "." :
            # si oui on renvoit le résultat 'true'
            return True
        else :
            return False

###############################################################################

#définition d'un dictionnaire contenant les chemins vers les sprites du perso
spritesDict = {
    "up"    : "assets/hero_up.png",
    "down"  : "assets/hero_down.png",
    "left"  : "assets/hero_left.png",
    "right" : "assets/hero_right.png"
}


class Perso() :

    # méthode s'exécutant à l'initialisation de la classe Perso
    # en donnant en paramètre la position du perso
    def __init__(self, initialPosition) :

        self.loadSprites()
        # déclare une variable de direction en lui indiquant une valeur par
        # défaut
        self.currentDirection = "down"
        # XXX
        (self.x, self.y) = initialPosition

    def loadSprites(self) :

        self.sprites = { }

        for sprite in spritesDict :

            spritePath = spritesDict[sprite]
            self.sprites[sprite] = pygame.image.load(spritePath)

    def look(self, direction) :

        self.currentDirection = direction

    def move(self, dx, dy) :

        nextTileIsWalkable = laMap.isWalkable(self.x + dx, self.y + dy)

        if (nextTileIsWalkable) :
            self.x += dx
            self.y += dy

    def render(self) :

        currentSprite = self.sprites[self.currentDirection]

        ecran.blit(currentSprite, (self.x * tailleTile, (self.y - 0.5) * tailleTile))

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
        lePerso.look("left")
        lePerso.move(-1, 0)
    if key == pygame.K_RIGHT :
        lePerso.look("right")
        lePerso.move(1, 0)
    if key == pygame.K_UP :
        lePerso.look("up")
        lePerso.move(0, -1)
    if key == pygame.K_DOWN :
        lePerso.look("down")
        lePerso.move(0, 1)

###############################################################################

# Initialise PyGame
pygame.init()

# Défini le nombre de FPS (Frames Per Second)
fps = 30
fpsClock = pygame.time.Clock()

# Défini la taille d'un tile en px
tailleTile = 64
# Défini la taille de la map en tiles
largeur = 20
hauteur = 10

# Setup the ecran
titreFenetre = "My Game"
ecran = pygame.display.set_mode((largeur * tailleTile, hauteur * tailleTile))
pygame.display.set_caption(titreFenetre)

# Init/load the map
laMap = Map("mapComplexe.asc")

# Init/load hero
lePerso = Perso((1,1))

# Main loop
while (True) :

    # Effacer l'ecran
    ecran.fill((10, 10, 10))

    # Gerer les events
    eventHandler()

    # Afficher la map puis le hero
    laMap.render()
    lePerso.render()

    # Update ecran
    pygame.display.update()
    fpsClock.tick(fps)

###############################################################################
