import pygame
pygame.init()                                       # Pygame setup
#---------------------     GRAPHISME & FENETRE ----------------------------------------
WIDTH, HEIGHT = 600, 600                            # dimensions
GRID_SIZE = 3                                       # éléments de la grille
LINE_COLOR = (200, 0, 0)                            # éléments de la grille
LINE_WIDTH = 30                                     # éléments de la grille
screen = pygame.display.set_mode((WIDTH, HEIGHT))   # affiche la fenêtre de jeux
pygame.display.set_caption("Morpion")               # titre de la fenêtre de jeux
fond_big = pygame.image.load('fond.jpg')            # image de fond
fond = pygame.transform.scale(fond_big, (600, 600)) # mise à l'echelle de l'image de fond


#----------------------     VARIABLES   -----------------------------------------------
clock = pygame.time.Clock()                         # système d'horloge
clock.tick(60)                                      # limite le nombre d'exécutions par seconde (fréquence d'affichage)
game_over = False
waiting_for_click = False
current_player = 'x'
run = True
restart = "Cliquez pour rejouer"
board = [                                           # liste des cases
    ((5, 5), 185, 185),                             # case 1 (origine, largeur, hauteur)
    ((210, 5), 180, 185),                           # case 2
    ((410, 5), 185, 185),                           # case 3
    ((5, 210), 185, 180),                           # case 4
    ((210, 210), 180, 180),                         # case 5
    ((410, 210), 185, 180),                         # case 6
    ((5, 410), 185, 185),                           # case 7
    ((210, 410), 180, 185),                         # case 8
    ((410, 410), 185, 185)                          # case 9
]

