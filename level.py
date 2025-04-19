import pygame
import random
from enemy import spawn_entity, Entity

class Level:
    def __init__(self, number, bg_image, enemy_images, cutscene_func=None, duration = 30000):
        self.number = number
        self.bg_image = bg_image
        self.enemy_images = enemy_images
        self.cutscene_func = cutscene_func

        self.entities = []
        self.bg_x = 0
        self.spawn_timer = 0
        self.food_timer = 0
        self.spawn_interval = 80
        self.food_interval = 180
        self.scroll_speed = 4 + number
        self.complete = False
        self.duration = duration  # ms per level

    def update(self, elapsed_time, WIDTH, HEIGHT):
        self.bg_x -= self.scroll_speed
        if self.bg_x <= -WIDTH:
            self.bg_x = 0

        self.spawn_timer += 1
        self.food_timer += 1

        # Spawn obstacles (trees, birds, cars)
        if self.spawn_timer >= self.spawn_interval:
            new_entity = spawn_entity(self.number, WIDTH, HEIGHT, self.enemy_images)
            # Prevent overlap with other non-food entities
            if not any(new_entity.rect.colliderect(e.rect.inflate(20, 20)) for e in self.entities if e.kind != "food"):
                self.entities.append(new_entity)
            self.spawn_timer = 0

        # Spawn food
        if self.food_timer >= self.food_interval:
            new_food = spawn_food(WIDTH, HEIGHT, self.scroll_speed)

            # Only add if not overlapping other entities
            if not any(new_food.rect.colliderect(e.rect.inflate(10, 10)) for e in self.entities):
                self.entities.append(new_food)
            self.food_timer = 0

        # Update positions
        for entity in self.entities:
            entity.speed = self.scroll_speed  # 🔥 force consistent scroll speed
            entity.update()

        # Remove off-screen entities
        self.entities = [e for e in self.entities if e.rect.right > 0]

    def draw_background(self, screen, WIDTH):
        screen.blit(self.bg_image, (self.bg_x, 0))
        screen.blit(self.bg_image, (self.bg_x + WIDTH, 0))

    def draw_objects(self, screen, food_img):
        for e in self.entities:
            if e.kind == "food":
                screen.blit(food_img, e.rect)
                pygame.draw.rect(screen, (0, 255, 0), e.rect, 2)
            else:
                e.draw(screen)
                pygame.draw.rect(screen, (255, 0, 0), e.rect, 2)

    def reset(self):
        self.foods = []
        self.obstacles = []
        self.bg_x = 0
        self.spawn_timer = 0
        self.food_timer = 0
        self.complete = False

def spawn_food(WIDTH, HEIGHT, scroll_speed):
    rect = pygame.Rect(WIDTH, random.randint(HEIGHT - 120, HEIGHT - 60), 25, 25)
    return Entity("food", rect.x, rect.y, None, speed=scroll_speed)
