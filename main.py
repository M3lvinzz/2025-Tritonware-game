import pygame
import random
import sys

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
dino_jump_imgs = load_images("assets/jump", 6, (100, 100))  # You have 6 jump frames!
dino_shoot_imgs = load_images("assets/shoot", 4, (100, 100))


# Load and scale fruit image
food_img = pygame.image.load("assets/food.png").convert_alpha()
food_img = pygame.transform.scale(food_img, (40, 40))  # Match your fruit size




#tree image load
tree_img = pygame.image.load("assets/tree.png").convert_alpha()

tree_img = pygame.transform.scale(tree_img, (60, 80))

car1_img = pygame.transform.scale(pygame.image.load("assets/car1.png").convert_alpha(), (60, 40))
car2_img = pygame.transform.scale(pygame.image.load("assets/car2.png").convert_alpha(), (60, 40))

#mana image load

mana_img = pygame.image.load("assets/mana.png").convert_alpha()

mana_img = pygame.transform.scale(mana_img, (40, 40))

#bullet image load

bullet_img = pygame.image.load("assets/bullet.png").convert_alpha()

bullet_img = pygame.transform.scale(bullet_img, (40, 40))


#bird images load
bird_imgs = [
    pygame.transform.scale(pygame.image.load("assets/bird1.png").convert_alpha(), (70, 70)),
    pygame.transform.scale(pygame.image.load("assets/bird2.png").convert_alpha(), (70, 70)),
    pygame.transform.scale(pygame.image.load("assets/bird3.png").convert_alpha(), (70, 70)),
]

#stamina bar images load
stamina_bar_imgs = [
    pygame.transform.scale(pygame.image.load("assets/stamina1.png").convert_alpha(), (30, 30)),
    pygame.transform.scale(pygame.image.load("assets/stamina2.png").convert_alpha(), (30, 30)),
    pygame.transform.scale(pygame.image.load("assets/stamina3.png").convert_alpha(), (30, 30)),
    pygame.transform.scale(pygame.image.load("assets/stamina4.png").convert_alpha(), (30, 30)),
    pygame.transform.scale(pygame.image.load("assets/stamina5.png").convert_alpha(), (30, 30)),
    pygame.transform.scale(pygame.image.load("assets/stamina6.png").convert_alpha(), (30, 30)),
    pygame.transform.scale(pygame.image.load("assets/stamina7.png").convert_alpha(), (30, 30)),
    pygame.transform.scale(pygame.image.load("assets/stamina8.png").convert_alpha(), (30, 30)),
]

# Load background image
bg_img1 = pygame.transform.scale(pygame.image.load("assets/background1.png").convert(), (WIDTH, HEIGHT))
bg_img2 = pygame.transform.scale(pygame.image.load("assets/background2.png").convert(), (WIDTH, HEIGHT))


bg_x = 0

# Load game over screen image
game_over_img1 = pygame.transform.scale(pygame.image.load("assets/gameover1.png").convert(), (WIDTH, HEIGHT))
game_over_img2 = pygame.transform.scale(pygame.image.load("assets/gameover2.png").convert(), (WIDTH, HEIGHT))
game_over_img3 = pygame.transform.scale(pygame.image.load("assets/gameover3.png").convert(), (WIDTH, HEIGHT))
game_over_img4 = pygame.transform.scale(pygame.image.load("assets/gameover4.png").convert(), (WIDTH, HEIGHT))



bird_imgs = [pygame.transform.scale(img, (40, 40)) for img in bird_imgs]


#Playing background music
pygame.mixer.music.load("music/forestbgm.mp3")
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
dino = pygame.Rect(50, HEIGHT - 100, 40, 60) 
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
last_damage_time = 0
damage_cooldown = 1000
first_time_no = True


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
        rect = pygame.Rect(WIDTH, HEIGHT - 70, 60, 40)  # Car height = 40
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

    pygame.draw.rect(screen, WHITE, (950, 20, progress_width, 20), 2)  # Outline
    pygame.draw.rect(screen, (0, 200, 0), (950, 20, fill_width, 20))   # Fill bar

def handle_collisions():
    global stamina, last_damage_time
    now = pygame.time.get_ticks()
    for enemy in enemies:
        if dino.colliderect(enemy["rect"]):
            if now - last_damage_time > damage_cooldown:
                stamina -= 20
                last_damage_time = now
            if stamina <= 0:
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
    global bullets, stamina, level, start_time, spawn_timer, bullet_cooldown, bullet_cooldown_time, last_damage_time
    bullets = 3
    stamina = 100
    level = 1
    start_time = pygame.time.get_ticks()
    spawn_timer = 0
    bullet_cooldown = False
    bullet_cooldown_time = 0
    last_damage_time = 0

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


portraits = load_images('assets/portrait', count = 6, scale = (60, 60))




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
    current_bg = bg_img1 if level != 2 else bg_img2
    screen.blit(current_bg, (bg_x, 0))
    screen.blit(current_bg, (bg_x + WIDTH, 0))



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
        shooting_timer = 30  # show shoot animation for a few frames


    if bullet_cooldown and pygame.time.get_ticks() - bullet_cooldown_time > 300:
        bullet_cooldown = False

    if is_shooting:
        shooting_timer -= 1
        if shooting_timer <= 0:
            is_shooting = False





    if is_jumping:
        dino_velocity_y += gravity
        dino.y += dino_velocity_y
        if dino.y >= HEIGHT - 90:
            dino.y = HEIGHT - 90
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
        elif enemy["type"] == "bird":
            screen.blit(bird_imgs[bird_frame_index], enemy["rect"])
        elif enemy["type"] == "car1":
            screen.blit(car1_img, enemy["rect"])
        elif enemy["type"] == "car2":
            screen.blit(car2_img, enemy["rect"])

    # DRAW TIMER HERE
    draw_level_timer(elapsed, level)

    # Draw fruits and bullets
    for food in foods:
        screen.blit(food_img, food)

    for bullet in bullets_fired:
        screen.blit(bullet_img, bullet)

    # Draw UI
    draw_text(f"Level: {level}", 20, 20)

    # Code for stamina bar
    bar_x, bar_y = 20, 50
    bar_width, bar_height = 100, 20
    bar_fill = int((stamina / 100) * bar_width)

    pygame.draw.rect(screen, (255,0,0), (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(screen, (0,255,0), (bar_x, bar_y, bar_fill, bar_height))

    stamina_index = int((stamina / 100) * (len(stamina_bar_imgs) - 1))
    stamina_index = 7 - min(7, stamina // 13)

    stamina_img = stamina_bar_imgs[stamina_index]

    screen.blit(stamina_img, (bar_x + bar_width + 10, bar_y - 10))

    # Mana bullets display
    for i in range(bullets):
        screen.blit(mana_img, (bar_x + bar_width + 50 + i * 35, bar_y - 10))

    pygame.display.flip()

