import pygame, sys, random, time
pygame.init()

WIDTH, HEIGHT = 600, 600
GRID_SIZE = 3
LINE_COLOR = (200, 0, 0)
LINE_WIDTH = 30
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Morpion")
image_trop_grande = pygame.image.load('fond.jpg')
image_de_fond = pygame.transform.scale(image_trop_grande, (WIDTH, HEIGHT))

TITLE = 'JEU DE MORPION'
TITLE_FONT = pygame.font.Font(None, 80)
FONT = pygame.font.Font(None, 50)

CREME = (240,240,240)
BACKGROUND_COLOR = (50, 50, 50, 220)      
NORMAL_COLOR = (50, 50, 200)
HOVER_COLOR = (100, 200, 100)

BUTTON_FONT = pygame.font.Font(None, 50)   

BOARD = [     # liste des cases (grille du jeu)
    ((5, 5), 185, 185),                             # case 1 (origine, largeur, hauteur)    ((0, 0), 200, 200),
    ((210, 5), 180, 185),                           # case 2                                ((0, 201), 200, 200),
    ((410, 5), 185, 185),                           # case 3                                ((0, 401), 200, 200),
    ((5, 210), 185, 180),                           # case 4                                ((0, 201), 200, 200),
    ((210, 210), 180, 180),                         # case 5                                ((201, 201), 200, 200),
    ((410, 210), 185, 180),                         # case 6                                ((401, 401), 200, 200),
    ((5, 410), 185, 185),                           # case 7                                ((0, 401), 200, 200),
    ((210, 410), 180, 185),                         # case 8                                ((201, 401), 200, 200), 
    ((410, 410), 185, 185)                          # case 9                                ((401, 401), 200, 200)
]

