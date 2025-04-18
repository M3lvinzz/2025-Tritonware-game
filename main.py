import pygame
import random
import sys
#addboss
import math

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 1200, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Dash")


class Cutscene:
    def __init__(self, screen, background, events=None):
        self.screen = screen
        self.background = background
        self.font = pygame.font.SysFont("Arial", 24)
        self.events = events or []
        self.clock = pygame.time.Clock()
        self.finished = False
        self.current_event_index = 0

        self.white_opacity = 120
        self.white_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.white_surface.fill((255, 255, 255, self.white_opacity))

    def play(self):
        running = True
        print("🟡 Cutscene started...")  # checkpoint

        pygame.mixer.music.load("music/cutscene_bgm.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("🔴 Quit event detected in cutscene")
                    running = False
                    return  # Don't use sys.exit() here!

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.current_event_index += 1
                        if self.current_event_index >= len(self.events):
                            print("🟢 Cutscene ended")
                            pygame.mixer.music.fadeout(1000)
                            running = False
                            return  # Safely exit
                    elif event.key == pygame.K_ESCAPE:  # Skip cutscene
                        print("⏩ Cutscene skipped")
                        pygame.mixer.music.fadeout(1000)
                        running = False
                        return  # Exit immediately

            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.white_surface, (0, 0))

            if self.current_event_index < len(self.events):
                current = self.events[self.current_event_index]

                if "portrait" in current and current["portrait"]:
                    self.screen.blit(current["portrait"], (50, 10))

                if current.get("text"):
                    text_surface = self.font.render(current["text"], True, (0, 0, 0))
                    text_rect = text_surface.get_rect(topright=(self.screen.get_width() - 250, 200))  # top-right padding
                    self.screen.blit(text_surface, text_rect)

            prompt = self.font.render("Press SPACE to continue or ESC to skip", True, (0, 0, 0))
            self.screen.blit(prompt, (self.screen.get_width() - 400, self.screen.get_height() - 50))

            pygame.display.update()
            self.clock.tick(60)


def tutorial(screen, bg, portraits):
    print("🟢 Running tutorial function")
    cutscene_events = [
        {"text": "Hey, My name is Dante the Dinosaur!", "pos": (100, 400), 'portrait': portraits[0]},
        {"text": "I am part Pentaceratops, Pterodactylus, and T-Rex!", "pos": (100, 400), 'portrait': portraits[1]},
        {"text": "Humans sure have changed nature since our time.", "pos": (100, 400), 'portrait': portraits[2]},
        {"text": "I'm not sure where home is anymore. Can you help me find it?", "pos": (100, 400), 'portrait': portraits[3]},
        {"text": "While I’m running, press [Arrow UP] to Jump!", "pos": (100, 400), 'portrait': portraits[4]},
        {"text": "Keep an eye on my stamina bar!", "pos": (100, 400), 'portrait': portraits[5]},
        {"text": "Pick up meat to refill stamina.", "pos": (100, 400), 'portrait': portraits[0]},
        {"text": "I can use 3 fireballs to destroy obstacles!", "pos": (100, 400), 'portrait': portraits[1]},
        {"text": "Press [Right Arrow] to shoot. Be careful—only 3 shots!", "pos": (100, 400), 'portrait': portraits[2]},
    ]

    cutscene = Cutscene(screen, bg, cutscene_events)
    cutscene.play()
    print("✅ Cutscene finished!") 

