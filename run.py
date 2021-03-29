import leveltwo
import pygame

# Screen settings
screen_width = 960
screen_height = 540
screen_size = (screen_width, screen_height)

if __name__ == "__main__":
    display = leveltwo.Display(screen_size)
    while display.running:
        display.display_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display.running = False
