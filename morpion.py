import pygame, sys, time
pygame.init()                                       # Pygame setup
font = pygame.font.Font(None, 24)
WIDTH, HEIGHT = 600, 600                            # dimensions
GRID_SIZE = 3                                       # éléments de la grille
LINE_COLOR = (200, 0, 0)                          # éléments de la grille
LINE_WIDTH = 30                                     # éléments de la grille
screen = pygame.display.set_mode((WIDTH, HEIGHT))   # affiche la fenêtre de jeux
pygame.display.set_caption("Morpion")               # titre de la fenêtre de jeux
clock = pygame.time.Clock()                         # système d'horloge
fond_big = pygame.image.load('fond.jpg')                # image de fond
fond = pygame.transform.scale(fond_big, (600, 600))
background_rect = fond.get_rect()                   # fond gris semi transparent fin de partie
winner = None
game_over = False
waiting_for_click = False

def draw_cross(position):                           # ajuste les coordonnées de départ et d'arrêt des lignes pour centrer sur le point de croisement des lignes.
    line1_start = (position[0] - 70, position[1] -70)
    line1_end = (position[0] + 70, position[1] + 70)
    line2_start = (position[0] - 70, position[1] + 70)
    line2_end = (position[0] + 70, position[1] -70)
    line_thickness = 35
    for line in [
        {'color': (70, 200, 70), 'start': line1_start, 'end': line1_end, 'thickness': line_thickness},
        {'color': (70, 200, 70), 'start': line2_start, 'end': line2_end, 'thickness': line_thickness}
    ]: #pygame.draw.line(surface,    color    ,   start_pos  ,  end_pos   , width            )
        pygame.draw.line(screen, line['color'], line['start'], line['end'], line['thickness'])

def draw_round(center):                              # circle(surface, color, center, radius, épaisseur)
    pygame.draw.circle(screen, (50,50,230), (center), 80, 35)

