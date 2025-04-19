import pygame
import math
import random

class Boss:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 100, 100)
        self.target = pygame.Vector2(x, y)
        self.health = 3
        self.bullets = []
        self.attack_type = "bullet_fan"
        self.attack_timer = 0
        self.move_timer = 0
        self.spiral_angle = 0
        self.active = False
        self.appearing = False
        self.entry_timer = 0
        self.warning_active = False
        self.last_fan_fire = 0

        self.target_x = 900
        self.target_y = 60

    def start_entry(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.appearing = True
        self.entry_timer = pygame.time.get_ticks()
        self.active = False

    def update_entry(self):
        if self.appearing:
            self.rect.x += (self.target_x - self.rect.x) * 0.05
            self.rect.y += (self.target_y - self.rect.y) * 0.05
            if abs(self.rect.x - self.target_x) < 2 and abs(self.rect.y - self.target_y) < 2:
                self.rect.x = self.target_x
                self.rect.y = self.target_y
                self.appearing = False
                self.active = True
                self.move_timer = pygame.time.get_ticks()
                self.attack_timer = pygame.time.get_ticks()

    def update_position(self):
        now = pygame.time.get_ticks()
        if now - self.move_timer > 2000:
            self.target = pygame.Vector2(
                random.randint(600, 1100),
                random.randint(20, 200)
            )
            self.move_timer = now

        direction = self.target - pygame.Vector2(self.rect.x, self.rect.y)
        if direction.length() > 1:
            direction = direction.normalize() * 2
            self.rect.x += int(direction.x)
            self.rect.y += int(direction.y)

    def update_attack(self):
        now = pygame.time.get_ticks()

        if now - self.attack_timer > 3000:
            self.attack_type = random.choice(["bullet_fan", "spiral"])
            self.attack_timer = now

        if self.attack_type == "bullet_fan" and now % 1500 < 20:
            base_angle = math.pi
            for i in range(-3, 4):
                angle = base_angle + i * 0.2
                self.bullets.append({
                    "x": self.rect.centerx,
                    "y": self.rect.centery,
                    "vx": 8 * math.cos(angle),
                    "vy": 8 * math.sin(angle)
                })

        if self.attack_type == "spiral" and now % 100 < 10:
            self.spiral_angle -= 0.2
            self.bullets.append({
                "x": self.rect.centerx,
                "y": self.rect.centery,
                "vx": 7 * math.cos(self.spiral_angle),
                "vy": 7 * math.sin(self.spiral_angle)
            })

    def update_bullets(self, screen_width, screen_height):
        for b in self.bullets:
            b["x"] += b["vx"]
            b["y"] += b["vy"]
        self.bullets = [b for b in self.bullets if 0 <= b["x"] <= screen_width and 0 <= b["y"] <= screen_height]

    def draw(self, screen, font=None):
        RED = (255, 50, 50)
        WHITE = (255, 255, 255)
        pygame.draw.rect(screen, RED, self.rect)
        pygame.draw.rect(screen, WHITE, (450, 20, 200, 20), 2)
        pygame.draw.rect(screen, RED, (450, 20, self.health * 66, 20))
        hint = "!!!" if self.attack_type == "bullet_fan" else "@@"
        if font:
            label = font.render(hint, True, WHITE)
            screen.blit(label, (self.rect.centerx - 10, self.rect.y - 30))

    def draw_bullets(self, screen):
        for b in self.bullets:
            pygame.draw.circle(screen, (255, 50, 50), (int(b["x"]), int(b["y"])), 5)
            
    def is_ready(self):
        return self.active and not self.appearing