cases   = [{ 'signe': '',    'position':  (case[0][0] + case[1] //2, case[0][1] + case[2] //2)  } for case in BOARD]
""" cases = [ liste de dictionnaire {chaine vide, centrées sur les cases} ]
 cases = [
           { 'signe': '',    'position':  centre de la case 1  }
           { 'signe': '',    'position':  centre de la case 2  } 
           { 'signe': '',    'position':  centre de la case 3  }
               etc...                                           ]"""

clock = pygame.time.Clock()
clock.tick(5)
game_over = False
wait_for_click = False
current_player = 'x'
click = False
run = True

def fond_jeu():             # affiche l'image de fond et la grille
    fond = image_de_fond.get_rect()   # defini une surface à la taille de l'image de fond
    SCREEN.blit(image_de_fond, fond)  # affiche l'image de fond sur la surface 
    for i in range(1, GRID_SIZE):       # dessine la grille                                                                                     # Lignes horizontales  
        pygame.draw.line(SCREEN, LINE_COLOR, (0, i * HEIGHT // GRID_SIZE), (WIDTH, i * HEIGHT // GRID_SIZE), LINE_WIDTH)    # l'opérateur // retourne le quotient de la division entre deux nombres. 10 // 3 donnera 3.
                                                                                                                            # i=1     début (0, 200)             , fin (600,200)
                                                                                                                            # i=2     début (0, 400)             , fin (600,400)
                                                                                                                            # Lignes verticale
        pygame.draw.line(SCREEN, LINE_COLOR, (i * WIDTH // GRID_SIZE, 0), (i * WIDTH // GRID_SIZE, HEIGHT), LINE_WIDTH)     # i=1     début 600//3= (200, 0)    ,  fin  600//3=(200,600)
 
def gris_transparent():            # Affiche l'image, la grille, le semi transparent
    semi_transparent = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)   # défini une surface pour le fond semi-transparent
    semi_transparent.fill(BACKGROUND_COLOR)           # attribue la couleur à la surface
    SCREEN.blit(semi_transparent, (0, 0))             # Dessine la surface     

def draw_text(text, FONT, CREME, SCREEN, x, y):
    textobj = FONT.render(text, 1, CREME)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    SCREEN.blit(textobj, textrect) 

def switch_player():
    global current_player
    current_player = 'o'  if current_player == 'x' else 'x'

def draw_sign():            # dessine x ou o

    def draw_round(center):     # dessine o                         
        pygame.draw.circle(SCREEN, (50,50,230), (center), 80, 35) # circle(surface, color, center, radius, épaisseur)
    
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
            pygame.draw.line(SCREEN, line['color'], line['start'], line['end'], line['thickness'])

    # for signe in cases:                                                        # dessine x ou o selon le joueur
    #     if signe['signe'] == 'x':
    #         draw_cross(signe['position'])
    #     elif signe['signe'] == 'o':
    #         draw_round(signe['position'])
    for case in cases:                                                        # dessine x ou o selon le joueur
        if case['signe'] == 'x':
            draw_cross(case['position'])
        elif case['signe'] == 'o':
            draw_round(case['position'])
  
def check_winner(cases):    # cherche 3 'x' ou 3 'o' 
    # Vérification des lignes, retourne le signe
    for row in range(0, 9, 3): 
        if cases[row]['signe'] == cases[row + 1]['signe'] == cases[row + 2]['signe'] != '':
            return cases[row]['signe']             #  retourne le signe de la ligne
    '''             # row = 0 ou 3 ou 6, non vide et identique
    #      cases [0]['signe']  == cases [1]['signe']      == cases [2]['signe']  -> signe des cases 0,1 et 2 (ligne 1)
    #      cases [3]['signe']  == cases [4]['signe']      == cases [5]['signe']  -> signe des cases 3,4 et 5 (ligne 2)
    #      cases [6]['signe']  == cases [7]['signe']      == cases [8]['signe']  -> signe des cases 6,7 et 8 (ligne 3)'''    

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

    return None  # Aucun gagnant pour le moment

def end_game():             # cherche un gagnant -> resultat -> reset_cells
    global  run, game_over

    winner = check_winner(cases)                                    # un gagnant ?
    grille_pleine = all(signe['signe'] != '' for signe in cases)    # grille pleine ?

    if winner or grille_pleine:             # s'il y a un gagnant ou si la grille est pleine
        game_over = True                                        # alors la partie est finie
                                
        if  grille_pleine and not winner:                                      # s'il n'y a pas de gagnant
            resultat = "Match nul !"                             # resultat = Match nul
        else:                                                   # sinon
            resultat = f"Joueur {winner} gagne la partie !"      # resultat = le gagnant est 'x' ou 'o'

        gris_transparent()
        text_resultat = BUTTON_FONT.render(resultat, True, (CREME)) # couleur et police des resultats
        SCREEN.blit(text_resultat, (WIDTH // 2 - text_resultat.get_width() // 2, HEIGHT // 2 - (text_resultat.get_height()*2) // 2)) # Dessine le texte
        rejouer()

def rejouer():
    global game_over, run, wait_for_click

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
 
                # wait_for_click = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()

                button_rejouer = pygame.Rect(100,350,400,80)           

                if button_rejouer.collidepoint((mx,my)):
                    pygame.draw.rect(SCREEN, HOVER_COLOR, button_rejouer) 
                    if click:
                        reset_cells()
                        wait_for_click = False
                        game_over = False                                          
                        return
                else:pygame.draw.rect(SCREEN, NORMAL_COLOR, button_rejouer)

                draw_text('Cliquez pour rejouer', BUTTON_FONT , (CREME), SCREEN, 120, 380)
                pygame.display.flip()

def reset_cells():          # vide les cases pour la prochaine partie
    global cases, current_player, game_over
    #                                   (      x    +  largeur/2  ,     y      +   hauteur/2 )
    cases = [{'signe': '', 'position': (case[0][0] + case[1] // 2, case[0][1] + case[2] // 2)} for case in BOARD]

def joueur_joue():
    for signe in cases:                                                # cases = liste de chaine de caractère vide, centrées sur les cases          
        if  signe['signe'] == '' and signe['position'][0] - 75 < pos[0] < signe['position'][0] + 75 and signe['position'][1] - 75 < pos[1] < signe['position'][1] + 75:
            signe['signe'] = current_player                             # current_player = 'x'
            switch_player()
            # current_player = 'o' if current_player == 'x' else 'x'      # Alterne les joueurs
            break

def deux_joueurs():
    global run, game_over, current_player
    while run:                        # pygame.event.get() renvoie un tableau avec tous les événements en cours
        for event in pygame.event.get():           # ces événements vont dans l'objet "event"
            if event.type == pygame.QUIT:          # si clic sur X 
                pygame.quit()
                run = False           # arrête la boucle

            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # clic
                pos = event.pos    

                # joueur_joue()
                for signe in cases:                                                # cases = liste de chaine de caractère vide, centrées sur les cases          
                    if  signe['signe'] == '' and signe['position'][0] - 75 < pos[0] < signe['position'][0] + 75 and signe['position'][1] - 75 < pos[1] < signe['position'][1] + 75:
                        signe['signe'] = current_player                             # current_player = 'x'
                        switch_player()
                        # current_player = 'o' if current_player == 'x' else 'x'      # Alterne les joueurs
                        break
        fond_jeu()                                                                  # dessine le fond et la grille
        draw_sign()
        pygame.display.flip()                                                       # Affiche tout ce qui doit être affiché (est nécessaire à partir du moment on dessine quelque chose) 
        end_game()

def algo_facile():
    global run, game_over, current_player
    while run:
        for event in pygame.event.get():                                    # pour quitter la partie          
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            # elif not game_over and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # si clic
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # clic
                pos = event.pos    
          
                if current_player=='x':                                     # Le joueur joue les croix               
                    for signe in cases:                                    # cherche parmis toutes les cases
                                                                            # La case qui correspond au clic                                          
                        if  signe['signe']  == '' and signe['position'][0] - 75 < pos[0] < signe['position'][0] + 75 and signe['position'][1] - 75 < pos[1] < signe['position'][1] + 75:
                            signe['signe'] = current_player                 # elle prend le signe de current_player (x)                 
                            switch_player()
                            break                                           # arrete de chercher la case
                    fond_jeu()
                    draw_sign()                                             # dessine le x
                    pygame.display.update()                                   # Affiche tout ce qui doit l'être
                    end_game()


                    time.sleep(0.3)                                         # petite pause, simule un temps de reflexion
                    
                    # vérifie si risque de perdre
                    count = 0
                    # Vérification des lignes
                    for row in range(0, 9, 3): # row = 0 ou 3 ou 6
                        if cases[row]['signe'] == 'x':
                            count += 1
                        if cases[row + 1]['signe'] == 'x':
                            count += 1
                        if cases[row + 2]['signe'] == 'x':
                            count += 1
                    if count == 2:
                        for i in range (3):
                            if cases [i]['signe'] == '':
                                cases [i]['signe'] = 'o'      
                    elif count < 2:
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
            
def algo_difficile():       
    global run, game_over, current_player, click, pos
    fond_jeu()                      
    for signe in cases:                                    # cherche parmis toutes les cases
                                                            # La case qui correspond au clic                                          
        if  signe['signe']  == '' and signe['position'][0] - 75 < pos[0] < signe['position'][0] + 75 and signe['position'][1] - 75 < pos[1] < signe['position'][1] + 75:
            signe['signe'] = current_player                 # elle prend le signe de current_player (x)                 
            break                                           # arrete de chercher la case
    draw_sign()                                             # dessine le x
    pygame.display.flip()                                   # Affiche tout ce qui doit l'être
    
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

def menu():
    global pos, click

    if click == False:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # si clic
            pos = event.pos                                             # position du clic de la souris
            click = True                                                # clic

        gris_transparent()                                              # ajoute le menu par dessus le fond                                                             
        BUTTON_2_JOUEURS = pygame.Rect(150,300,300,80)                  # affiche les boutons
        BUTTON_FACILE = pygame.Rect(150,400,300,80)
        BUTTON_DIFFICILE = pygame.Rect(150,500,300,80)

        if BUTTON_2_JOUEURS.collidepoint((mx,my)):                      # si bouton et la souris coincident
            
            pygame.draw.rect(SCREEN, HOVER_COLOR, BUTTON_2_JOUEURS)     # dessine le bouton couleur survol
            if click:  
                deux_joueurs()                                          # appel la fonction deux_joueurs()                                   
        else: pygame.draw.rect(SCREEN, NORMAL_COLOR, BUTTON_2_JOUEURS)  # sinon dessine le bouton couleur normale

        if BUTTON_FACILE.collidepoint((mx,my)):
            pygame.draw.rect(SCREEN, HOVER_COLOR, BUTTON_FACILE) 
            if click:
                algo_facile()                                           
        else: pygame.draw.rect(SCREEN, NORMAL_COLOR, BUTTON_FACILE)

        if BUTTON_DIFFICILE.collidepoint((mx,my)):
            pygame.draw.rect(SCREEN, HOVER_COLOR, BUTTON_DIFFICILE) 
            if click:                                                   
                algo_difficile()                                         
        else:pygame.draw.rect(SCREEN, NORMAL_COLOR, BUTTON_DIFFICILE)
            

        draw_text(TITLE, TITLE_FONT, CREME, SCREEN, 50,100)
        draw_text('2 joueurs', BUTTON_FONT, CREME, SCREEN, WIDTH//2-80, 330)
        draw_text('Facile', BUTTON_FONT , CREME, SCREEN, WIDTH//2-80, 430)
        draw_text('Difficile', BUTTON_FONT , CREME, SCREEN, WIDTH//2-80, 530)

#   ----------------------     BOUCLE   ----------------------------------------------
while run:

    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    pygame.display.flip()
    fond_jeu()
    menu()




