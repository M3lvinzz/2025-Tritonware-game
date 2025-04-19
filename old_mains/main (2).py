import pygame
import sys
from dino import Player
from cutscenes import tutorial, level1, level2, ending, level_up_cutscene
from assets import load_images, load_image
from enemy import Entity
from boss import Boss
from ui import draw_text, draw_stamina_bar, draw_mana_icons, draw_level_progress_bar
from level import Level

pygame.init()
WIDTH, HEIGHT = 1200, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Dash")

clock = pygame.time.Clock()

# Load assets
bg_img1 = load_image("assets/background1.png", (WIDTH, HEIGHT))
bg_img2 = load_image("assets/background2.png", (WIDTH, HEIGHT))
bg_img3 = load_image("assets/background3.png", (WIDTH, HEIGHT))
food_img = load_image("assets/food.png", (40, 40))
mana_img = load_image("assets/mana.png", (40, 40))
stamina_bar_imgs = load_images("assets/stamina", 8, (30, 30))
portraits = load_images("assets/portrait", 6, (400, 400))
bullet_img = load_image("assets/bullet.png", (40, 40))


enemy_images = {
    "tree": load_image("assets/tree.png", (60, 80)),
    "bird": load_images("assets/bird", 3, (60, 60)),
    "car1": load_image("assets/car1.png", (100, 80)),
    "car2": load_image("assets/car2.png", (100, 80)),
    'barrel': load_image('assets/barrel.png', (60, 80))
}

run_imgs = load_images("assets/run", 6, (100, 100))
jump_imgs = load_images("assets/jump", 6, (100, 100))
shoot_imgs = load_images("assets/shoot", 4, (100, 100))

player = Player(50, 410, run_imgs, jump_imgs, shoot_imgs)

# ⬇️ Use level 1 background for tutorial
tutorial(screen, bg_img1, portraits)

levels = [
    Level(1, bg_img1, enemy_images, cutscene_func=None),
    Level(2, bg_img2, enemy_images, cutscene_func=level1),
    Level(3, bg_img3, enemy_images, cutscene_func=level2)
]
level = 1
current_level = levels[level - 1]

bullets = 4
stamina = 100
max_stamina = 100


boss = Boss(WIDTH + 100, -100)
boss_active = False
boss_defeated = False
boss_intro_timer = None
boss_intro_duration = 3000  # milliseconds

start_time = pygame.time.get_ticks()
bullet_cooldown = False
bullet_cooldown_time = 0
damage_cooldown = 1000
last_damage_time = 0
bullet_rects = []

def game_over():
    screen.fill((0, 0, 0))
    draw_text(screen, pygame.font.Font(None, 80), "Game Over!", 400, 200)
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