def draw_grid():                                    # dessine la grille
    for i in range(1, GRID_SIZE):                                                                                           # Lignes horizontales  
        pygame.draw.line(screen, LINE_COLOR, (0, i * HEIGHT // GRID_SIZE), (WIDTH, i * HEIGHT // GRID_SIZE), LINE_WIDTH)    # l'opérateur // retourne le quotient de la division entre deux nombres. 10 // 3 donnera 3.
                                                                                                                            # i=1     début (0, 200)             , fin (600,200)
                                                                                                                            # i=2     début (0, 400)             , fin (600,400)
                                                                                                                            # Lignes verticale
        pygame.draw.line(screen, LINE_COLOR, (i * WIDTH // GRID_SIZE, 0), (i * WIDTH // GRID_SIZE, HEIGHT), LINE_WIDTH)     # i=1     début 600//3= (200, 0)    ,  fin  600//3=(200,600)
                                                                                                                            # i=2     début 1200//3= (400, 0)   ,  fin 1200//3=(400,600)

def display_message(message):
    font = pygame.font.Font(None, 50)
    text = font.render(message, True, (220, 220, 50))   # couleur et police
    background_color = (50, 50, 50, 220)                # couleur du Fond semi-transparent (RGBA)
    background_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)   # Crée une surface pour le fond semi-transparent
    background_surface.fill(background_color)           # attribue la couleur à la surface
    screen.blit(background_surface, (0, 0))             # Dessine la surface
    # centre le texte horizontalement : moitié de la largeur de l'écran - moitié de la largeur du texte,
    # centre le texte verticalement : moitié de la hauteur de l'écran - moitié de la hauteur du texte.
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2)) # Dessine le texte

    text_surface = font.render(message, True, (255, 255, 255))
    text_rect = text_surface.get_rect()

def check_winner(symbols):
    for row in range(3):
        if symbols[row * 3]['symbol'] == symbols[row * 3 + 1]['symbol'] == symbols[row * 3 + 2]['symbol'] != '':
            return symbols[row * 3]['symbol']  # Le joueur gagne

    for col in range(3):
        if symbols[col]['symbol'] == symbols[col + 3]['symbol'] == symbols[col + 6]['symbol'] != '':
            return symbols[col]['symbol']  # Le joueur gagne

    if symbols[0]['symbol'] == symbols[4]['symbol'] == symbols[8]['symbol'] != '':
        return symbols[0]['symbol']  # Le joueur gagne

    if symbols[2]['symbol'] == symbols[4]['symbol'] == symbols[6]['symbol'] != '':
        return symbols[2]['symbol']  # Le joueur gagne

    if all(symbol['symbol'] != '' for symbol in symbols):      # grille pleine = match nul
        return 'nul'  

    return None  # Aucun joueur n'a gagné pour le moment

def reset_game():
    global symbols, current_player, game_over
    symbols = [{'symbol': '', 'position': (case[0][0] + case[1] // 2, case[0][1] + case[2] // 2)} for case in cases]
    current_player = 'x'
    game_over = False

def quadrillage(cases):
    for case in cases: 
                  # rect(surface,    color   , (    x     ,      y    ,  width , height ))
        pygame.draw.rect(screen, (50, 50, 50), (case[0][0], case[0][1], case[1], case[2]))

cases = [
    ((5, 5), 185, 185),
    ((210, 5), 180, 185),
    ((410, 5), 185, 185),
    ((5, 210), 185, 180),
    ((210, 210), 180, 180),
    ((410, 210), 185, 180),
    ((5, 410), 185, 185),
    ((210, 410), 180, 185),
    ((410, 410), 185, 185)
]

# crée une liste de dictionnaires. Chaque dictionnaire contient une clé 'symbol' (chaine de caractère vide), et une clé 'position' (tuple).
# point médian de la largeur et de la hauteur de chaque case, pour centrer le symbole.
symbols = [{'symbol': '', 'position':  (case[0][0] + case[1] // 2,   case[0][1] + case[2] //  2)} for case in cases]
current_player = 'x'

run = True
while run:                            # pygame.event.get() renvoie un tableau avec tous les événements en cours
    for event in pygame.event.get():  # ces événements vont dans l'objet "event"
        if event.type == pygame.QUIT: # clic sur X 
            run = False               # pour fermer la fenêtre
        elif not game_over and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos

            for symbol in symbols:
                if symbol['symbol'] == '' and symbol['position'][0] - 75 < pos[0] < symbol['position'][0] + 75 and symbol['position'][1] - 75 < pos[1] < symbol['position'][1] + 75:
                    symbol['symbol'] = current_player
                    # Alternez entre les joueurs
                    current_player = 'o' if current_player == 'x' else 'x'
   
    screen.blit(fond, background_rect)              # Afficher l'image de fond
    clock.tick(60)                                  # limite le nombre d'exécutions par seconde de la "boucle de jeu"  (fréquence d'affichage)    
    draw_grid()                                     # Dessine la grille

    for symbol in symbols:
        if symbol['symbol'] == 'x':
            draw_cross(symbol['position'])
        elif symbol['symbol'] == 'o':
            draw_round(symbol['position'])

    pygame.display.flip()                           # Affiche tout ce qui doit être affiché (est nécessaire à partir du moment on dessine quelque chose)
    winner = check_winner(symbols)                         # Vérifiez si un joueur gagne

    if winner  or all(symbol['symbol'] != '' for symbol in symbols):                                          # Afficher le message du gagnant après la boucle principale
        game_over = True

        if winner == 'nul':
            message = "Match nul !"
        else:
            message = f"Joueur {winner} gagne la partie !"

        display_message(message)
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

    #  time.sleep(3)                                    # Ajout d'une pause de 3 secondes avant de quitter










        # if event.type == pygame.MOUSEBUTTONDOWN :           # clic de la souris
    #   if pygame.mouse.get_pressed() == (1,0,0):         # or pygame.mouse.get_pressed() == (0,1,0) or pygame.mouse.get_pressed() == (0,0,1):
    #     pos = pygame.mouse.get_pos()                    # position de la souris
    #     screen.blit(croix,(pos))

        #for case in cases:
            #AFFICHER CROIX
            
            # if pos in case:
            #   screen.blit(croix,(pos))  -----   MARCHE PAS

# croix_big = pygame.image.load('croix.png')                # importe une croix
# croix = pygame.transform.scale(croix_big, (200, 200))
# rond = pygame.transform.scale(rond_big, (200, 200))       # importe une rond
