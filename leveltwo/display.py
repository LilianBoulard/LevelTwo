import pygame # Moteur 2D
import pygame_menu #Créer les Menus
import os # Pour importer des fichiers
import time # Pour le timer qui servira a vérifier les actions dans le jeu
pygame.init()

#Paramètre Ecran
WIDTH = 1920 #Largeur Ecran
HEIGHT = 1080 # Hauteur Ecran
#Parametre Ecriture
style = pygame.font.SysFont('Comic',50)

running = True
# timer = pygame.time.Clock()
def Play():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    menu = pygame_menu.Menu(600, 600, 'LevelTwo',theme=pygame_menu.themes.THEME_SOLARIZED) #Fenetre Menu
    menu.add.button("Bienvenue" + " " + input.get_value(), Play) #Bouton Jouer
    pygame.display.set_caption('LevelTwo') #Titre Fenetre
    menu.mainloop(screen)

#Affichage Ecran Menu Principal
def displayMenu():
    global input
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Creer la Fenetre selon paramètre
    menu = pygame_menu.Menu(600, 600, 'LevelTwo',theme=pygame_menu.themes.THEME_SOLARIZED) #Fenetre Menu
    input = menu.add.text_input('Name :', default='Nom') #Texte input Nom Joueur
    menu.add.button('Jouer', Play) #Bouton Jouer
    menu.add.button('Editer', Play) #Bouton Jouer
    menu.add.button('Créer', Play) #Bouton Jouer
    menu.add.selector('Niveaux :', [('Niveau 1', 1), ('Niveau 2', 2), ('Niveau Aleatoire', 3)]) #Selecteur Niveaux
    menu.add.button('Quit', pygame_menu.events.EXIT) #Bouton Quitter
    pygame.display.set_caption('LevelTwo') #Titre Fenetre
    menu.mainloop(screen)

    
    
    
            


while running:
    displayMenu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False