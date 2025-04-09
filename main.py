import pygame
import random
import sys

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Sprint: Elemental Run")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Colors
WHITE = (255, 255, 255)
DINO_COLOR = (0, 200, 0)
TREE_COLOR = (139, 69, 19)
BIRD_COLOR = (50, 100, 255)
FRUIT_COLOR = (255, 100, 0)
BULLET_COLOR = (255, 255, 0)
BG_COLOR = (180, 240, 255)

# Dino setup
dino = pygame.Rect(50, 220, 40, 40)
gravity = 1.2
jump_velocity = -16
dino_velocity_y = 0
is_jumping = False

# Game state
score = 0
bullets = 3
stamina = 0
enemies = []
fruits = []
bullets_fired = []
level = 1
start_time = pygame.time.get_ticks()
LEVEL_DURATION = 30000
spawn_timer = 0


def draw_text(text, x, y):
    label = font.render(text, True, WHITE)
    screen.blit(label, (x, y))


def spawn_obstacle():
    kind = random.choice(["tree", "bird"])
    if kind == "tree":
        rect = pygame.Rect(WIDTH, 220, 30, 40)
    else:
        bird_y = random.randint(120, 180)
        rect = pygame.Rect(WIDTH, bird_y, 30, 30)
    enemies.append({"rect": rect, "type": kind})


def spawn_fruit():
    fruit_rect = pygame.Rect(WIDTH, random.randint(180, 240), 20, 20)
    fruits.append(fruit_rect)


def handle_collisions():
    global score, stamina
    for enemy in enemies:
        if dino.colliderect(enemy["rect"]):
            game_over()

    for fruit in fruits[:]:
        if dino.colliderect(fruit):
            stamina += 10
            fruits.remove(fruit)

    for bullet in bullets_fired[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy["rect"]):
                enemies.remove(enemy)
                if bullet in bullets_fired:
                    bullets_fired.remove(bullet)
                break


def game_over():
    print("Game Over! Final Score:", int(score))
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
                    stamina += 20
                    choosing = False

# Main loop
running = True
while running:
    dt = clock.tick(60)
    elapsed = pygame.time.get_ticks() - start_time
    screen.fill(BG_COLOR)

    # LEVEL PROGRESSION
    current_level = min(3, elapsed // LEVEL_DURATION + 1)
    if current_level != level:
        level = current_level
        level_up()

    game_speed = 5 + level + (elapsed / 15000)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and not is_jumping:
        dino_velocity_y = jump_velocity
        is_jumping = True

    if keys[pygame.K_RIGHT] and bullets > 0:
        bullet = pygame.Rect(dino.right, dino.centery - 5, 15, 10)
        bullets_fired.append(bullet)
        bullets -= 1

    # Jump physics
    if is_jumping:
        dino_velocity_y += gravity
        dino.y += dino_velocity_y
        if dino.y >= 220:
            dino.y = 220
            is_jumping = False
            dino_velocity_y = 0

    # Spawning
    spawn_timer += 1
    if spawn_timer > 60:
        if random.random() < 0.7:
            spawn_obstacle()
        else:
            spawn_fruit()
        spawn_timer = 0

    # Move enemies and bullets
    for enemy in enemies:
        enemy["rect"].x -= int(game_speed)
    enemies = [e for e in enemies if e["rect"].x + e["rect"].width > 0]

    for fruit in fruits:
        fruit.x -= int(game_speed)
    fruits = [f for f in fruits if f.x + f.width > 0]

    for bullet in bullets_fired:
        bullet.x += 10
    bullets_fired = [b for b in bullets_fired if b.x < WIDTH]

    # Collisions
    handle_collisions()

    # Drawing
    pygame.draw.rect(screen, DINO_COLOR, dino)

    for enemy in enemies:
        color = TREE_COLOR if enemy["type"] == "tree" else BIRD_COLOR
        pygame.draw.rect(screen, color, enemy["rect"])

    for fruit in fruits:
        pygame.draw.rect(screen, FRUIT_COLOR, fruit)

    for bullet in bullets_fired:
        pygame.draw.rect(screen, BULLET_COLOR, bullet)

    # UI
    score += 0.5
    draw_text(f"Score: {int(score)}", 20, 20)
    draw_text(f"Level: {level}", 20, 50)
    draw_text(f"Bullets: {bullets}", 20, 80)
    draw_text(f"Stamina: {stamina}", 20, 110)

    pygame.display.flip()

pygame.quit()
