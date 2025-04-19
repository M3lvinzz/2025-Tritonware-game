import pygame
import random

class Entity:
    def __init__(self, kind, x, y, image, speed):
        self.kind = kind
        self.speed = speed
        self.frame_index = 0
        self.frame_timer = 0

        self.image = image
        self.animated = isinstance(image, list)

        if image is None:
            self.rect = pygame.Rect(x, y, 25, 25)  # default size for food or other non-image entity
        else:
            base_image = image[0] if self.animated else image
            self.rect = pygame.Rect(x, y, base_image.get_width(), base_image.get_height())

    def update(self):
        self.rect.x -= self.speed  # everything moves left at its own speed

        if self.animated and self.image:
            self.frame_timer += 1
            if self.frame_timer >= 6:
                self.frame_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.image)

    def draw(self, screen):
        if self.animated:
            screen.blit(self.image[self.frame_index], self.rect)
        elif self.image:
            screen.blit(self.image, self.rect)

def spawn_entity(level, WIDTH, HEIGHT, images):
    kind = random.choice(["tree", "bird"] if level < 2 else ["tree", "bird", "car1", "car2"])

    if kind == "tree":
        size_options = [(40, 60), (50, 75), (60, 90)]
        size = random.choice(size_options)
        img = pygame.transform.scale(images[kind], size)
        y = HEIGHT - size[1]
    elif kind == "bird":
        img = images[kind]
        y = random.choice([HEIGHT - 160, HEIGHT - 140])
    else:
        img = images[kind]
        y = HEIGHT - 70

    return Entity(kind, WIDTH, y, img, speed=None)  # Speed will be set dynamically later

