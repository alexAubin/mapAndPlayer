import sys
import pygame
from pygame.locals import *

###############################################################################
tile_dict = {
    "─": "assets/wall-width.png",
    "│": "assets/wall-height.png",
    "┬": "assets/wall-all.png",
    "╵": "assets/wall-top.png",
    "┌": "assets/wall-righttopbot.png",
    "┐": "assets/wall-lefttopbot.png",
    "└": "assets/wall-righttop.png",
    "┘": "assets/wall-lefttop.png",

    ".": "assets/empty.png",
    "■": "assets/bloc.png",
    "□": "assets/interrupteur.png",
    "▣": "assets/blocActive.png"

}

class Map() :
    """ Classe recueillant toutes les méthodes relatives à la gestion de la map """

    # Méthode exécutée à l'appel de la classe Map
    def __init__(self, fileName):
        """ Exécute les méthodes chargeant la map et les images en mémoire """

        self.load_map(fileName)
        self.load_tiles()

    def load_map(self, fileName):
        """ Transforme le fichier de la map en une liste à 2 niveaux que
        l'on pourra modifier. Cette liste servira à l'affichage de la map.
        """

        # Défini une liste vide dans laquelle nous allons stocker les lignes
        self.map = []

        # Ouvre le fichier en mode 'read only' et lui assigne la variable 'f'
        with open(fileName, "r") as f:
            # Pour chaque ligne ('L') du fichier, on transforme son contenu en
            # une liste de caractères et on l'ajoute à la liste 'map'
            for L in f:
                # On se débarasse aussi du caractère de passage à la ligne '\n'
                self.map.append(list(L.strip("\n")))

    def load_tiles(self):
        """ Charge les images des tiles dans un dictionnaire """

        # Défini un dictionnaire 'tiles' vide
        self.tiles = { }

        # Parcourt le dictionnaire 'tile_dict' et on nomme 'tile_symbol' chaque
        # élément du dictionnaire ce qui offre la possibilité de faire quelque
        # chose avec à chaque itération de la boucle 'for'
        for tile_symbol in tile_dict:
            # Récupère le chemin vers l'image stockée dans le dictionnaire
            # 'tile_dict' et on le stocke dans la variable 'tile_path'
            tile_path = tile_dict[tile_symbol]
            # Ajoute à 'tiles' un caractère en clé et une image chargée en valeur
            self.tiles[tile_symbol] = pygame.image.load(tile_path).convert_alpha()

    def render(self):
        """ Affiche le rendu de la carte sur l'écran """

        # Parcourt toutes les coordonnées x,y de la map
        for x in range(width):
            for y in range(heigth):
                # Récupère le caractère associé à cette coordonnée x,y
                caractere = self.map[y][x]
                # Récupère l'image associé à ce caractère dans la liste 'tiles'
                tile_image = self.tiles[caractere]
                # Afficher l'image sur l'écran
                ecran.blit(tile_image, (x * taille_tile, y * taille_tile))

    def walkable(self, x, y):
        """ Détermine si le prochain tile est traversable """

        # on regarde dans la liste 'map' si le prochain tile est traversable
        # on parcourt les lignes d'abord (y) puis le caractère dans la chaîne (x)
        if self.map[y][x] == "." or self.map[y][x] == "□":
            # si oui on renvoit le boléen 'True'
            return True
        # Sinon implicitement la fonction renvoit 'None'

    def pushable(self, x, y, dx, dy):
        """ Détermine si le prochain tile est poussable """

        # On récupère la valeur du tile que l'on veut pousser dans le tableau 'map'
        next_tile = self.map[y + dy][x + dx]
        # On récupère aussi la valeur du tile derrière l'élément à pousser
        after_next_tile = self.map[y + dy*2][x + dx*2]

        # Différents comportement à prévoir suivant les cas de figures
        if next_tile == "■":
            if after_next_tile == ".":
                self.map[y + dy][x + dx] = "."
                self.map[y + dy*2][x + dx*2] = "■"
                return True
            elif after_next_tile == "□":
                self.map[y + dy][x + dx] = "."
                self.map[y + dy*2][x + dx*2] = "▣"
                return True
        elif next_tile == "▣":
            if after_next_tile == "." :
                self.map[y + dy][x + dx] = "□"
                self.map[y + dy*2][x + dx*2] = "■"
                return True

    def victory_condition(self) :
        """ Check si les conditions de victoires sont remplies """

        # Parcours le tableau de la map
        for y in self.map :
            for x in y :
                # S'il y a encore un socle, le jeu continu
                if x == "□" :
                    return False
        # Sinon charge la map avec les félicitations :
        # Parce que si le return False est exécuté, le reste de la méthode
        # ne sera pas exécuté
        self.load_map("maps/youWin.asc")