# signes = [ liste de dictionnaire {chaine vide, centrées sur les cases} ]
#            chaine    ,     position    (origine x  + largeur //2,  origine y + hauteur //2)
signes = [{ 'signe': '',    'position':  (case[0][0] + case[1] //2, case[0][1] + case[2] //2)  } for case in board]

# signes = [
#   { 'signe': '',    'position':  centre de la case   }
#   { 'signe': '',    'position':  centre de la case   } 
#   { 'signe': '',    'position':  centre de la case   }
#   etc...
# ]

#----------------------     FONCTIONS   ----------------------------------------------
def check_winner(signes):
    # Vérification des lignes horizontales
    for row in range(0, 9, 3):                                                                 # row = (0,3,6)
        if signes[row]['signe'] == signes[row + 1]['signe'] == signes[row + 2]['signe'] != '': # non vide et identique
    #      signes [0]['signe']  == signes [1]['signe']      == signes [2]['signe']  -> signe des cases 0,1 et 2 (ligne 1)
    #      signes [3]['signe']  == signes [4]['signe']      == signes [5]['signe']  -> signe des cases 3,4 et 5 (ligne 2)
    #      signes [6]['signe']  == signes [7]['signe']      == signes [8]['signe']  -> signe des cases 6,7 et 8 (ligne 3)
            return signes[row]['signe']             #  retourne le signe de la ligne

    # Vérification des lignes verticales
    for col in range(3):                                                                       # col = (0,1,2)
        if signes[col]['signe'] == signes[col + 3]['signe'] == signes[col + 6]['signe'] != '': # signe des cases 0,3 et 6 (colonne 1)
            return signes[col]['signe']

    if signes[0]['signe'] == signes[4]['signe'] == signes[8]['signe'] != '':    # signe des cases 0,4 et 8 (diagonale de gauche à droite)
        return signes[0]['signe']

    if signes[2]['signe'] == signes[4]['signe'] == signes[6]['signe'] != '':    # signe des cases 2,4 et 6 (diagonale dedroite à gauche)
        return signes[2]['signe']
    
    if all(signe['signe'] != '' for signe in signes):      # grille pleine = match nul
        return 'nul'  

    return None  # Aucun gagnant pour le moment

def draw_cross(position):                           # dessine x                          
    line1_start = (position[0] - 70, position[1] -70)   # ajuste les coordonnées
    line1_end = (position[0] + 70, position[1] + 70)    # de départ et d'arrêt des lignes
    line2_start = (position[0] - 70, position[1] + 70)  # pour centrer le point de positionnement
    line2_end = (position[0] + 70, position[1] -70)     # sur le croisement des lignes
    line_thickness = 35
    vert = (70, 200, 70)
    for line in [
        {'color': vert, 'start': line1_start, 'end': line1_end, 'thickness': line_thickness},
        {'color': vert, 'start': line2_start, 'end': line2_end, 'thickness': line_thickness}
    ]: #pygame.draw.line(surface,    color    ,   start_pos  ,  end_pos   , width            )
        pygame.draw.line(screen, line['color'], line['start'], line['end'], line['thickness'])

def draw_round(center):                             # dessine o                         
    pygame.draw.circle(screen, (50,50,230), (center), 80, 35) # circle(surface, color, center, radius, épaisseur)

def draw_grid():                                    # dessine la grille
    for i in range(1, GRID_SIZE):                                                                                           # Lignes horizontales  
        pygame.draw.line(screen, LINE_COLOR, (0, i * HEIGHT // GRID_SIZE), (WIDTH, i * HEIGHT // GRID_SIZE), LINE_WIDTH)    # l'opérateur // retourne le quotient de la division entre deux nombres. 10 // 3 donnera 3.
                                                                                                                            # i=1     début (0, 200)             , fin (600,200)
                                                                                                                            # i=2     début (0, 400)             , fin (600,400)
                                                                                                                            # Lignes verticale
        pygame.draw.line(screen, LINE_COLOR, (i * WIDTH // GRID_SIZE, 0), (i * WIDTH // GRID_SIZE, HEIGHT), LINE_WIDTH)     # i=1     début 600//3= (200, 0)    ,  fin  600//3=(200,600)
                                                                                                                            # i=2     début 1200//3= (400, 0)   ,  fin 1200//3=(400,600)

def display_message(message):
    font = pygame.font.Font(None, 50)                   # police et des messages
    text = font.render(message, True, (220, 220, 50))   # couleur des messages
    background_color = (50, 50, 50, 220)                # défini la couleur d'un fond semi-transparent (RGBA)
    background_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)   # défini une surface pour le fond semi-transparent
    background_surface.fill(background_color)           # attribue la couleur à la surface
    screen.blit(background_surface, (0, 0))             # Dessine la surface
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - (text.get_height()*2) // 2)) # Dessine le texte
    # centré horizontalement : moitié de la largeur de l'écran - moitié de la largeur du texte,
    # centré verticalement : moitié de la hauteur de l'écran - moitié de la hauteur du texte.

def display_restart(restart):
    font = pygame.font.Font(None, 50)                   # police et des messages
    text = font.render(restart, True, (220, 220, 50))   # couleur des messages
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + (text.get_height()*2) // 2)) # Dessine le texte


def reset_game():
    global signes, current_player, game_over
    signes = [{'signe': '', 'position': (case[0][0] + case[1] // 2, case[0][1] + case[2] // 2)} for case in board]
    current_player = 'x'
    game_over = False


#----------------------     BOUCLE   ----------------------------------------------
while run:                                                                      # pygame.event.get() renvoie un tableau avec tous les événements en cours
    for event in pygame.event.get():                                            # ces événements vont dans l'objet "event"
        if event.type == pygame.QUIT:                                           # si clic sur X 
            run = False                                                         # arrête la boucle
        elif not game_over and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # clic
            pos = event.pos                                                     # position du clic de la souris

            for signe in signes:                                                # signes = liste de chaine de caractère vide, centrées sur les cases
                if signe['signe'] == '' and signe['position'][0] - 75 < pos[0] < signe['position'][0] + 75 and signe['position'][1] - 75 < pos[1] < signe['position'][1] + 75:
                    signe['signe'] = current_player                             # current_player = 'x'
                    current_player = 'o' if current_player == 'x' else 'x'      # Alterne les joueurs
   
    background_rect = fond.get_rect()                                           # fond gris semi transparent
    screen.blit(fond, background_rect)                                          # Afficher l'image de fond    
    draw_grid()                                                                 # Dessine la grille

    for signe in signes:                                                        # dessine x ou o selon le joueur
        if signe['signe'] == 'x':
            draw_cross(signe['position'])
        elif signe['signe'] == 'o':
            draw_round(signe['position'])

    pygame.display.flip()                                                       # Affiche tout ce qui doit être affiché (est nécessaire à partir du moment on dessine quelque chose)
    winner = check_winner(signes)                                               # Vérifie si un joueur gagne

    if winner  or all(signe['signe'] != '' for signe in signes):                # Affiche le message du gagnant
        game_over = True

        if winner == 'nul':
            message = "Match nul !"
        else:
            message = f"Joueur {winner} gagne la partie !"

        display_message(message)
        display_restart(restart)
        pygame.display.flip()

        waiting_for_click = True
        while waiting_for_click:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    waiting_for_click = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    reset_game()
                    waiting_for_click = False
                    game_over = False