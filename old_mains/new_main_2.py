import pygame
import sys
from dino import Player
from cutscenes import tutorial, level1, level2, ending
from assets import load_images, load_image
from enemy import Obstacle
from boss import Boss
from ui import draw_text, draw_stamina_bar, draw_mana_icons
from level import Level

pygame.init()
WIDTH, HEIGHT = 1200, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Dash")

clock = pygame.time.Clock()

# Load assets
bg_img1 = load_image("assets/background1.png", (WIDTH, HEIGHT))
bg_img2 = load_image("assets/background2.png", (WIDTH, HEIGHT))
food_img = load_image("assets/food.png", (40, 40))
mana_img = load_image("assets/mana.png", (40, 40))
stamina_bar_imgs = load_images("assets/stamina", 8, (30, 30))
portraits = load_images("assets/portrait", 6, (400, 400))

enemy_images = {
    "tree": load_image("assets/tree.png", (60, 80)),
    "bird": load_image("assets/bird1.png", (80, 80)),
    "car1": load_image("assets/car1.png", (100, 80)),
    "car2": load_image("assets/car2.png", (100, 80)),
}

run_imgs = load_images("assets/run", 6, (100, 100))
jump_imgs = load_images("assets/jump", 6, (100, 100))
shoot_imgs = load_images("assets/shoot", 4, (100, 100))

player = Player(50, 410, run_imgs, jump_imgs, shoot_imgs)

bg_image = load_image("assets/bg/cutscene_bg.png")
tutorial(screen, bg_image, portraits)

levels = [
    Level(1, bg_img1, enemy_images, cutscene_func=None),
    Level(2, bg_img2, enemy_images, cutscene_func=level1),
    Level(3, bg_img2, enemy_images, cutscene_func=level2)
]
level = 1
current_level = levels[level - 1]

bullets = 3
stamina = 100
boss = Boss(WIDTH + 100, -100)

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

running = True
font = pygame.font.Font(None, 36)

while running:
    dt = clock.tick(60)
    elapsed = pygame.time.get_ticks() - start_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
    for obs in current_level.obstacles:
        if player.rect.colliderect(obs.rect):
            if now - last_damage_time > damage_cooldown:
                stamina -= 20
                last_damage_time = now

    for food in current_level.foods[:]:
        if player.rect.colliderect(food):
            stamina = min(100, stamina + 20)
            current_level.foods.remove(food)

    for bullet in bullet_rects[:]:
        for obs in current_level.obstacles[:]:
            if bullet.colliderect(obs.rect):
                bullet_rects.remove(bullet)
                current_level.obstacles.remove(obs)
                break

    # Draw player (includes its hitbox now)
    player.draw(screen)

    # Draw obstacles and food (with hitboxes)
    current_level.draw_objects(screen, food_img)

    # Draw bullets with hitboxes
    for b in bullet_rects:
        screen.blit(mana_img, (b.x, b.y))
        pygame.draw.rect(screen, (255, 255, 0), b, 2)

    # UI overlays
    draw_text(screen, font, f"Level: {level}", 20, 20)
    draw_stamina_bar(screen, stamina, stamina_bar_imgs)
    draw_mana_icons(screen, mana_img, bullets, (160, 40))

    # Level transition logic
    new_level = min(3, elapsed // current_level.duration + 1)
    if new_level != level:
        level = new_level
        current_level = levels[level - 1]
        current_level.reset()
        bullets = 3
        stamina = min(100, stamina + 30)
        if current_level.cutscene_func:
            current_level.cutscene_func(screen, bg_image, portraits)
        if level == 3:
            boss = Boss(WIDTH + 100, -100)

    if stamina <= 0:
        game_over()

    pygame.display.flip()