###############################################################################

# défini un dictionnaire contenant les chemins vers les sprites du perso
sprites_dict = {
    "up"   : "assets/hero_up.png",
    "down" : "assets/hero_down.png",
    "left" : "assets/hero_left.png",
    "right": "assets/hero_right.png"
}


class Perso() :
    """ Classe recueillant toutes les méthodes relatives à la gestion du perso """

    def __init__(self, initial_position) :
        """ Exécute les méthodes chargeant les images du perso en mémoire et
            donnant une position initiale au personnage.
        """

        self.load_sprites()
        self.replace_hero(initial_position)

    def load_sprites(self) :
        """ Charge les sprites en mémoire et les stocke dans un dictionnaire """

        self.sprites = { }

        # Parcourt le dictionnaire 'sprites_dict' et on nomme 'sprite' chaque
        # élément du dictionnaire
        for sprite in sprites_dict :
            # Stocke le chemin vers l'image dans la variable 'sprite_path'
            sprite_path = sprites_dict[sprite]
            # Ajoute à 'sprites' une direction en clé et une image chargée en valeur
            self.sprites[sprite] = pygame.image.load(sprite_path)

    def look(self, direction) :
        """ Défini la direction dans laquelle le personnage regarde """

        self.current_direction = direction

    def move(self, dx, dy) :
        """ Gère le déplacement du personnage """

        # Détermine si le prochain tile est traversable/poussable en stockant
        # la valeur renvoyée par les méthodes de la classe 'Map' dans des
        # nouvelles variables
        next_tile_is_walkable = laMap.walkable(self.x + dx, self.y + dy)
        next_tile_is_pushable = laMap.pushable(self.x, self.y, dx, dy)

        # Si ces méthodes renvoit 'True' la position du personnage change
        if (next_tile_is_walkable) or (next_tile_is_pushable) :
            self.x += dx
            self.y += dy

    def replace_hero(self, initial_position):
        """ Défini un sprite de direction par défaut et une position
            donnée en argument.
        """

        # Déclare une variable de direction en lui indiquant une valeur par défaut
        self.current_direction = "down"
        # Défini la position initiale du personnage avec le tuple donné en argument
        (self.x, self.y) = initial_position


    def render(self) :
        """ Affiche le sprite du personnage sur l'écran """

        # Défini l'image à afficher en récupérant l'image chargée dans le
        # dictionnaire suivant la direction du personnage
        current_sprite = self.sprites[self.current_direction]

        # Affiche le sprite du perso sur l'écran à la bonne position
        ecran.blit(current_sprite, (self.x * taille_tile, (self.y - 0.5) * taille_tile))

###############################################################################

def event_handler() :
    """ Observe et réagit aux actions du joueurs """

    for event in pygame.event.get():
        # Si le joueur utilise un événement 'QUIT'
        if (event.type == pygame.QUIT) :
            pygame.quit()
            sys.exit()
        # Si le joueur enfonce une touche
        if (event.type == pygame.KEYDOWN) :
            # Exécute la fonction
            keys_handler(event.key)

def keys_handler(key) :
    """ Gère les actions à effectuer suivant la touche enfoncée """

    # la touche 'r' reset le niveau
    if key == pygame.K_r :
        laMap.load_map("maps/sokobanMap.asc")
        lePerso.replace_hero((8,3))

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
fps_clock = pygame.time.Clock()

# Défini la taille d'un tile en px
taille_tile = 64
# Défini la taille de la map en tiles
width = 20
heigth = 11

# Setup l'écran, 'ecran' sera la variable sur laquelle blitter les images
ecran = pygame.display.set_mode((width * taille_tile, heigth * taille_tile))
# Donne un nom à la fenêtre
pygame.display.set_caption("My Game")

# Initialise et charge la map
laMap = Map("maps/sokobanMap.asc")

# Initialise et charge le personnage
lePerso = Perso((8,3))

# Boucle principale et infinie
while (True) :

    # Efface l'ecran
    ecran.fill((10, 10, 10))

    # Check si les conditions de victoire sont remplies
    laMap.victory_condition()

    # Gèrer les événements
    event_handler()

    # Blitte la map puis le hero
    laMap.render()
    lePerso.render()

    # met à jour l'écran
    pygame.display.update()
    fps_clock.tick(fps)

###############################################################################
