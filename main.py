import pygame, sys

# Initialize pygame
pygame.init()

# Screen setup
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("College Decision Game")

# Font setup
font = pygame.font.SysFont("Arial", 24)

# Basic text drawing function
def draw_text(text, x, y):
    rendered = font.render(text, True, (0,0,0))
    screen.blit(rendered, (x,y))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((255,255,255))
    draw_text("College Decision Game!", 280, 280)
    pygame.display.flip()
    