def run_game():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    big_font = pygame.font.SysFont("Arial", 80, bold=True)

    running = True
    while running:
        dt = clock.tick(60)
        # all your current game loop code here...


        
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
        
        boss_intro_active = False
        boss_intro_timer = 0
        

        dino_run_imgs = load_images("assets/run", 6, (100, 100))
        dino_jump_imgs = load_images("assets/jump", 6, (100, 100))  # You have 6 jump frames!
        dino_shoot_imgs = load_images("assets/shoot", 4, (100, 100))


        # Load and scale fruit image
        food_img = pygame.image.load("assets/food.png").convert_alpha()
        food_img = pygame.transform.scale(food_img, (40, 40))  # Match your fruit size

        #load bullet image
        bullet_img = pygame.image.load("assets/bullet.png").convert_alpha()
        bullet_img = pygame.transform.scale(bullet_img, (40, 40))  # adjust size as needed


        #tree image load
        tree_img = pygame.image.load("assets/tree.png").convert_alpha()

        tree_img = pygame.transform.scale(tree_img, (60, 80))

        car1_img = pygame.transform.scale(pygame.image.load("assets/car1.png").convert_alpha(), (100, 80))
        car2_img = pygame.transform.scale(pygame.image.load("assets/car2.png").convert_alpha(), (100, 80))

        #mana image load

        mana_img = pygame.image.load("assets/mana.png").convert_alpha()

        mana_img = pygame.transform.scale(mana_img, (40, 40))


        #bird images load
        bird_imgs = [
            pygame.transform.scale(pygame.image.load("assets/bird1.png").convert_alpha(), (80, 80)),
            pygame.transform.scale(pygame.image.load("assets/bird2.png").convert_alpha(), (80, 80)),
            pygame.transform.scale(pygame.image.load("assets/bird3.png").convert_alpha(), (80, 80)),
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




        bird_imgs = [pygame.transform.scale(img, (40, 40)) for img in bird_imgs]


        #Playing background music
        pygame.mixer.music.load("music/forestbgm.mp3")
        pygame.mixer.music.set_volume(0.5)  # set volume to 50%
        pygame.mixer.music.play(-1)  

        jump_sound = pygame.mixer.Sound("music/jumpsound2.mp3")
        hurt_sound = pygame.mixer.Sound("music/hurtsound.mp3")
        shoot_sound = pygame.mixer.Sound("music/shoot.mp3")

        jump_sound.set_volume(0.4)
        hurt_sound.set_volume(0.6)
        shoot_sound.set_volume(0.5)


        # Colors
        WHITE = (255, 255, 255)
        DINO_COLOR = (0, 200, 0)
        TREE_COLOR = (139, 69, 19)
        BIRD_COLOR = (50, 100, 255)
        F_COLOR = (255, 100, 0)
        BULLET_COLOR = (255, 255, 0)
        BG_COLOR = (180, 240, 255)
        #addboss
        RED = (255, 50, 50)



        # Dino setup
        dino = pygame.Rect(50, HEIGHT - 100, 40, 60) 
        gravity = 1.2
        jump_velocity = -20
        dino_velocity_y = 0
        is_jumping = False

       


        #boss add
        boss = pygame.Rect(900, 100, 100, 100)
        boss_target = pygame.Vector2(boss.x, boss.y)
        boss_active = False
        boss_health = 3
        boss_bullets = []
        boss_attack_type = "bullet_fan"
        boss_attack_timer = 0
        next_attack_time = 3000
        spiral_angle = 0
        boss_move_timer = 0
        last_fan_fire = 0


        boss_entry_timer = 0
        boss_appearing = False
        boss_y_offset = -100  

        boss_target_x = WIDTH - 250
        boss_target_y = 60









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
                bird_y = random.choice([HEIGHT - 160, HEIGHT - 140])
                rect = pygame.Rect(WIDTH, bird_y + 10, 40, 25)
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
            nonlocal stamina, last_damage_time
            now = pygame.time.get_ticks()
            for enemy in enemies:
                if dino.colliderect(enemy["rect"]):
                    if now - last_damage_time > damage_cooldown:
                        stamina -= 20
                        last_damage_time = now
                        hurt_sound.play()
                    
                    if stamina <= 0:
                        game_over()

            for food in foods[:]:
                if dino.colliderect(food):
                    stamina = min(100, stamina + 20)
                    foods.remove(food)

            for bullet in bullets_fired[:]:
                for enemy in enemies[:]:
                    if bullet["rect"].colliderect(enemy["rect"]):
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
            nonlocal bullets, stamina
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

        def pause_game():
            paused = True
            font = pygame.font.SysFont("Arial", 50)
            pause_text = font.render("Game Paused. Press P to Resume.", True, (255, 255, 255))
            text_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

            while paused:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        paused = False

                screen.fill((0, 0, 0))  # Optional: Dim the screen
                screen.blit(pause_text, text_rect)
                pygame.display.flip()
                pygame.time.Clock().tick(30)  # Limit pause screen FPS



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

        # === Add white gradient overlay ===
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for y in range(HEIGHT):
            alpha = int(140 * ((y / HEIGHT) ** 2))  # 下越大，上越小
            pygame.draw.line(overlay, (255, 255, 255, alpha), (0, y), (WIDTH, y))
        screen.blit(overlay, (0, 0))



        # Animate birds
        bird_frame_timer += 1
        if bird_frame_timer > 5:
            bird_frame_index = (bird_frame_index + 1) % len(bird_imgs)
            bird_frame_timer = 0

        # Level progression
        current_level = min(3, elapsed // LEVEL_DURATION + 1)
        if current_level != level:
            level = current_level
            
                # === Switch Background Music by Level ===
            if level == 2:
                pygame.mixer.music.load("music/level2_bgm.mp3")
                pygame.mixer.music.play(-1)
            elif level == 3:
                pygame.mixer.music.load("music/level3_bgm.mp3")
                pygame.mixer.music.play(-1)

            
            
            
            
            
            
            if level <= 3:
                level_up()
        #bossadd
            if level == 3:
                boss_appearing = True
                boss_active = False
                boss_entry_timer = pygame.time.get_ticks()
                boss.x = WIDTH + 100  # 右侧外部
                boss.y = -100         # 屏幕上方外部
# 暂不激活
                
                boss_intro_active = True
                boss_intro_timer = pygame.time.get_ticks()
                #pygame.mixer.Sound("sounds/boss_warning.wav").play()


        
        #bossadd
            if level > 3:
                boss_active = False  # stop boss if still alive
                win_game()

        

        if pygame.time.get_ticks() % 1000 < 20:
            stamina -= 1
            if stamina <= 0:
                game_over()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pause_game()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and not is_jumping:
            dino_velocity_y = jump_velocity
            is_jumping = True
            jump_sound.play()


        if keys[pygame.K_RIGHT] and bullets > 0 and not bullet_cooldown:
            bullet = {
                "rect": pygame.Rect(dino.right, dino.centery - 5, 20, 20),
                "x": dino.right,
                "y": dino.centery - 5
            }
            bullets_fired.append(bullet)
            bullets -= 1
            bullet_cooldown = True
            bullet_cooldown_time = pygame.time.get_ticks()
            shoot_sound.play()
        
        
        
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
            bullet["x"] += 10
            bullet["rect"].x = bullet["x"]

        bullets_fired = [b for b in bullets_fired if b["x"] < WIDTH]


        handle_collisions()





        # === Boss延迟登场（飞入）动画 ===
        if level == 3 and boss_appearing:
            time_since_entry = pygame.time.get_ticks() - boss_entry_timer

# boss缓缓滑入
            target_x = WIDTH - 300
            if boss.x > target_x:
                boss.x -= 4  # 控制飞入速度（越小越慢）

# 5 秒后启用 Boss 攻击
            if time_since_entry >= 5000 and boss.x <= target_x:
                boss_active = True
                boss_appearing = False
                boss_move_timer = pygame.time.get_ticks()
                boss_attack_timer = pygame.time.get_ticks()
                boss.x += (target_x - boss.x) * 0.1  # 越来越慢地接近


# 控制飞入速度
        if boss_appearing:
            boss.x += (boss_target_x - boss.x) * 0.05
            boss.y += (boss_target_y - boss.y) * 0.05

            if abs(boss.x - boss_target_x) < 2 and abs(boss.y - boss_target_y) < 2:
                boss.x = boss_target_x
                boss.y = boss_target_y
                boss_appearing = False
                boss_active = True
                boss_move_timer = pygame.time.get_ticks()




    #addboss
            # === Boss Logic for Level 3 ===
        if boss_active:
            now = pygame.time.get_ticks()

            # Move boss target every few seconds
            if now - boss_move_timer > 2000:
                boss_target = pygame.Vector2(
                    random.randint(600, WIDTH - 100),
                    random.randint(20, HEIGHT // 2)
                )
                boss_move_timer = now

            # Smooth boss movement
            direction = boss_target - pygame.Vector2(boss.x, boss.y)
            if direction.length() > 1:
                direction = direction.normalize() * 2
                boss.x += int(direction.x)
                boss.y += int(direction.y)

            # Switch attack
            if now - boss_attack_timer > next_attack_time:
                boss_attack_type = random.choice(["bullet_fan", "spiral"])
                boss_attack_timer = now

            # Bullet fan (shoots left)
            if boss_attack_type == "bullet_fan" and now % 1500 < 20:
                base_angle = math.pi
                for i in range(-3, 4):
                    angle = base_angle + i * 0.2
                    boss_bullets.append({
                        "x": boss.centerx,
                        "y": boss.centery,
                        "vx": 8 * math.cos(angle),
                        "vy": 8 * math.sin(angle)
                    })

        # Spiral bullet
            if boss_attack_type == "spiral" and now - boss_attack_timer > 200 and now % 100 < 10:
                last_fan_fire = now
                spiral_angle -= 0.2
                boss_bullets.append({
                    "x": boss.centerx,
                    "y": boss.centery,
                    "vx": 7 * math.cos(spiral_angle),
                    "vy": 7 * math.sin(spiral_angle)
                })

        # Move boss bullets
            for b in boss_bullets:
                b["x"] += b["vx"]
                b["y"] += b["vy"]
            boss_bullets = [b for b in boss_bullets if 0 <= b["x"] <= WIDTH and 0 <= b["y"] <= HEIGHT]

        # Check collision: Boss bullets → player
            for b in boss_bullets:
                if dino.colliderect(pygame.Rect(b["x"], b["y"], 10, 10)):
                    if now - last_damage_time > damage_cooldown:
                        stamina -= 20
                        last_damage_time = now
                        hurt_sound.play()
                    if stamina <= 0:
                        game_over()
                        
        
        
        # Check collision: Your bullets → boss
            for bullet in bullets_fired[:]:
                if boss.colliderect(bullet["rect"]):
                    bullets_fired.remove(bullet)
                    boss_health -= 1
                    if boss_health <= 0:
                        boss_active = False
                        print("Boss defeated!")











        # Draw Dino
        if dino_state == "run":
            screen.blit(dino_run_imgs[dino_frame_index], dino)
        elif dino_state == "jump":
            screen.blit(dino_jump_imgs[dino_frame_index], dino)
        elif dino_state == "shoot":
            screen.blit(dino_shoot_imgs[dino_frame_index], dino

            pygame.draw.rect(screen, (255, 0, 0), dino, 2)

        # addboss
        if boss_active:
            pygame.draw.rect(screen, RED, boss)
            pygame.draw.rect(screen, WHITE, (450, 20, 200, 20), 2)
            pygame.draw.rect(screen, RED, (450, 20, boss_health * 66, 20))
            hint = "!!!" if boss_attack_type == "bullet_fan" else "@@"
            draw_text(hint, boss.centerx - 10, boss.y - 30)






        # Draw Boss Bullets
        for b in boss_bullets:
            pygame.draw.circle(screen, RED, (int(b["x"]), int(b["y"])), 5)













        # Draw enemies
        for enemy in enemies:
            if enemy["type"] == "tree":
                screen.blit(tree_img, (enemy["rect"].x - 10, enemy["rect"].y))  
            elif enemy["type"] == "bird":
                screen.blit(bird_imgs[bird_frame_index], (enemy["rect"].x, enemy["rect"].y - 10))
            elif enemy["type"] == "car1":
                screen.blit(car1_img, (enemy["rect"].x-10, enemy["rect"].y - 20))  
            elif enemy["type"] == "car2":
                screen.blit(car2_img, (enemy["rect"].x-10, enemy["rect"].y - 20))

                # 🛠 DEBUG: Draw enemy hitboxes
            pygame.draw.rect(screen, (255, 0, 0), enemy["rect"], 2)

        # DRAW TIMER HERE
        draw_level_timer(elapsed, level)

        # Draw fruits and bullets
        for food in foods:
            screen.blit(food_img, food)

        for bullet in bullets_fired:
            screen.blit(bullet_img, (bullet["x"], bullet["y"]))

        if boss_intro_active:
            time_since_intro = pygame.time.get_ticks() - boss_intro_timer
            if time_since_intro < 3000:  # 播放 3 秒
                if (time_since_intro // 500) % 2 == 0:  # 每 0.5 秒闪一下
                    warning_text = big_font.render("WARNING!", True, (255, 0, 0))
                    text_rect = warning_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                    screen.blit(warning_text, text_rect)
            else:
                boss_intro_active = False






        # Draw UI
        draw_text(f"Level: {level}", 20, 20)

        # Code for stamina bar
        bar_x, bar_y = 20, 50
        bar_width, bar_height = 100, 20
        bar_fill = int((stamina / 100) * bar_width)

        pygame.draw.rect(screen, (255,255,255), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (255,0,0), (bar_x, bar_y, bar_fill, bar_height))

        stamina_index = int((stamina / 100) * (len(stamina_bar_imgs) - 1))
        stamina_index = 7 - min(7, stamina // 13)

        stamina_img = stamina_bar_imgs[stamina_index]

        screen.blit(stamina_img, (bar_x + bar_width + 10, bar_y - 10))

        # Mana bullets display
        for i in range(bullets):
            screen.blit(mana_img, (bar_x + bar_width + 50 + i * 35, bar_y - 10))

        pygame.display.flip()



def load_images(prefix, count, scale):
    return [
        pygame.transform.scale(pygame.image.load(f"{prefix}{i}.png").convert_alpha(), scale)
        for i in range(1, count + 1)
    ]
          

print("Loading background...")
# Load background for tutorial and portraits
bg_image = pygame.image.load("assets/bg/cutscene_bg.png").convert()
print("Loading portraits...")
portraits = load_images('assets/portrait', count=6, scale=(400,400))


print("Calling tutorial...")

# Show tutorial first
tutorial(screen, bg_image, portraits)


print("Tutorial finished, starting game...")
# Then start the actual game

run_game()
