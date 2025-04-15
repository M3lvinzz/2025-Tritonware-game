import pygame
from cutscenes import Cutscene, tutorial

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space to Advance Cutscene")

def load_images(prefix, count, scale):
    return [
        pygame.transform.scale(pygame.image.load(f"{prefix}{i}.png").convert_alpha(), scale)
        for i in range(1, count + 1)
    ]
# Load assets
bg = pygame.image.load("assets/background1.png")
portraits = load_images('assets/portrait', count = 6, scale = (60, 60))

tutorial(screen, bg, portraits= portraits)