def choose_level_reward(screen, font, bg_img):
    choosing = True
    small_font = pygame.font.Font(None, 28)

    while choosing:
        screen.blit(bg_img, (0, 0))  # ⬅️ draw the background

        # Draw the prompt
        prompt1 = font.render("Level Up!", True, (255, 255, 255))
        prompt2 = small_font.render("Press [B] to Replenish Fireballs", True, (255, 255, 255))
        prompt3 = small_font.render("Press [S] to Increase Max Stamina", True, (255, 255, 255))

        screen.blit(prompt1, (WIDTH // 2 - prompt1.get_width() // 2, 180))
        screen.blit(prompt2, (WIDTH // 2 - prompt2.get_width() // 2, 240))
        screen.blit(prompt3, (WIDTH // 2 - prompt3.get_width() // 2, 280))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    return "bullets"
                elif event.key == pygame.K_s:
                    return "stamina"
            

running = True
font = pygame.font.Font(None, 36)

while running:
    dt = clock.tick(60)
    elapsed = pygame.time.get_ticks() - start_time
    if level == 3 and not boss_active and not boss_defeated and boss_intro_timer:
        if pygame.time.get_ticks() - boss_intro_timer >= boss_intro_duration:
            boss_active = True
            boss_intro_timer = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            # ⏩ DEBUG: Press A to skip to next level
            if event.key == pygame.K_a:
                if level < 3:
                    level += 1
                    current_level = levels[level - 1]
                    current_level.reset()
                    stamina = max_stamina
                    bullets = 3

                    # Trigger boss if jumping to level 3
                    if level == 3:
                        boss = Boss(WIDTH + 100, -100)
                        boss_active = False
                        boss_defeated = False
                        boss_intro_timer = pygame.time.get_ticks()

                    print(f"[DEBUG] Skipped to level {level}")

            # ⏸ Optional: add pause key here
            elif event.key == pygame.K_p:
                paused = True
                while paused:
                    for pause_event in pygame.event.get():
                        if pause_event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif pause_event.type == pygame.KEYDOWN and pause_event.key == pygame.K_p:
                            paused = False

    keys = pygame.key.get_pressed()
    bullet = player.handle_input(keys, bullets, bullet_cooldown)
    if bullet:
        bullet_rects.append(bullet)
        bullets -= 1
        bullet_cooldown = True
        bullet_cooldown_time = pygame.time.get_ticks()
        player.is_shooting = True
        player.shooting_timer = 30

    if bullet_cooldown and pygame.time.get_ticks() - bullet_cooldown_time > 300:
        bullet_cooldown = False

    player.update()
    current_level.update(elapsed, WIDTH, HEIGHT)

    # Bullet movement
    for b in bullet_rects:
        b.x += 10
    bullet_rects = [b for b in bullet_rects if b.x < WIDTH]

    current_level.draw_background(screen, WIDTH)

    # Collisions
    now = pygame.time.get_ticks()
    for entity in current_level.entities[:]:
        if player.rect.colliderect(entity.rect):
            if entity.kind == "food":
                stamina = min(100, stamina + 20)
                current_level.entities.remove(entity)
            else:
                if now - last_damage_time > damage_cooldown:
                    stamina -= 20
                    last_damage_time = now

    for bullet in bullet_rects[:]:
        for entity in current_level.entities[:]:
            if entity.kind != "food" and bullet.colliderect(entity.rect):
                bullet_rects.remove(bullet)
                current_level.entities.remove(entity)
                break

    # Draw player (includes its hitbox now)
    player.draw(screen)

    # Draw obstacles and food (with hitboxes)
    current_level.draw_objects(screen, food_img)

    # Draw bullets with hitboxes
    for b in bullet_rects:
        screen.blit(bullet_img, (b.x, b.y))
        pygame.draw.rect(screen, (255, 255, 0), b, 2)
        
    if boss_active:
        pygame.draw.rect(screen, (255, 255, 255), (boss.rect.x, boss.rect.y - 10, 100, 6))
        pygame.draw.rect(screen, (255, 0, 0), (boss.rect.x, boss.rect.y - 10, 100 * (boss.health / 3), 6))

        now = pygame.time.get_ticks()
        boss.update_position()
        boss.shoot(now)
        boss.update_bullets()

        boss.draw(screen)

        # Check boss bullet collisions
        for b in boss.bullets:
            bullet_rect = pygame.Rect(b["x"], b["y"], 10, 10)
            if player.rect.colliderect(bullet_rect):
                if pygame.time.get_ticks() - last_damage_time > damage_cooldown:
                    stamina -= 20
                    last_damage_time = pygame.time.get_ticks()
                    if stamina <= 0:
                        game_over()

        # Check if player's bullets hit boss
        for bullet in bullet_rects[:]:
            if boss.rect.colliderect(bullet):
                bullet_rects.remove(bullet)
                boss.health -= 1
                if boss.health <= 0:
                    boss_defeated = True
                    boss_active = False

    # UI overlays
    draw_text(screen, font, f"Level: {level}", 20, 20)
    draw_stamina_bar(screen, stamina, stamina_bar_imgs)
    draw_mana_icons(screen, mana_img, bullets, (160, 40))
    draw_level_progress_bar(screen, elapsed, level, WIDTH)


    # Level transition logic
    new_level = min(3, elapsed // current_level.duration + 1)
    if new_level != level:
        level = new_level
        current_level = levels[level - 1]
        current_level.reset()

        # Choose correct background for the current level
        bg_for_cutscene = bg_img1 if level == 2 else bg_img2

        # ⬇️ 1. Show unskippable level-up reward
        reward = choose_level_reward(screen, font, bg_for_cutscene)
        if reward == "bullets":
            bullets = 4
        elif reward == "stamina":
            max_stamina += 20
            stamina = max_stamina

        # ⬇️ 2. Optional cutscene after reward
        if current_level.cutscene_func:
            current_level.cutscene_func(screen, bg_for_cutscene, portraits)

    stamina -= 0.025  # Decrease slowly over time
    if stamina <= 0:
        stamina = 0
        game_over()

    if level == 3:
        boss = Boss(WIDTH + 100, -100)
        boss_active = False
        boss_defeated = False
        boss_intro_timer = pygame.time.get_ticks()

    pygame.display.flip()
