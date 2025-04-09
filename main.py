import pygame
import random
import sys

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Equilibrium Run")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (200, 0, 0)
BLUE  = (0, 0, 200)
GREEN = (0, 200, 0)
GROUND_Y = 350

# Dino setup
dino = pygame.Rect(100, GROUND_Y - 50, 50, 50)
dino_color = BLACK
dino_velocity = 0
is_jumping = False
gravity = 1

# Obstacles list: each element is a tuple (rect, type)
obstacles = []
# We'll spawn an obstacle every 1500ms
SPAWN_OBSTACLE = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_OBSTACLE, 1500)

# Fireball list
fireballs = []

# Attack and Shield settings (in frames, 60 frames ~ 1 sec)
attack_cooldown = 0       # frames until next attack allowed
ATTACK_COOLDOWN_FRAMES = 90  # e.g., 1.5 sec cooldown

shield_cooldown = 0       # frames until shield can be activated again
SHIELD_COOLDOWN_FRAMES = 180  # e.g., 3 sec cooldown

shield_active = False
shield_timer = 0          # frames remaining for shield
SHIELD_DURATION_FRAMES = 60  # shield lasts 1 sec

# Score and game state
score = 0
game_active = True

# Main Game Loop
while True:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_active:
            if event.type == SPAWN_OBSTACLE:
                # Randomly choose between ground obstacle or bird
                obstacle_type = random.choice(["ground", "bird"])
                if obstacle_type == "ground":
                    height = random.choice([30, 50])
                    obs_rect = pygame.Rect(WIDTH, GROUND_Y - height, 20, height)
                else:
                    # Bird obstacle: smaller, flying in the air (around y = 200)
                    obs_rect = pygame.Rect(WIDTH, 200, 40, 30)
                obstacles.append((obs_rect, obstacle_type))
        else:
            # Reset the game if 'R' is pressed after game over.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                dino.y = GROUND_Y - 50
                obstacles.clear()
                fireballs.clear()
                dino_velocity = 0
                is_jumping = False
                score = 0
                game_active = True
                attack_cooldown = 0
                shield_cooldown = 0
                shield_active = False

    keys = pygame.key.get_pressed()
    if game_active:
        # Jump with UP arrow
        if keys[pygame.K_UP] and not is_jumping:
            dino_velocity = -18
            is_jumping = True

        # Duck with DOWN arrow (adjust dino height)
        if keys[pygame.K_DOWN]:
            dino.height = 30
        else:
            dino.height = 50

        # Attack with RIGHT arrow if not cooling down.
        if keys[pygame.K_RIGHT] and attack_cooldown <= 0:
            # Spawn a fireball at the Dino's right side, centered vertically.
            fireball = pygame.Rect(dino.right, dino.y + dino.height//2 - 5, 10, 10)
            fireballs.append(fireball)
            attack_cooldown = ATTACK_COOLDOWN_FRAMES

        # Shield with LEFT arrow if available.
        if keys[pygame.K_LEFT] and shield_cooldown <= 0 and not shield_active:
            shield_active = True
            shield_timer = SHIELD_DURATION_FRAMES
            shield_cooldown = SHIELD_COOLDOWN_FRAMES

        # Update cooldowns if active
        if attack_cooldown > 0:
            attack_cooldown -= 1
        if shield_cooldown > 0:
            shield_cooldown -= 1

        if shield_active:
            shield_timer -= 1
            if shield_timer <= 0:
                shield_active = False

        # Apply gravity to Dino
        dino_velocity += gravity
        dino.y += dino_velocity
        if dino.y >= GROUND_Y - dino.height:
            dino.y = GROUND_Y - dino.height
            dino_velocity = 0
            is_jumping = False

        # Move obstacles
        new_obstacles = []
        for obs_rect, obs_type in obstacles:
            obs_rect.x -= 6
            # Draw obstacles: red for ground obstacles, green for birds.
            if obs_type == "ground":
                pygame.draw.rect(screen, RED, obs_rect)
            else:
                pygame.draw.rect(screen, GREEN, obs_rect)
            # If obstacle is still on screen, keep it.
            if obs_rect.x > -50:
                new_obstacles.append((obs_rect, obs_type))
        obstacles = new_obstacles

        # Move fireballs and draw them (blue)
        new_fireballs = []
        for fireball in fireballs:
            fireball.x += 10  # move right faster
            pygame.draw.rect(screen, BLUE, fireball)
            if fireball.x < WIDTH:
                new_fireballs.append(fireball)
        fireballs = new_fireballs

        # Check collisions between fireballs and obstacles (only for birds)
        for fireball in fireballs[:]:
            for obs in obstacles[:]:
                obs_rect, obs_type = obs
                if fireball.colliderect(obs_rect):
                    if obs_type == "bird":
                        obstacles.remove(obs)
                        if fireball in fireballs:
                            fireballs.remove(fireball)
                    # For ground obstacles, fireball might just pass by.
                    
        # Collision check between Dino and obstacles
        for obs in obstacles[:]:
            obs_rect, obs_type = obs
            if dino.colliderect(obs_rect):
                if shield_active:
                    # Shield is active so remove the obstacle and continue
                    obstacles.remove(obs)
                else:
                    game_active = False

        # Draw Dino (with shield indicator if active)
        pygame.draw.rect(screen, dino_color, dino)
        if shield_active:
            # Draw a circle around Dino to show the shield (blue outline)
            pygame.draw.circle(screen, BLUE, dino.center, max(dino.width, dino.height), 3)

        # Score
        score += 1
        score_text = font.render(f"Score: {score // 10}", True, BLACK)
        screen.blit(score_text, (10, 10))
    else:
        # Game Over screen
        msg = font.render("Game Over! Press 'R' to Restart", True, BLACK)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))

    # Draw ground line
    pygame.draw.line(screen, BLACK, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)

    pygame.display.update()
    clock.tick(60)
