import pygame # Moteur 2D
import pygame_menu
import os # Pour importer des fichiers
import time # Pour le timer qui servira a vérifier les actions dans le jeu
pygame.init()

#Paramètre Ecran
WIDTH = 1920 #Largeur Ecran
HEIGHT = 1080 # Hauteur Ecran
#Parametre Ecriture
style = pygame.font.SysFont('Comic',50)

running = True

timer = pygame.time.Clock()

#Affichage Ecran Menu Principal
def displayMenu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    menu = pygame_menu.Menu(600, 400, 'Welcome',theme=pygame_menu.themes.THEME_SOLARIZED)
    menu.add.text_input('Name :', default='Nouveau')
    menu.add.button('Play')
    menu.add.selector('Niveaux :', [('Niveau 1', 1), ('Niveau 2', 2), ('Niveau Aleatoire', 3)])
    menu.add.button('Quit', pygame_menu.events.EXIT)
    pygame.display.set_caption('LevelTwo') #Titre Fenetre
    
    pygame.display.update() #Update screen
    menu.mainloop(screen)
    
            


while running:
    displayMenu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False