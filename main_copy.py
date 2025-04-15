import pygame
import random
import sys
from dino import Player

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 1200, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Dash")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

def load_images(prefix, count, scale):
    return [
        pygame.transform.scale(pygame.image.load(f"{prefix}{i}.png").convert_alpha(), scale)
        for i in range(1, count + 1)
    ]

dino_run_imgs = load_images("assets/run", 6, (100, 100))
dino_jump_imgs = load_images("assets/jump", 6, (100, 100))
dino_shoot_imgs = load_images("assets/shoot", 4, (100, 100))

food_img = pygame.transform.scale(pygame.image.load("assets/food.png").convert_alpha(), (40, 40))

tree_img = pygame.transform.scale(pygame.image.load("assets/tree.png").convert_alpha(), (60, 80))

car1_img = pygame.transform.scale(pygame.image.load("assets/car1.png").convert_alpha(), (60, 40))
car2_img = pygame.transform.scale(pygame.image.load("assets/car2.png").convert_alpha(), (60, 40))

mana_img = pygame.transform.scale(pygame.image.load("assets/mana.png").convert_alpha(), (40, 40))

bird_imgs = load_images('assets/bird', 3, (70, 70))

stamina_bar_imgs = load_images('assets/stamina', 8, (30, 30))

bg_img1 = pygame.transform.scale(pygame.image.load("assets/background1.png").convert(), (WIDTH, HEIGHT))
bg_img2 = pygame.transform.scale(pygame.image.load("assets/background2.png").convert(), (WIDTH, HEIGHT))

bg_x = 0

pygame.mixer.music.load("music/forestbgm.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

WHITE = (255, 255, 255)
BULLET_COLOR = (255, 255, 0)
BG_COLOR = (180, 240, 255)

player = Player(50, HEIGHT - 100, dino_run_imgs, dino_jump_imgs, dino_shoot_imgs)

bullets = 3
stamina = 100
enemies = []
foods = []
bullets_fired = []
level = 1
start_time = pygame.time.get_ticks()
LEVEL_DURATION = 30000
spawn_timer = 0
bullet_cooldown = False
bullet_cooldown_time = 0
last_damage_time = 0
damage_cooldown = 1000

portraits = load_images('assets/portrait', count = 6, scale = (60, 60))

def draw_text(text, x, y):
    label = font.render(text, True, WHITE)
    screen.blit(label, (x, y))

def spawn_obstacle():
    if level == 2:
        kind = random.choice(["car1", "car2", "tree", "bird"])
    else:
        kind = random.choice(["tree", "bird"])

    if kind == "tree":
        rect = pygame.Rect(WIDTH, HEIGHT - 80, 40, 60)
    elif kind == "bird":
        bird_y = random.choice([HEIGHT - 160, HEIGHT - 120])
        rect = pygame.Rect(WIDTH, bird_y, 40, 40)
    elif kind == "car1" or kind == "car2":
        rect = pygame.Rect(WIDTH, HEIGHT - 70, 60, 40)
    enemies.append({"rect": rect, "type": kind})

def spawn_foods():
    food_rect = pygame.Rect(WIDTH, random.randint(HEIGHT - 120, HEIGHT - 60), 25, 25)
    foods.append(food_rect)

def draw_level_timer(elapsed, level):
    level_start_time = (level - 1) * LEVEL_DURATION
    level_elapsed = max(0, elapsed - level_start_time)
    level_remaining = max(0, LEVEL_DURATION - level_elapsed)

    progress_width = 200
    fill_width = int(progress_width * (level_elapsed / LEVEL_DURATION))

    pygame.draw.rect(screen, WHITE, (950, 20, progress_width, 20), 2)
    pygame.draw.rect(screen, (0, 200, 0), (950, 20, fill_width, 20))

def handle_collisions():
    global stamina, last_damage_time
    now = pygame.time.get_ticks()
    for enemy in enemies:
        if player.rect.colliderect(enemy["rect"]):
            if now - last_damage_time > damage_cooldown:
                stamina -= 20
                last_damage_time = now
            if stamina <= 0:
                game_over()

    for food in foods[:]:
        if player.rect.colliderect(food):
            stamina = min(100, stamina + 20)
            foods.remove(food)

    for bullet in bullets_fired[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy["rect"]):
                enemies.remove(enemy)
                if bullet in bullets_fired:
                    bullets_fired.remove(bullet)
                break

def game_over():
    screen.fill(BG_COLOR)
    draw_text("Game Over!", 330, 120)
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

def win_game():
    screen.fill(BG_COLOR)
    draw_text("You Win!", 350, 120)
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

def level_up():
    global bullets, stamina
    choosing = True
    while choosing:
        screen.fill(BG_COLOR)
        draw_text("Level Up! Choose a reward:", 250, 100)
        draw_text("Press B to Refill Bullets", 270, 140)
        draw_text("Press S to Boost Stamina", 270, 180)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    bullets = 3
                    choosing = False
                elif event.key == pygame.K_s:
                    stamina = min(100, stamina + 30)
                    choosing = False

bird_frame_index = 0
bird_frame_timer = 0

running = True
while running:
    dt = clock.tick(60)
    elapsed = pygame.time.get_ticks() - start_time
    screen.fill(BG_COLOR)

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
    new_bullet = player.handle_input(keys, bullets, bullet_cooldown)
    if new_bullet:
        bullets_fired.append(new_bullet)
        bullets -= 1
        bullet_cooldown = True
        bullet_cooldown_time = pygame.time.get_ticks()

    if bullet_cooldown and pygame.time.get_ticks() - bullet_cooldown_time > 300:
        bullet_cooldown = False

    player.update()

    spawn_timer += 1
    if spawn_timer > 60:
        if random.random() < 0.7:
            spawn_obstacle()
        else:
            spawn_foods()
        spawn_timer = 0

    for enemy in enemies:
        enemy["rect"].x -= int(game_speed)
    enemies = [e for e in enemies if e["rect"].x + e["rect"].width > 0]

    for food in foods:
        food.x -= int(game_speed)
    foods = [f for f in foods if f.x + f.width > 0]

    for bullet in bullets_fired:
        bullet.x += 10
    bullets_fired = [b for b in bullets_fired if b.x < WIDTH]

    handle_collisions()

    player.draw(screen)

    for enemy in enemies:
        if enemy["type"] == "tree":
            screen.blit(tree_img, enemy["rect"])
        elif enemy["type"] == "bird":
            screen.blit(bird_imgs[bird_frame_index], enemy["rect"])
        elif enemy["type"] == "car1":
            screen.blit(car1_img, enemy["rect"])
        elif enemy["type"] == "car2":
            screen.blit(car2_img, enemy["rect"])

    draw_level_timer(elapsed, level)

    for food in foods:
        screen.blit(food_img, food)

    for bullet in bullets_fired:
        pygame.draw.rect(screen, BULLET_COLOR, bullet)

    draw_text(f"Level: {level}", 20, 20)

    bar_x, bar_y = 20, 50
    bar_width, bar_height = 100, 20
    bar_fill = int((stamina / 100) * bar_width)

    pygame.draw.rect(screen, (255,255,255), (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(screen, (0,255,0), (bar_x, bar_y, bar_fill, bar_height))

    stamina_index = 7 - min(7, stamina // 13)
    stamina_img = stamina_bar_imgs[stamina_index]
    screen.blit(stamina_img, (bar_x + bar_width + 10, bar_y - 10))

    for i in range(bullets):
        screen.blit(mana_img, (bar_x + bar_width + 50 + i * 35, bar_y - 10))

    pygame.display.flip()
