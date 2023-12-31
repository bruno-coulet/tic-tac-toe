import pygame, pygame_menu, sys, random, time
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


#----------------------     VARIABLES du MENU  -----------------------------------------------
click = False
font = pygame.font.Font(None, 50)                   # police et des messages
normal_color = (50, 50, 200)
hover_color = (100, 200, 100)

#----------------------     VARIABLES du JEU  -----------------------------------------------
clock = pygame.time.Clock()                         # système d'horloge
clock.tick(10)                                      # limite le nombre d'exécutions par seconde (fréquence d'affichage)
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

signes = [{ 'signe': '',    'position':  (case[0][0] + case[1] //2, case[0][1] + case[2] //2)  } for case in board]
# signes = [ liste de dictionnaire {chaine vide, centrées sur les cases} ]
# signes = [
#           { 'signe': '',    'position':  centre de la case   }
#           { 'signe': '',    'position':  centre de la case   } 
#           { 'signe': '',    'position':  centre de la case   }
#               etc...                                           ]
               

#----------------------     FONCTIONS DU MENU   ----------------------------------------------
def fond_menu():                            # Affiche l'image, la grille, le semi transparent
    background_rect = fond.get_rect()                   # fond = image de 600x600 px. gris semi transparent 
    screen.blit(fond, background_rect)                  # Afficher l'image de fond    blit(source, dest, area=None, special_flags=0) -> Rect
    draw_grid()                                         # dessine la grille
    background_color = (50, 50, 50, 220)                # défini une couleur semi-transparente (RGBA)
    background_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)   # défini une surface pour le fond semi-transparent
    background_surface.fill(background_color)           # attribue la couleur à la surface
    screen.blit(background_surface, (0, 0))             # Dessine la surface     

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect) 

def main_menu():                            # Première fonction appelée
    while True:                         
        fond_menu()                                             # affiche le fond
        draw_text('JEU DE MORPION', pygame.font.Font(None, 80), (240,240,240), screen, 50,170)  # affiche un texte blanc
        mx, my = pygame.mouse.get_pos()                         # position de la souris
        button_1_joueur = pygame.Rect(200,270,200,80)                  # bouton 1
        button_2_joueurs = pygame.Rect(200,430,200,80)                  # bouton 2
        
        if button_1_joueur.collidepoint( (mx,my)):                     # si bouton 1 et la souris coincident
            pygame.draw.rect(screen, hover_color, button_1_joueur)     # dessine le bouton couleur survol
            if click:                                           # click sur bouton 1
                menu_joueur_vs_algo()                           # appel la fonction menu_joueur_vs_algo
        else:                                                   # sinon
            pygame.draw.rect(screen, normal_color, button_1_joueur)    # dessine le bouton couleur normale
 
        if button_2_joueurs.collidepoint((mx,my)):                      # si bouton 2 et la souris coincident
            pygame.draw.rect(screen, hover_color, button_2_joueurs)     # dessine le bouton couleur survol
            if click:                                           # click sur bouton 2                                                                                                           
                deux_joueurs()                                  # appel la fonction deux_joueurs()                                   
        else:                                                   # sinon
            pygame.draw.rect(screen, normal_color, button_2_joueurs)    # dessine le bouton couleur normale


        draw_text('1 joueur', font, (255, 255, 255), screen, 220, 295)   # affiche les textes des boutons
        draw_text('2 joueurs', font, (255, 255, 255), screen, 220, 455)

        click = False

        for event in pygame.event.get():                       # pour fermer de la fenêtre                           
            if event.type == pygame.QUIT:                                   
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()
        clock.tick(60)

def menu_joueur_vs_algo():                  # annonce que l'IA n'est pas prête
    running = True
    click = False
    while running:
        pygame.display.flip()
        fond_menu()
        draw_text("Le mode difficile n'est pas finie", font, (255,255,255), screen, 25,50)
        draw_text("revenez plus tard",font, (255,255,255), screen, 150,120)

        mx, my = pygame.mouse.get_pos()

        button_menu_principal = pygame.Rect(150,200,300,80)
        button_facile = pygame.Rect(150,300,300,80)
        button_plus_dur = pygame.Rect(150,400,300,80)

        if button_menu_principal.collidepoint((mx,my)):
            pygame.draw.rect(screen, hover_color, button_menu_principal) 
            if click:                                           # click sur bouton "menu principal"
                return                                          # Retour au menu principal   
        else:pygame.draw.rect(screen, normal_color, button_menu_principal)

        if button_facile.collidepoint((mx,my)):
            pygame.draw.rect(screen, hover_color, button_facile) 
            if click:                                           # click sur bouton "facile"
                algo_facile()                                   # appel la fonction algo_facile()     
        else:pygame.draw.rect(screen, normal_color, button_facile)

        if button_plus_dur.collidepoint((mx,my)):
            pygame.draw.rect(screen, hover_color, button_plus_dur) 
            if click:                                           # click sur bouton 1
                return                                          # Return to the main menu     
        else:pygame.draw.rect(screen, normal_color, button_plus_dur)
        
        
        draw_text('Menu principal', font , (255,255,255), screen, 170, 230)
        draw_text('Facile', font , (255,255,255), screen, 170, 330)
        draw_text('Plus dur', font , (255,255,255), screen, 170, 430)

        click = False

        for event in pygame.event.get():                                    # ces événements vont dans l'objet "event"
            if event.type == pygame.QUIT:                                   # si clic sur X 
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)




#----------------------     FONCTIONS  DU JEU  ----------------------------------------------

