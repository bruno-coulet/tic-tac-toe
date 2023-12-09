import pygame, sys
#  Pygame setup
pygame.init()
font = pygame.font.Font(None, 24)
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 3
LINE_COLOR = (200, 10, 10)
LINE_WIDTH = 15
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# titre
pygame.display.set_caption("Morpion")
clock = pygame.time.Clock()         # défini un système d'horloge

croix_big = pygame.image.load('croix.png')
croix = pygame.transform.scale(croix_big, (200, 200))
rond_big = pygame.image.load('rond.png')
rond = pygame.transform.scale(rond_big, (200, 200))
fond = pygame.image.load('fond.jpg')

def draw_grid():                    # Fonction pour dessiner la grille
    for i in range(1, GRID_SIZE):   # i=1 puis i=2
        # Lignes horizontales  l'opérateur de division // retourne le quotient de la division entre deux nombres. Exemple : 10 // 3 donnera 3. # quotient faire référence à la partie entière d'une division.
        pygame.draw.line(screen, LINE_COLOR, (0, i * HEIGHT // GRID_SIZE), (WIDTH, i * HEIGHT // GRID_SIZE), LINE_WIDTH)
                                            # début (0, 200)             , fin (600,200)
                                            # début (0, 400)             , fin (600,400)
        # Lignes verticales
        pygame.draw.line(screen, LINE_COLOR, (i * WIDTH // GRID_SIZE, 0), (i * WIDTH // GRID_SIZE, HEIGHT), LINE_WIDTH)
                                            # début 600//3= (200, 0)    ,  fin  600//3=(200,600)
                                            # début 1200//3= (400, 0)   ,  fin 1200//3=(400,600)

case_1 = ((0,0),195, 195)           # défini la case : 190 ou 195 px de côté.
case_2 = ((205,0),190, 195)         # coordonnées, largeur, hauteur
case_3 = ((405,0),195, 195)
case_4 = ((0,205),195, 190)
case_5 = ((205,205),190, 190)
case_6 = ((405,205),190, 190)
case_7 = ((0,405),195, 195)
case_8 = ((205,405),190, 195)
case_9 = ((405,405),190, 195)
cases = (case_1, case_2, case_3, case_4, case_5, case_6, case_7, case_8, case_9)
case_surfaces = [pygame.Surface((case[1], case[2])) for case in cases]

# Initialisation des symboles dans chaque case
symbols = [''] * len(cases)

run = True

while run:                            # pygame.event.get() renvoie un tableau avec tous les événements en cours
    for event in pygame.event.get():  # ces événements vont dans l'objet "event"
        if event.type == pygame.QUIT: # clic sur X 
            run = False               # pour fermer la fenêtre



        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        # Gestion du clic de souris
            for index, (position, width, height) in enumerate(cases):
                if width > event.pos[0] > position[0] and height > event.pos[1] > position[1] and symbols[index] == '':
                    # Vérifier si la case est vide avant de placer le symbole
                    symbols[index] = 'X'  # Vous pouvez changer 'X' à 'O' pour alterner les symboles

    # Dessiner les symboles sur les surfaces des cases
    for index, surface in enumerate(case_surfaces):
        if symbols[index] == 'X':
            surface.blit(croix, (0, 0))
        elif symbols[index] == 'O':
            surface.blit(rond, (0, 0))
        screen.blit(surface, cases[index][0])









    # screen.blit(fond, (0, 0))         # image de fond
    # clock.tick(60)                    # limite le nombre d'exécutions par seconde de la "boucle de jeu"  (fréquence d'affichage)

    # if event.type == pygame.MOUSEBUTTONDOWN : # clic de la souris
    #   if pygame.mouse.get_pressed() == (1,0,0) or pygame.mouse.get_pressed() == (0,1,0) or pygame.mouse.get_pressed() == (0,0,1):
    #     pos = pygame.mouse.get_pos()          # position de la souris
    #     for case in cases:
    #         #AFFICHER CROIX
    #         screen.blit(rond,(pos))
    #         # if pos in case:
    #         #   screen.blit(croix,(pos))  -----   MARCHE PAS

    # Dessine la grille
    draw_grid()
    # Indique à Pygame qu'il faut afficher tout ce qui doit être affiché (est nécessaire à partir du moment on dessine quelque chose)
    pygame.display.flip()
