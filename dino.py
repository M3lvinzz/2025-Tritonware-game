import pygame
import random

class Player:
    def __init__(self, x, y, run_imgs, jump_imgs, shoot_imgs):
        self.rect = pygame.Rect(x, y, 40, 60)
        self.run_imgs = run_imgs
        self.jump_imgs = jump_imgs
        self.shoot_imgs = shoot_imgs

        self.gravity = 1.2
        self.jump_velocity = -20
        self.velocity_y = 0
        self.is_jumping = False
        self.jump_key_held = False  # Track jump key hold
        self.is_shooting = False
        self.shooting_timer = 0

        self.state = "run"
        self.frame_index = 0
        self.frame_timer = 0

    def handle_input(self, keys, bullets, bullet_cooldown):
        new_bullet = None

        # Jump logic
        if keys[pygame.K_UP]:
            if not self.is_jumping:
                self.velocity_y = self.jump_velocity
                self.is_jumping = True
            self.jump_key_held = True
        else:
            self.jump_key_held = False

        # Shoot logic
        if keys[pygame.K_RIGHT] and bullets > 0 and not bullet_cooldown:
            self.action = "shoot"
            self.frame_index = 0
            new_bullet = pygame.Rect(self.rect.right, self.rect.centery - 5, 10, 5)

        return new_bullet

    def update(self):
        # Gravity / Jump physics
        if self.is_jumping:
            if not self.jump_key_held and self.velocity_y < 0:
                self.velocity_y *= 0.5  # Short hop if jump key released early

            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y

            if self.rect.y >= 410:  # Ground level
                self.rect.y = 410
                self.is_jumping = False
                self.velocity_y = 0

        # Animation state logic
        if self.is_jumping:
            self.state = "jump"
        elif self.is_shooting:
            self.state = "shoot"
        else:
            self.state = "run"

        # Handle shoot duration
        if self.shooting_timer > 0:
            self.shooting_timer -= 1
        else:
            self.is_shooting = False

        # Frame animation update (slower)
        self.frame_timer += 1
        if self.frame_timer > 10:
            self.frame_timer = 0
            self.frame_index += 1

            if self.state == "run":
                self.frame_index %= len(self.run_imgs)
            elif self.state == "jump":
                self.frame_index %= len(self.jump_imgs)
            elif self.state == "shoot":
                if self.frame_index >= len(self.shoot_imgs):
                    self.frame_index = 0
                    self.is_shooting = False

    def draw(self, screen):
        if self.state == "run":
            screen.blit(self.run_imgs[self.frame_index], self.rect)
        elif self.state == "jump":
            screen.blit(self.jump_imgs[self.frame_index], self.rect)
        elif self.state == "shoot":
            screen.blit(self.shoot_imgs[self.frame_index], self.rect)
        elif hasattr(self, 'action') and self.action == "shoot":
            index = self.frame_index % len(self.shoot_imgs)
            screen.blit(self.shoot_imgs[index], self.rect)
