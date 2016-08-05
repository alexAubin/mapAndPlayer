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

    # methode executee a l'appel de la classe Map
    # avec un nom de fichier en argument
    def __init__(self, fileName) :
        # execute la methode loadMap() avec le nom du fichier en argument
        self.loadMap(fileName)
        # execute aussi la methode loadTiles()
        self.loadTiles()

    # methode stockant les chaines de caractere venant du fichier de la map
    # dans une liste 'map'
    def loadMap(self, fileName) :
        # definition de la liste 'map'
        self.map = []

        # ouvre le fichier en mode 'read only' et lui assigne la variable 'f'
        with open(fileName, "r") as f :
            # on appelle 'line' chaque ligne de texte extraite du fichier avec
            # la fonction readlines()
            for line in f.readlines() :
                # on ajoute a la liste 'map' ces lignes les unes apres les
                # autres en enlevant le caractere de retour a la ligne
                self.map.append(line.rstrip())

    # methode chargeant les images des tiles dans un dictionnaire
    def loadTiles(self) :

        # definition du dictionnaire 'tiles'
        self.tiles = { }

        # on parcourt le dictionnaire 'tileDict' et on nomme tileSymbol chaque
        # element du dictionnaire en ayant la possibilite de faire quelque chose avec
        # a chaque fois
        for tileSymbol in tileDict :
            # on recupere le chemin vers l'image stocke dans le dictionnaire
            # 'tileDict' et on le stocke dans la variable 'tilePath'
            tilePath = tileDict[tileSymbol]
            # on ajoute a 'tiles' le chemin vers chaque image
            self.tiles[tileSymbol] = pygame.image.load(tilePath).convert_alpha()

    # methode pour faire le rendu de la carte
    def render(self) :

        # Parcourir toutes les coordonnees x,y de la map
        for x in range(largeur) :
            for y in range(hauteur) :

                # Recuperer le caractere associe a cette coordonnee x,y
                caractere = self.map[y][x]
                # Recuper l'image associe a ce caractere
                tileImage = self.tiles[caractere]
                # Afficher l'image sur l'ecran
                ecran.blit(tileImage, (x * tailleTile, y * tailleTile))

    # methode pour determiner si le prochain tile est traversable
    # on donne la position du dit tile en argument (x, y)
    def isWalkable(self, x, y) :
        # on regarde, dans la liste 'map', si le prochain tile sera un '.'
        if self.map[y][x] == "." :
            # si oui on renvoit le resultat 'true'
            return True
        else :
            return False

###############################################################################

#definition d'un dictionnaire contenant les chemins vers les sprites du perso
spritesDict = {
    "up"    : "assets/hero_up.png",
    "down"  : "assets/hero_down.png",
    "left"  : "assets/hero_left.png",
    "right" : "assets/hero_right.png"
}


class Perso() :

    # methode s'executant a l'initialisation de la classe Perso
    # en donnant en parametre la position du perso
    def __init__(self, initialPosition) :

        self.loadSprites()
        # declare une variable de direction en lui indiquant une valeur par
        # defaut
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

# Defini le nombre de FPS (Frames Per Second)
fps = 30
fpsClock = pygame.time.Clock()

# Defini la taille d'un tile en px
tailleTile = 64
# Defini la taille de la map en tiles
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
