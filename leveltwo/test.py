import pygame
WIDTH = 1920 #Largeur Ecran
HEIGHT = 1080 # Hauteur Ecran
# screen = pygame.display.set_mode((WIDTH, HEIGHT))  #pygame.FULLSCREEN) # Initialisation Fenetre
pygame.display.set_caption('test') #Titre Fenetre
running = True
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
class Cube:
    def update(self):
        self.cx, self.cy = pygame.mouse.get_pos()
        self.square = pygame.Rect(self.cx, self.cy, 100, 50)
    def vertical(self):
        self.cx, self.cy = pygame.mouse.get_pos()
        self.square = pygame.Rect(self.cx, self.cy, 50, 100)

    def draw(self): 
        pygame.draw.rect(screen, (255, 255, 255), self.square)


drawing_cube = False

while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    mx ,my = pygame.mouse.get_pos()
    if event.type == pygame.MOUSEBUTTONDOWN:
        pygame.draw.rect(screen, (255 , 255, 255), (mx, my, 100, 50))
    pygame.display.update()
    clock.tick(60)
       

    screen.fill((0, 0, 0))
    if drawing_cube:
        cube.draw()
        pygame.display.update()
pygame.quit()
quit()
#  while run:
#     screen = pygame.display.set_mode((WIDTH, HEIGHT))  #pygame.FULLSCREEN) # Initialisation Fenetre
#     mx, my = pygame.mouse.get_pos()
#     button_1 = pygame.Rect(20, 20, mx, my)
#     for event in pygame.event.get():
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             print("test")
#             pygame.draw.rect(screen, (255, 255, 255), button_1)
        