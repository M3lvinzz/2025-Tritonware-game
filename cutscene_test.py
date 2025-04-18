import pygame
from cutscenes import Cutscene, tutorial

pygame.init()
WIDTH, HEIGHT = 1200, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space to Advance Cutscene")

def load_images(prefix, count, scale):
    return [
        pygame.transform.scale(pygame.image.load(f"{prefix}{i}.png").convert_alpha(), scale)
        for i in range(1, count + 1)
    ]
# Load assets
bg = pygame.image.load("assets/background1.png")
portraits = load_images('assets/portrait', count = 6, scale = (500, 500))

running = True
while running:
    tutorial(screen, bg, portraits= portraits)