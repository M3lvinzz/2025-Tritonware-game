import pygame
import sys
from dino import Player
from cutscenes import tutorial, level1, level2, ending, level_up_cutscene
from assets import load_images, load_image
from enemy import Entity
from ui import draw_text, draw_stamina_bar, draw_mana_icons, draw_level_progress_bar
from level import Level
from boss import Boss

pygame.init()
WIDTH, HEIGHT = 1200, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Dash")
clock = pygame.time.Clock()

# Load assets
bg_img1 = load_image("assets/background1.png", (WIDTH, HEIGHT))
bg_img2 = load_image("assets/background2.png", (WIDTH, HEIGHT))
bg_img3 = load_image("assets/background3.png", (WIDTH, HEIGHT))
game_over_img1 = pygame.transform.scale(pygame.image.load("assets/gameover1.png").convert(), (WIDTH, HEIGHT))
game_over_img2 = pygame.transform.scale(pygame.image.load("assets/gameover2.png").convert(), (WIDTH, HEIGHT))
game_over_img3 = pygame.transform.scale(pygame.image.load("assets/gameover3.png").convert(), (WIDTH, HEIGHT))
game_over_img4 = pygame.transform.scale(pygame.image.load("assets/gameover4.png").convert(), (WIDTH, HEIGHT))

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
    "barrel": load_image("assets/barrel.png", (60, 80)),
}

run_imgs = load_images("assets/run", 6, (100, 100))
jump_imgs = load_images("assets/jump", 6, (100, 100))
shoot_imgs = load_images("assets/shoot", 4, (100, 100))

player = Player(50, 410, run_imgs, jump_imgs, shoot_imgs)
boss = Boss(WIDTH + 100, -100)
boss_active = False
boss_appearing = False
boss_intro_timer = None
boss_intro_active = False
boss_initialized = False

tutorial(screen, bg_img1, portraits)

levels = [
    Level(1, bg_img1, enemy_images, cutscene_func=None, duration=30000),
    Level(2, bg_img2, enemy_images, cutscene_func=level1, duration=40000),
    Level(3, bg_img3, enemy_images, cutscene_func=level2, duration=50000),
]
level = 1
current_level = levels[level - 1]
level_start_time = pygame.time.get_ticks()
first_time_no = True

bullets = 4
stamina = 100
max_stamina = 100

bullet_cooldown = False
bullet_cooldown_time = 0
damage_cooldown = 1000
last_damage_time = 0
bullet_rects = []

def game_over():
    global first_time_no
    choosing = True
    state = 1
    state3_start_time = None
    while choosing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if state == 1 and event.key == pygame.K_RIGHT:
                    state = 2
                elif state == 2:
                    if event.key == pygame.K_RETURN:
                        if first_time_no:
                            state = 3
                            state3_start_time = pygame.time.get_ticks()
                            first_time_no = False
                        else:
                            pygame.quit()
                            sys.exit()
                    elif event.key == pygame.K_LEFT:
                        state = 1
                elif state == 1 and event.key == pygame.K_RETURN:
                    reset_game()
                    return
                elif state == 4 and event.key == pygame.K_RETURN:
                    reset_game()
                    return
        if state == 3 and state3_start_time:
            elapsed = pygame.time.get_ticks() - state3_start_time
            if elapsed >= 1500:
                state = 4
                state3_start_time = None
        if state == 1:
            screen.blit(game_over_img1, (0, 0))
        elif state == 2:
            screen.blit(game_over_img2, (0, 0))
        elif state == 3:
            screen.blit(game_over_img3, (0, 0))
        elif state == 4:
            screen.blit(game_over_img4, (0, 0))
        pygame.display.flip()

def reset_game():
    global bullets, stamina, level, level_start_time, bullet_cooldown, bullet_cooldown_time, last_damage_time
    bullets = 4
    stamina = 100
    level = 1
    level_start_time = pygame.time.get_ticks()
    bullet_cooldown = False
    bullet_cooldown_time = 0
    last_damage_time = 0

def choose_level_reward(screen, font, bg_img):
    choosing = True
    small_font = pygame.font.Font(None, 28)
    while choosing:
        screen.blit(bg_img, (0, 0))
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
    elapsed = pygame.time.get_ticks() - level_start_time
    if level == 3:
        if boss_appearing:
            boss.update_entry()
            if boss.is_ready():
                boss_active = True
                boss_appearing = False
                boss.reset_attack_timer()
        if boss_active:
            boss.update_position()
            boss.attack()
            boss.update_bullets()
            for b in boss.bullets:
                bullet_rect = pygame.Rect(b["x"], b["y"], 10, 10)
                if player.rect.colliderect(bullet_rect):
                    if pygame.time.get_ticks() - last_damage_time > damage_cooldown:
                        stamina -= 20
                        last_damage_time = pygame.time.get_ticks()
                        if stamina <= 0:
                            game_over()
            for bullet in bullet_rects[:]:
                if boss.rect.colliderect(bullet):
                    bullet_rects.remove(bullet)
                    boss.health -= 1
                    if boss.health <= 0:
                        boss_active = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
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
    for b in bullet_rects:
        b.x += 10
    bullet_rects = [b for b in bullet_rects if b.x < WIDTH]

    current_level.draw_background(screen, WIDTH)
    now = pygame.time.get_ticks()
    for entity in current_level.entities[:]:
        if player.rect.colliderect(entity.rect):
            if entity.kind == "food":
                stamina = min(max_stamina, stamina + 20)
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

    player.draw(screen)
    current_level.draw_objects(screen, food_img)
    for b in bullet_rects:
        screen.blit(bullet_img, (b.x, b.y))
        pygame.draw.rect(screen, (255, 255, 0), b, 2)

    if boss_active or boss_appearing:
        boss.draw(screen)
        pygame.draw.rect(screen, (255, 255, 255), (450, 20, 200, 20), 2)
        pygame.draw.rect(screen, (255, 0, 0), (450, 20, 200 * (boss.health / 3), 20))

    draw_text(screen, font, f"Level: {level}", 20, 20)
    draw_stamina_bar(screen, stamina, stamina_bar_imgs)
    draw_mana_icons(screen, mana_img, bullets, (160, 40))
    draw_level_progress_bar(screen, elapsed, current_level.duration, WIDTH)

    if elapsed > current_level.duration:
        level += 1
        if level > len(levels):
            running = False
            break
        current_level = levels[level - 1]
        current_level.reset()
        level_start_time = pygame.time.get_ticks()

        bg_for_cutscene = bg_img1 if level == 1 else bg_img2 if level == 2 else bg_img3
        reward = choose_level_reward(screen, font, bg_for_cutscene)
        if reward == "bullets":
            bullets = 4
        elif reward == "stamina":
            max_stamina += 20
            stamina = max_stamina
        if current_level.cutscene_func:
            current_level.cutscene_func(screen, bg_for_cutscene, portraits)
        if level == 3 and not boss_initialized:
            boss.start_entry(WIDTH - 300, 60)
            boss_active = False
            boss_appearing = True
            boss_intro_timer = pygame.time.get_ticks()
            boss_intro_active = True
            boss_initialized = True

    stamina -= 0.025
    stamina = max(0, stamina)
    if stamina <= 0:
        game_over()

    pygame.display.flip()