def fond_jeu():
    background_rect = fond.get_rect()                                           # 
    screen.blit(fond, background_rect)                                          # Afficher l'image de fond    
    draw_grid()                                                                 # Dessine la grille

def check_winner(signes):                               # cherche 3 signes identiqus alignés dans les lignes, colonnes et diagonales
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

def draw_cross(position):                               # dessine x                          
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

def draw_round(center):                                 # dessine o                         
    pygame.draw.circle(screen, (50,50,230), (center), 80, 35) # circle(surface, color, center, radius, épaisseur)

def draw_sign():
    for signe in signes:                                                        # dessine x ou o selon le joueur
        if signe['signe'] == 'x':
            draw_cross(signe['position'])
        elif signe['signe'] == 'o':
            draw_round(signe['position'])

def draw_grid():                                        # dessine la grille
    for i in range(1, GRID_SIZE):                                                                                           # Lignes horizontales  
        pygame.draw.line(screen, LINE_COLOR, (0, i * HEIGHT // GRID_SIZE), (WIDTH, i * HEIGHT // GRID_SIZE), LINE_WIDTH)    # l'opérateur // retourne le quotient de la division entre deux nombres. 10 // 3 donnera 3.
                                                                                                                            # i=1     début (0, 200)             , fin (600,200)
                                                                                                                            # i=2     début (0, 400)             , fin (600,400)
                                                                                                                            # Lignes verticale
        pygame.draw.line(screen, LINE_COLOR, (i * WIDTH // GRID_SIZE, 0), (i * WIDTH // GRID_SIZE, HEIGHT), LINE_WIDTH)     # i=1     début 600//3= (200, 0)    ,  fin  600//3=(200,600)
                                                                                                                            # i=2     début 1200//3= (400, 0)   ,  fin 1200//3=(400,600)

def end_game():
    global game_over
    winner = check_winner(signes)                                               # Vérifie si un joueur gagne

    if winner  or all(signe['signe'] != '' for signe in signes):                # s'il y a un gagnant ou si toutes les cases sont occupées
        game_over = True                                                        # alors la partie est finie

        if winner == 'nul':                                                     # s'il n'y a pas de gagnant
            message = "Match nul !"                                             # message = Match nul
        else:
            message = f"Joueur {winner} gagne la partie !"                      # sinon message = le gagnant est...

        display_message(message)                                                # affiche le message
        display_restart(restart)                                                # relance la partie
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
    #                                   (      x    +  largeur/2  ,     y      +   hauteur/2 )
    signes = [{'signe': '', 'position': (case[0][0] + case[1] // 2, case[0][1] + case[2] // 2)} for case in board]
    current_player = 'x'
    game_over = False

def deux_joueurs():
    global run, game_over, current_player
    while run:                                     # pygame.event.get() renvoie un tableau avec tous les événements en cours
        for event in pygame.event.get():           # ces événements vont dans l'objet "event"
            if event.type == pygame.QUIT:          # si clic sur X 
                run = False                        # arrête la boucle

            elif not game_over and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # clic
                pos = event.pos                                                     # position du clic de la souris
                for signe in signes:                                                # signes = liste de chaine de caractère vide, centrées sur les cases          
                    if  signe['signe'] == '' and signe['position'][0] - 75 < pos[0] < signe['position'][0] + 75 and signe['position'][1] - 75 < pos[1] < signe['position'][1] + 75:
                        signe['signe'] = current_player                             # current_player = 'x'
                        current_player = 'o' if current_player == 'x' else 'x'      # Alterne les joueurs
                        break
        fond_jeu()                                                                  # dessine le fond et la grille
        draw_sign()
        pygame.display.flip()                                                       # Affiche tout ce qui doit être affiché (est nécessaire à partir du moment on dessine quelque chose) 
        end_game()

def algo_facile():
    global run, game_over, current_player # = 'x'
    while run:
        for event in pygame.event.get():                                # pour quitter la partie          
            if event.type == pygame.QUIT:
                run = False                       

            elif not game_over and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # si clic
                pos = event.pos                                         # position du clic de la souris

                if current_player=='x':
                    for signe in signes:                                    # cherche parmis toutes les cases
                                                                            # La case qui correspond au clic                                          
                        if  signe['signe']  == '' and signe['position'][0] - 75 < pos[0] < signe['position'][0] + 75 and signe['position'][1] - 75 < pos[1] < signe['position'][1] + 75:
                            signe['signe'] = current_player                 # elle prend le signe de current_player (x)                 
                            break                                           # arrete de chercher la case
                    draw_sign()                                             # dessine le x
                    pygame.display.flip()                                   # Affiche tout ce qui doit l'être
                    current_player = 'o'                                    # Passe au joueur o
                    fond_jeu()
                    end_game()

                # current_player = 'o'  if current_player == 'x' else 'x'  # Alterne les joueurs

            #   ------- Algo joue une case disponible au hasard ---------------------------------------------
                if current_player=='o':
                    time.sleep(0.5)                                         # petite pause, simule un temps de reflexion
                    dispo = [signe for signe in signes if signe['signe'] == ''] # liste des cases disponibles   
                    random_signe = random.choice(dispo)                     # choisi une case disponible au hasard
                    random_signe['signe'] = current_player                  # elle prend le signe o
                    draw_sign()                                             # dessine le o
                    pygame.display.flip()                                   # Affiche tout ce qui doit l'être
                    current_player = 'x'                                    # Passe au joueur x
                    fond_jeu()
                    end_game()


def algo_dur():
    pass






#   ----------------------     BOUCLE   ----------------------------------------------
main_menu()                                    # APPEL LE MENU PRINCIPAL

