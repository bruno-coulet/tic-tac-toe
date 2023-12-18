import pygame, sys, random, time
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
# click = False
button_font = pygame.font.Font(None, 50)            # police et des messages
title_font = pygame.font.Font(None, 80)
subtitle_font = pygame.font.Font(None, 50)
normal_color = (50, 50, 200)
hover_color = (100, 200, 100)
# launching = True

#----------------------     VARIABLES du JEU  -----------------------------------------------
clock = pygame.time.Clock()                         # système d'horloge
clock.tick(10)                                      # limite le nombre d'exécutions par seconde (fréquence d'affichage)
game_over = False
waiting_for_click = False
current_player = 'x'
run = True
# board = [                                         # liste des cases
#     ((0, 0), 200, 200),                           # case 1 (origine, largeur, hauteur)
#     ((0, 201), 200, 200),                         # case 2
#     ((0, 401), 200, 200),                         # case 3
#     ((0, 201), 200, 200),                         # case 4
#     ((201, 201), 200, 200),                       # case 5
#     ((401, 401), 200, 200),                       # case 6
#     ((0, 401), 200, 200),                         # case 7
#     ((201, 401), 200, 200),                       # case 8
#     ((401, 401), 200, 200)                        # case 9
# ]
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
cases   = [{ 'signe': '',    'position':  (case[0][0] + case[1] //2, case[0][1] + case[2] //2)  } for case in board]
# cases = [ liste de dictionnaire {chaine vide, centrées sur les cases} ]
# cases = [
#           { 'signe': '',    'position':  centre de la case 1  }
#           { 'signe': '',    'position':  centre de la case 2  } 
#           { 'signe': '',    'position':  centre de la case 3  }
#               etc...                                           ]
               

#----------------------     FONCTIONS DU MENU   ----------------------------------------------
def fond_menu():                            # Affiche l'image, la grille, le semi transparent
    fond_jeu()                                          # affiche l'image de fond et la grille
    background_color = (50, 50, 50, 220)                # défini une couleur semi-transparente (RGBA)
    background_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)   # défini une surface pour le fond semi-transparent
    background_surface.fill(background_color)           # attribue la couleur à la surface
    screen.blit(background_surface, (0, 0))             # Dessine la surface     

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect) 

def menu_principal():                                             # Première fonction appelée
    click = False
    # while True:          
    fond_menu()                                                     # affiche le fond
    draw_text('JEU DE MORPION', title_font, (240,240,240), screen, 50,170)  # affiche un texte blanc
    
    # mx, my = pygame.mouse.get_pos()                                 # position de la souris
    
    button_1_joueur = pygame.Rect(200,270,200,80)                   # bouton 1
    button_2_joueurs = pygame.Rect(200,430,200,80)                  # bouton 2
    
    if button_1_joueur.collidepoint( (mx,my)):                      # si bouton 1 et la souris coincident
        pygame.draw.rect(screen, hover_color, button_1_joueur)      # dessine le bouton couleur survol
        if click:                                                   # click sur bouton 1
            menu_1_joueur()                                         # appel la fonction menu_1_joueur
    else: pygame.draw.rect(screen, normal_color, button_1_joueur)   # sinon dessine le bouton couleur normale

    if button_2_joueurs.collidepoint((mx,my)):                      # si bouton 2 et la souris coincident
        pygame.draw.rect(screen, hover_color, button_2_joueurs)     # dessine le bouton couleur survol
        if click:                                                   # click sur bouton 2                                                                                                           
            deux_joueurs()                                          # appel la fonction deux_joueurs()                                   
    else: pygame.draw.rect(screen, normal_color, button_2_joueurs)  # sinon dessine le bouton couleur normale


    draw_text('1 joueur', button_font, (255, 255, 255), screen, 220, 295)  # affiche le texte du bouton 1
    draw_text('2 joueurs', button_font, (255, 255, 255), screen, 220, 455) # affiche le texte du bouton 2

    pygame.display.update()
    pygame.display.flip()

def menu_1_joueur():              
    click = False
    # while True:
    fond_menu()
    mx, my = pygame.mouse.get_pos()
    button_menu_principal = pygame.Rect(150,200,300,80)
    button_facile = pygame.Rect(150,300,300,80)
    button_difficile = pygame.Rect(150,400,300,80)

    if button_menu_principal.collidepoint((mx,my)):
        pygame.draw.rect(screen, hover_color, button_menu_principal)
        if click:     
                                                    # click sur bouton "menu principal"
            # menu_principal()                                # Retour au menu_principal
            return  
    else:pygame.draw.rect(screen, normal_color, button_menu_principal)

    if button_facile.collidepoint((mx,my)):
        pygame.draw.rect(screen, hover_color, button_facile) 
        if click:
            algo_facile()                                   # appel la fonction algo_facile()

    else: pygame.draw.rect(screen, normal_color, button_facile)

    if button_difficile.collidepoint((mx,my)):
        pygame.draw.rect(screen, hover_color, button_difficile) 
        if click:                                           # click sur bouton 1
            # return
            algo_difficile()
                                                            # Return to the main menu     
    else:pygame.draw.rect(screen, normal_color, button_difficile)

    draw_text("Le mode 'difficile' n'est pas fini", subtitle_font, (255,255,255), screen, 40,100)
    draw_text("Essayez le mode 'facile'!",subtitle_font, (255,255,255), screen, 100,140)
    draw_text('Menu principal', button_font , (255,255,255), screen, 170, 230)
    draw_text('Facile', button_font , (255,255,255), screen, 170, 330)
    draw_text('Difficile - a finir', button_font , (255,255,255), screen, 170, 430)

    pygame.display.update()
    pygame.display.flip()


#----------------------     FONCTIONS  DU JEU  ----------------------------------------------

def fond_jeu():             # affiche l'image de fond et la grille
    background_rect = fond.get_rect()   # defini une surface à la taille de l'image ?
    screen.blit(fond, background_rect)  # affiche l'image de fond sur la surface  ? 
    for i in range(1, GRID_SIZE):       # dessine la grille                                                                                     # Lignes horizontales  
        pygame.draw.line(screen, LINE_COLOR, (0, i * HEIGHT // GRID_SIZE), (WIDTH, i * HEIGHT // GRID_SIZE), LINE_WIDTH)    # l'opérateur // retourne le quotient de la division entre deux nombres. 10 // 3 donnera 3.
                                                                                                                            # i=1     début (0, 200)             , fin (600,200)
                                                                                                                            # i=2     début (0, 400)             , fin (600,400)
                                                                                                                            # Lignes verticale
        pygame.draw.line(screen, LINE_COLOR, (i * WIDTH // GRID_SIZE, 0), (i * WIDTH // GRID_SIZE, HEIGHT), LINE_WIDTH)     # i=1     début 600//3= (200, 0)    ,  fin  600//3=(200,600)
                                                                                                                            # i=2     début 1200//3= (400, 0)   ,  fin 1200//3=(400,600)                                                                # Dessine la grille

def draw_sign():            # dessine x ou o

    def draw_round(center):     # dessine o                         
        pygame.draw.circle(screen, (50,50,230), (center), 80, 35) # circle(surface, color, center, radius, épaisseur)
    
    def draw_cross(position):   # dessine x                          
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

    for signe in cases:                                                        # dessine x ou o selon le joueur
        if signe['signe'] == 'x':
            draw_cross(signe['position'])
        elif signe['signe'] == 'o':
            draw_round(signe['position'])
  
def check_winner(cases):    # cherche 3 cases identiques alignés dans les lignes, colonnes et diagonales
    # Vérification des lignes horizontales, retourne le signe
    for row in range(0, 9, 3):         # row = 0 ou 3 ou 6
        if cases[row]['signe'] == cases[row + 1]['signe'] == cases[row + 2]['signe'] != '': # non vide et identique
    #      cases [0]['signe']  == cases [1]['signe']      == cases [2]['signe']  -> signe des cases 0,1 et 2 (ligne 1)
    #      cases [3]['signe']  == cases [4]['signe']      == cases [5]['signe']  -> signe des cases 3,4 et 5 (ligne 2)
    #      cases [6]['signe']  == cases [7]['signe']      == cases [8]['signe']  -> signe des cases 6,7 et 8 (ligne 3)
            return cases[row]['signe']             #  retourne le signe de la ligne

    # Vérification des colonnes, retourne le signe
    for col in range(3):                                                                       # col = (0,1,2)
        if cases[col]['signe'] == cases[col + 3]['signe'] == cases[col + 6]['signe'] != '': # signe des cases 0,3 et 6 (colonne 1)
            return cases[col]['signe']
    
    # Vérification diagonale de gauche à droite, retourne le signe
    if cases[0]['signe'] == cases[4]['signe'] == cases[8]['signe'] != '':    # signe des cases 0,4 et 8
        return cases[0]['signe']
    
    # Vérification diagonale de droite à gauche, retourne le signe
    if cases[2]['signe'] == cases[4]['signe'] == cases[6]['signe'] != '':    # signe des cases 2,4 et 6
        return cases[2]['signe']
    
    # grille pleine = match nul
    if all(signe['signe'] != '' for signe in cases):     
        return 'nul'  

    return None  # Aucun gagnant pour le moment

def end_game():             # cherche un gagnant -> message -> reset_cells
    global game_over
    global run
    winner = check_winner(cases)                                    # un joueur gagne ?
    grille_pleine = all(signe['signe'] != '' for signe in cases)    # la grille pleine ?

    if winner or grille_pleine:             # s'il y a un gagnant ou si la grille est pleine
        game_over = True                                        # alors la partie est finie
        
        # if winner == 'nul':                                     # s'il n'y a pas de gagnant
        if  grille_pleine:
            message = "Match nul !"                             # message = Match nul
        else:                                                   # sinon
            message = f"Joueur {winner} gagne la partie !"      # message = le gagnant est 'x' ou 'o'

        fond_menu()
        text = button_font.render(message, True, (220, 220, 50)) # couleur et police des messages
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - (text.get_height()*2) // 2)) # Dessine le texte


        waiting_for_click = True
        while waiting_for_click:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    waiting_for_click = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    reset_cells()
                    waiting_for_click = False
                    game_over = False
            mx, my = pygame.mouse.get_pos() 
            button_rejouer = pygame.Rect(100,350,400,80)            # bouton rejouer
            if button_rejouer.collidepoint((mx,my)):
                pygame.draw.rect(screen, hover_color, button_rejouer) 
                if click:                                          
                    # menu_principal()
                    return
                    # run = False
                    print('click')  
            else:pygame.draw.rect(screen, normal_color, button_rejouer)
            draw_text('Cliquez pour rejouer', button_font , (255,255,255), screen, 120, 380)
            pygame.display.flip()

def reset_cells():          # vide les cases pour la prochaine partie
    global cases, current_player, game_over
    #                                   (      x    +  largeur/2  ,     y      +   hauteur/2 )
    cases = [{'signe': '', 'position': (case[0][0] + case[1] // 2, case[0][1] + case[2] // 2)} for case in board]
    current_player = 'x'
    game_over = False

def deux_joueurs():
    global run, game_over, current_player

    # mx, my = pygame.mouse.get_pos()                                 # position de la souris
    # pos =(mx,my)                                                            # position du clic de la souris
    for signe in cases:                                                # cases = liste de chaine de caractère vide, centrées sur les cases          
        if  signe['signe'] == '' and signe['position'][0] - 75 < pos[0] < signe['position'][0] + 75 and signe['position'][1] - 75 < pos[1] < signe['position'][1] + 75:
            signe['signe'] = current_player                             # current_player = 'x'
            current_player = 'o' if current_player == 'x' else 'x'      # Alterne les joueurs
            break
    fond_jeu()                                                                  # dessine le fond et la grille
    draw_sign()
    pygame.display.flip()                                                       # Affiche tout ce qui doit être affiché (est nécessaire à partir du moment on dessine quelque chose) 
    end_game()

def algo_facile():
    fond_jeu()
    global run, game_over, current_player # = 'x'
    
    if not game_over and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # si clic
        pos = event.pos                                             # position du clic de la souris                
        if current_player=='x':                                     # Le joueur joue les croix               
            for signe in cases:                                    # cherche parmis toutes les cases
                                                                    # La case qui correspond au clic                                          
                if  signe['signe']  == '' and signe['position'][0] - 75 < pos[0] < signe['position'][0] + 75 and signe['position'][1] - 75 < pos[1] < signe['position'][1] + 75:
                    signe['signe'] = current_player                 # elle prend le signe de current_player (x)                 
                    break                                           # arrete de chercher la case
            fond_jeu()
            draw_sign()                                             # dessine le x
            pygame.display.flip()                                   # Affiche tout ce qui doit l'être
            current_player = 'o'                                    # Passe au joueur o
            end_game()
            time.sleep(0.3)                                         # petite pause, simule un temps de reflexion
        # current_player = 'o'  if current_player == 'x' else 'x'   # Alterne les joueurs
        
        # Vérifie si les coins sont disponible
        coins_dispo = []
        for coin in (cases[0],cases[2],cases[6],cases[8]) :
            if coin ['signe'] == '':
                coins_dispo.append (coin)
        if coins_dispo != []:
            random_coin_dispo = random.choice(coins_dispo)
            random_coin_dispo['signe'] = current_player             # elle prend le signe o
            current_player = 'x'                                    # Passe au joueur x
            
        #  Joue une case disponible au hasard ---------------------------------------------
        elif coins_dispo == []:
            dispo = [signe for signe in cases if signe['signe'] == ''] # liste des cases disponibles   
            random_signe = random.choice(dispo)                     # choisi une case disponible au hasard
            random_signe['signe'] = current_player                  # elle prend le signe o
            current_player = 'x'                                    # Passe au joueur x
            
        fond_jeu()
        draw_sign()                                             # dessine le o
        pygame.display.flip()                                   # Affiche tout ce qui doit l'être
        end_game()
            
def algo_difficile():                                         # A FINIR
        
    global run, game_over, current_player # = 'x'
    fond_jeu()

                
    # Le joueur joue les croix 
    if current_player=='x':
        pos = event.pos                                             # position du clic de la souris                                    
        for signe in cases:                                    # cherche parmis toutes les cases
                                                                # La case qui correspond au clic                                          
            if  signe['signe']  == '' and signe['position'][0] - 75 < pos[0] < signe['position'][0] + 75 and signe['position'][1] - 75 < pos[1] < signe['position'][1] + 75:
                signe['signe'] = current_player                 # elle prend le signe de current_player (x)                 
                break                                           # arrete de chercher la case

        draw_sign()                                             # dessine le x
        pygame.display.flip()                                   # Affiche tout ce qui doit l'être
        current_player = 'o'  if current_player == 'x' else 'x'
    end_game()
    time.sleep(0.3)                                         # petite pause, simule un temps de reflexion
    current_player = 'o'  if current_player == 'x' else 'x'   # Alterne les joueurs


    # S'il y a 2 'x' dans une ligne, met un 'o' dans la case disponible
    for row in range(0, 9, 3):
        count = 0  
        for case in [0, 2]:
            if cases[case]['signe'] == 'x':
                count += 1
                if count == 2:
                    if cases[case]['signe'] == '':
                        cases[case]['signe'] = current_player
                        current_player="x"
                        break  # Sort de la boucle interne quand deux 'x' sont trouvés


    # Vérification des colonnes, retourne le signe
    # else:
    #     for col in range(3):
    #         count = 0                                                                       # col = (0,1,2)
    #         if cases[col]['signe'] == cases[col + 3]['signe'] == cases[col + 6]['signe'] != '': # signe des cases 0,3 et 6 (colonne 1)
    #             return cases[col]['signe']


        else :
        # Vérifie si les coins sont disponible
            coins_dispo = []
            for coin in (cases[0],cases[2],cases[6],cases[8]) :
                if coin ['signe'] == '':
                    coins_dispo.append (coin)                  # ajoute les coins dispo à la liste
            if coins_dispo != []:                              # si la liste n'est pas vide
                random_coin_dispo = random.choice(coins_dispo) # un coin au hasard...
                random_coin_dispo['signe'] = current_player    # ... prend le signe o
                current_player = 'x'                           # Passe au joueur x

#  Joue une case disponible au hasard ---------------------------------------------
            elif coins_dispo == []:
                dispo = [signe for signe in cases if signe['signe'] == ''] # liste des cases disponibles   
                random_signe = random.choice(dispo)                     # choisi une case disponible au hasard
                random_signe['signe'] = current_player                  # elle prend le signe o
                current_player = 'x'                                    # Passe au joueur x



    fond_jeu()
    draw_sign()                                             # dessine le o
    pygame.display.flip()                                   # Affiche tout ce qui doit l'être
    end_game()


#   ----------------------     BOUCLE   ----------------------------------------------
click = False
while True:
    mx, my = pygame.mouse.get_pos()                                 # position de la souris
    pos =(mx,my)
    
    for event in pygame.event.get():                                # pour fermer de la fenêtre                           
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
            
        elif not game_over and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # clic
            pos = event.pos 

        fond_menu()                                                     # affiche le fond
        draw_text('JEU DE MORPION', title_font, (240,240,240), screen, 50,170)  # affiche un texte blanc
        
        button_1_joueur = pygame.Rect(200,270,200,80)                   # bouton 1
        button_2_joueurs = pygame.Rect(200,430,200,80)                  # bouton 2
        
        if button_1_joueur.collidepoint( (mx,my)):                      # si bouton 1 et la souris coincident
            pygame.draw.rect(screen, hover_color, button_1_joueur)      # dessine le bouton couleur survol
            if click:                                                   # click sur bouton 1
                menu_1_joueur()                                         # appel la fonction menu_1_joueur
        else: pygame.draw.rect(screen, normal_color, button_1_joueur)   # sinon dessine le bouton couleur normale

        if button_2_joueurs.collidepoint((mx,my)):                      # si bouton 2 et la souris coincident
            pygame.draw.rect(screen, hover_color, button_2_joueurs)     # dessine le bouton couleur survol
            if click:                                                   # click sur bouton 2                                                                                                           
                deux_joueurs()                                          # appel la fonction deux_joueurs()                                   
        else: pygame.draw.rect(screen, normal_color, button_2_joueurs)  # sinon dessine le bouton couleur normale

        draw_text('1 joueur', button_font, (255, 255, 255), screen, 220, 295)  # affiche le texte du bouton 1
        draw_text('2 joueurs', button_font, (255, 255, 255), screen, 220, 455) # affiche le texte du bouton 2
    
        pygame.display.update()
        pygame.display.flip()
