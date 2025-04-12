



import pygame
import random
import sys

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 1200, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Sprint: Elemental Run")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)




def load_images(prefix, count, scale):
    return [
        pygame.transform.scale(pygame.image.load(f"{prefix}{i}.png").convert_alpha(), scale)
        for i in range(1, count + 1)
    ]


dino_run_imgs = load_images("run", 6, (60, 60))
dino_jump_imgs = load_images("jump", 6, (60, 60))  # You have 6 jump frames!
dino_shoot_imgs = load_images("shoot", 4, (60, 60))


# Load and scale fruit image
food_img = pygame.image.load("food.png").convert_alpha()
food_img = pygame.transform.scale(food_img, (25, 25))  # Match your fruit size




#tree image load
tree_img = pygame.image.load("tree.png").convert_alpha()

tree_img = pygame.transform.scale(tree_img, (30, 40))  # Match the tree size


tree_img = pygame.transform.scale(tree_img, (40, 60))


#bird images load
bird_imgs = [
    pygame.transform.scale(pygame.image.load("bird1.png").convert_alpha(), (30, 30)),
    pygame.transform.scale(pygame.image.load("bird2.png").convert_alpha(), (30, 30)),
    pygame.transform.scale(pygame.image.load("bird3.png").convert_alpha(), (30, 30)),
]


# Load background image
bg_img = pygame.image.load("background.png").convert()
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))


bg_x = 0




bird_imgs = [pygame.transform.scale(img, (40, 40)) for img in bird_imgs]


#Playing background music
pygame.mixer.music.load("forestbgm.mp3")
pygame.mixer.music.set_volume(0.5)  # set volume to 50%
pygame.mixer.music.play(-1)  

# Colors
WHITE = (255, 255, 255)
DINO_COLOR = (0, 200, 0)
TREE_COLOR = (139, 69, 19)
BIRD_COLOR = (50, 100, 255)
F_COLOR = (255, 100, 0)
BULLET_COLOR = (255, 255, 0)
BG_COLOR = (180, 240, 255)

# Dino setup
dino = pygame.Rect(50, HEIGHT - 80, 40, 60) 
gravity = 1.2
jump_velocity = -20
dino_velocity_y = 0
is_jumping = False

# Game state
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


def draw_text(text, x, y):
    label = font.render(text, True, WHITE)
    screen.blit(label, (x, y))


def spawn_obstacle():
    kind = random.choice(["tree", "bird"])
    if kind == "tree":
        rect = pygame.Rect(WIDTH, HEIGHT - 80, 40, 60)
    else:
        bird_y = random.choice([HEIGHT - 160, HEIGHT - 120])
        rect = pygame.Rect(WIDTH, bird_y, 40, 40)
    enemies.append({"rect": rect, "type": kind})


def spawn_foods():
    food_rect = pygame.Rect(WIDTH, random.randint(HEIGHT - 120, HEIGHT - 60), 25, 25)
    foods.append(food_rect)



def handle_collisions():
    global stamina
    for enemy in enemies:
        if dino.colliderect(enemy["rect"]):
            game_over()

    for food in foods[:]:
        if dino.colliderect(food):
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


dino_state = "run"  
dino_frame_index = 0
dino_frame_timer = 0



is_shooting = False
shooting_timer = 0






running = True
while running:
    dt = clock.tick(60)
   
    prev_dino_state = dino_state  # Save the previous state for comparison

   
   
    elapsed = pygame.time.get_ticks() - start_time
    screen.fill(BG_COLOR)

    game_speed = 5 + level + (elapsed / 15000)
# Move and draw scrolling background
    bg_x -= int(game_speed * 0.5)  # Adjust speed for parallax effect
    if bg_x <= -WIDTH:
        bg_x = 0

# Draw background images side-by-side for looping
    screen.blit(bg_img, (bg_x, 0))
    screen.blit(bg_img, (bg_x + WIDTH, 0))



    # Animate birds
    bird_frame_timer += 1
    if bird_frame_timer > 5:
        bird_frame_index = (bird_frame_index + 1) % len(bird_imgs)
        bird_frame_timer = 0

    # Level progression
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

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and not is_jumping:
        dino_velocity_y = jump_velocity
        is_jumping = True

    if keys[pygame.K_RIGHT] and bullets > 0 and not bullet_cooldown:
        bullet = pygame.Rect(dino.right, dino.centery - 5, 15, 10)
        bullets_fired.append(bullet)
        bullets -= 1
        bullet_cooldown = True
        bullet_cooldown_time = pygame.time.get_ticks()
    
    # Set shooting state
        is_shooting = True
        shooting_timer = 10  # show shoot animation for a few frames


    if bullet_cooldown and pygame.time.get_ticks() - bullet_cooldown_time > 300:
        bullet_cooldown = False

    if is_shooting:
        shooting_timer -= 1
        if shooting_timer <= 0:
            is_shooting = False





    if is_jumping:
        dino_velocity_y += gravity
        dino.y += dino_velocity_y
        if dino.y >= HEIGHT - 80:
            dino.y = HEIGHT - 80
            is_jumping = False
            dino_velocity_y = 0

    if is_jumping:
        dino_state = "jump"
    elif is_shooting:
        dino_state = "shoot"
    else:
        dino_state = "run"


# Reset animation index if state changed
    if dino_state != prev_dino_state:
        dino_frame_index = 0
        dino_frame_timer = 0




    # Update animation frame
    dino_frame_timer += 1
    if dino_frame_timer > 6:
        dino_frame_timer = 0
        dino_frame_index += 1

        if dino_state == "run":
            dino_frame_index %= len(dino_run_imgs)
        elif dino_state == "jump":
            dino_frame_index %= len(dino_jump_imgs)
        elif dino_state == "shoot":
            dino_frame_index %= len(dino_shoot_imgs)

    # Spawn enemies/fruits
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

    # Draw Dino
    if dino_state == "run":
        screen.blit(dino_run_imgs[dino_frame_index], dino)
    elif dino_state == "jump":
        screen.blit(dino_jump_imgs[dino_frame_index], dino)
    elif dino_state == "shoot":
        screen.blit(dino_shoot_imgs[dino_frame_index], dino)

    # Draw enemies
    for enemy in enemies:
        if enemy["type"] == "tree":
            screen.blit(tree_img, enemy["rect"])
        else:
            screen.blit(bird_imgs[bird_frame_index], enemy["rect"])

    # Draw fruits and bullets
    for food in foods:
        screen.blit(food_img, food)

    for bullet in bullets_fired:
        pygame.draw.rect(screen, BULLET_COLOR, bullet)

    # Draw UI
    draw_text(f"Level: {level}", 20, 20)
    draw_text(f"Bullets: {bullets}", 20, 50)
    draw_text(f"Stamina: {stamina}", 20, 80)

    pygame.display.flip()

