import pygame
import sys

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Sprite Test")
clock = pygame.time.Clock()

# Load one dino image (run1.png must exist in same folder)
try:
    dino_img = pygame.transform.scale(pygame.image.load("run1.png").convert_alpha(), (60, 60))
except:
    print("Failed to load run1.png")
    pygame.quit()
    sys.exit()

# Dino position
dino = pygame.Rect(50, HEIGHT - 80, 60, 60)

# Main loop
running = True
while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((180, 240, 255))  # Light blue background
    screen.blit(dino_img, dino)   # Draw the dino
    pygame.display.flip()         # Refresh the screen

pygame.quit()
