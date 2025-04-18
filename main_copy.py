import pygame
import random
import math
import sys
from dino import Player
from cutscene_test import *

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flying Boss Fight - Fixed")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)
BG_COLOR = (30, 30, 30)

# Player setup
player = pygame.Rect(50, HEIGHT - 60, 40, 40)
player_velocity_y = 0
gravity = 1.2
jump_velocity = -15
is_jumping = False
bullets = []

# Boss setup
boss = pygame.Rect(600, 100, 100, 100)
boss_active = True
boss_health = 3
boss_bullets = []
boss_attack_type = "bullet_fan"
boss_attack_timer = 0
next_attack_time = 3000
spiral_angle = 0
move_timer = 0
boss_target = pygame.Vector2(boss.x, boss.y)

# Game state
running = True
bullet_cooldown = False
bullet_timer = 0

def draw_text(text, x, y):
    label = font.render(text, True, WHITE)
    screen.blit(label, (x, y))

while running:
    dt = clock.tick(60)
    now = pygame.time.get_ticks()
    screen.fill(BG_COLOR)

    tutorial(screen, current_bg, portraits)

    game_speed = 5 + level + (elapsed / 15000)
    bg_x -= int(game_speed * 0.5)
    if bg_x <= -WIDTH:
        bg_x = 0
    current_bg = bg_img1 if level != 2 else bg_img2
    screen.blit(current_bg, (bg_x, 0))
    screen.blit(current_bg, (bg_x + WIDTH, 0))

    bird_frame_timer += 1
    if bird_frame_timer > 5:
        bird_frame_index = (bird_frame_index + 1) % len(bird_imgs)
        bird_frame_timer = 0

    current_level = min(3, elapsed // LEVEL_DURATION + 1)
    if current_level != level:
        level = current_level
        if level <= 3:
            level_up()
    if level > 3:
        win_game()

    if pygame.time.get_ticks() % 1000 < 20:
        stamina -= 1
        if stamina <= 0:
            game_over()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # === Player Movement ===
    if keys[pygame.K_UP] and not is_jumping:
        player_velocity_y = jump_velocity
        is_jumping = True

    if keys[pygame.K_RIGHT] and not bullet_cooldown:
        bullets.append(pygame.Rect(player.right, player.centery - 5, 10, 5))
        bullet_cooldown = True
        bullet_timer = now

    if bullet_cooldown and now - bullet_timer > 300:
        bullet_cooldown = False

    player_velocity_y += gravity
    player.y += player_velocity_y
    if player.y >= HEIGHT - 60:
        player.y = HEIGHT - 60
        is_jumping = False

    # === Player Bullets ===
    for bullet in bullets:
        bullet.x += 10
    bullets = [b for b in bullets if b.x < WIDTH]

    # === Boss Flying Movement ===
    if boss_active:
        # Every few seconds, change flight target
        if now - move_timer > 2000:
            boss_target = pygame.Vector2(
                random.randint(400, WIDTH - 100),
                random.randint(20, HEIGHT // 2)
            )
            move_timer = now

        # Smooth movement toward target
        dir_vec = boss_target - pygame.Vector2(boss.x, boss.y)
        if dir_vec.length() > 1:
            dir_vec = dir_vec.normalize() * 2
            boss.x += int(dir_vec.x)
            boss.y += int(dir_vec.y)

        # === Boss Attack Logic ===
        if now - boss_attack_timer > next_attack_time:
            boss_attack_type = random.choice(["bullet_fan", "spiral"])
            boss_attack_timer = now

        # Bullet Fan
        if boss_attack_type == "bullet_fan" and now % 1500 < 20:
            for i in range(-3, 4):
                angle = i * 0.3
                boss_bullets.append({
                    "x": boss.centerx,
                    "y": boss.centery,
                    "vx": 5 * math.cos(angle),
                    "vy": 5 * math.sin(angle)
                })

        # Spiral Bullets
        if boss_attack_type == "spiral" and now % 100 < 10:
            spiral_angle += 0.2
            boss_bullets.append({
                "x": boss.centerx,
                "y": boss.centery,
                "vx": 4 * math.cos(spiral_angle),
                "vy": 4 * math.sin(spiral_angle)
            })

        # Move Boss Bullets
        for b in boss_bullets:
            b["x"] += b["vx"]
            b["y"] += b["vy"]
        boss_bullets = [b for b in boss_bullets if 0 <= b["x"] <= WIDTH and 0 <= b["y"] <= HEIGHT]

        # Collision: Boss Bullets → Player
        for b in boss_bullets:
            if player.colliderect(pygame.Rect(b["x"], b["y"], 10, 10)):
                print("You were hit!")
                running = False

        # Collision: Player Bullets → Boss
        for bullet in bullets[:]:
            if boss.colliderect(bullet):
                bullets.remove(bullet)
                boss_health -= 1
                if boss_health <= 0:
                    boss_active = False
                    print("Boss defeated!")

    # === Draw ===
    pygame.draw.rect(screen, GREEN, player)
    for bullet in bullets:
        pygame.draw.rect(screen, YELLOW, bullet)

    for b in boss_bullets:
        pygame.draw.circle(screen, RED, (int(b["x"]), int(b["y"])), 5)

    if boss_active:
        pygame.draw.rect(screen, RED, boss)
        pygame.draw.rect(screen, WHITE, (300, 20, 200, 20), 2)
        pygame.draw.rect(screen, RED, (300, 20, boss_health * 66, 20))
        hint = "!!!" if boss_attack_type == "bullet_fan" else "@@"
        draw_text(hint, boss.centerx - 10, boss.y - 30)

    draw_text("↑ Jump | → Shoot", 20, 20)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
sys.exit()
