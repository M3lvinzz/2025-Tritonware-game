import pygame

def load_images(prefix, count, scale):
    return [
        pygame.transform.scale(
            pygame.image.load(f"{prefix}{i}.png").convert_alpha(), scale
        ) for i in range(1, count + 1)
    ]

def load_image(path, size=None):
    img = pygame.image.load(path).convert_alpha()
    if size:
        img = pygame.transform.scale(img, size)
    return img