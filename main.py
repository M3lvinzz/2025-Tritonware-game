import pygame
import random
import sys
#addboss
import math

# Initialize Pygame
pygame.init()
SCALE = 1.5
VIRTUAL_WIDTH, VIRTUAL_HEIGHT = 1200, 500
WIDTH, HEIGHT = int(VIRTUAL_WIDTH * SCALE), int(VIRTUAL_HEIGHT * SCALE)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
virtual_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
pygame.display.set_caption("Dino Dash")


first_time_no = True





class Cutscene:
    def __init__(self, background, events=None):
        self.background = background
        self.font = pygame.font.SysFont("Arial", 24)
        self.events = events or []
        self.clock = pygame.time.Clock()
        self.finished = False
        self.current_event_index = 0
        self.white_opacity = 120
        self.white_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
        self.white_surface.fill((255, 255, 255, self.white_opacity))


    def play(self):
        running = True
        print("🟡 Cutscene started...")  # checkpoint

        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("🔴 Quit event detected in cutscene")
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    pause_game()
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

            virtual_surface.blit(self.background, (0, 0))
            virtual_surface.blit(self.white_surface, (0, 0))
            if self.current_event_index < len(self.events):
                current = self.events[self.current_event_index]

                if "portrait" in current and current["portrait"]:
                    virtual_surface.blit(current["portrait"], (50, 10))

                if current.get("text"):
                    text_surface = self.font.render(current["text"], True, (0, 0, 0))
                    text_rect = text_surface.get_rect(topright=(VIRTUAL_WIDTH - 250, 200))
                    virtual_surface.blit(text_surface, text_rect)

            prompt = self.font.render("Press SPACE to continue or ESC to skip", True, (0, 0, 0))
            virtual_surface.blit(prompt, (VIRTUAL_WIDTH - 400, VIRTUAL_HEIGHT - 50))

            pygame.display.update()
            self.clock.tick(60)

            press_space_font = pygame.font.SysFont("Arial", 24, bold=True)
            press_space_text = press_space_font.render("Press SPACE", True, (255, 255, 255))
            virtual_surface.blit(press_space_text, (80, VIRTUAL_HEIGHT - 70))

            scaled_surface = pygame.transform.scale(virtual_surface, (WIDTH, HEIGHT))
            screen.blit(scaled_surface, (0, 0))
            pygame.display.flip()



def show_start_screen():
    pygame.mixer.music.load("music/cutscene_bgm.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    
    
    
    
    start_bg = pygame.image.load("assets/cover.png").convert()
    start_bg = pygame.transform.scale(start_bg, (VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
    start_font = pygame.font.SysFont("Arial", 24, bold=True)

    waiting = True
    while waiting:
        virtual_surface.blit(start_bg, (0, 0))
        press_text = start_font.render("Press [SPACE] to Start", True, (255, 255, 255))
        virtual_surface.blit(press_text, (180, VIRTUAL_HEIGHT - 80)) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

       
       
        # --- FINAL RENDERING STEP ---
        scaled_surface = pygame.transform.scale(virtual_surface, (WIDTH, HEIGHT))
        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()















def tutorial(screen, bg, portraits):
    print("🟢 Running tutorial function")
    cutscene_events = [
    {"text": "Hey, I'm Dante the Dinosaur!", "pos": (100, 400), 'portrait': portraits[1]},      # happy
    {"text": "I'm part Pentaceratops, Pterodactylus, and T-Rex!", "pos": (100, 400), 'portrait': portraits[4]},  # happy
    {"text": "Nature looks... different now.", "pos": (100, 400), 'portrait': portraits[0]},    # neutral
    {"text": "A giant factory is polluting the land.", "pos": (100, 400), 'portrait': portraits[5]},  # neutral
    {"text": "Rumor is... something—or someone—runs it.", "pos": (100, 400), 'portrait': portraits[2]},  # scared
    {"text": "Can you help me reach it and stop the damage?", "pos": (100, 400), 'portrait': portraits[1]},  # happy

    {"text": "Press [↑] to jump and avoid obstacles.", "pos": (100, 400), 'portrait': portraits[4]},  # happy
    {"text": "Watch my stamina bar!", "pos": (100, 400), 'portrait': portraits[0]},  # neutral
    {"text": "Pick up meat to stay energized.", "pos": (100, 400), 'portrait': portraits[1]},  # happy
    {"text": "Press [→] to shoot magic balls—only 5!", "pos": (100, 400), 'portrait': portraits[5]},  # scared
    {"text": "Press [P] if you ever need to pause.", "pos": (100, 400), 'portrait': portraits[3]},  # neutral
]


    cutscene = Cutscene(bg, cutscene_events)
    cutscene.play()
    print("✅ Cutscene finished!") 


    if not cutscene.finished:
        print("🟡 Cutscene was skipped early but continuing.")




def initialize_game_state():
    return {
        "bullets": 5,
        "stamina": 100,
        "enemies": [],
        "foods": [],
        "bullets_fired": [],
        "level": 1,
        "start_time": pygame.time.get_ticks(),
        "spawn_timer": 0,
        "bullet_cooldown": False,
        "bullet_cooldown_time": 0,
        "last_damage_time": 0,
        "damage_cooldown": 1000,
        "last_stamina_drain": 0,
        "dino_y": VIRTUAL_HEIGHT - 90,
        "dino_velocity_y": 0,
        "is_jumping": False,
        "boss_intro_active": False,
        "boss_intro_timer": 0,
        "LEVEL_DURATION": 30000
    }




def run_game():
    while True:
        result = actual_game_logic()
        if result == "restart":
            continue
        return result  # "menu" 或 "exit"


def actual_game_logic():
    global first_time_no
    #first_time_no = True
    
    # ✅ 初始化所有状态
    state = initialize_game_state()
    LEVEL_DURATIONS = {1: 30000, 2: 60000, 3: 90000}

    # ✅ 解包变量
    bullets = state["bullets"]
    stamina = state["stamina"]
    enemies = state["enemies"]
    foods = state["foods"]
    bullets_fired = state["bullets_fired"]
    level = state["level"]
    start_time = state["start_time"]
    spawn_timer = state["spawn_timer"]
    bullet_cooldown = state["bullet_cooldown"]
    bullet_cooldown_time = state["bullet_cooldown_time"]
    last_damage_time = state["last_damage_time"]
    damage_cooldown = state["damage_cooldown"]
    last_stamina_drain = state["last_stamina_drain"]
    dino_velocity_y = state["dino_velocity_y"]
    is_jumping = state["is_jumping"]
    boss_intro_active = state["boss_intro_active"]
    boss_intro_timer = state["boss_intro_timer"]

    dino = pygame.Rect(50, state["dino_y"], 40, 60)

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    big_font = pygame.font.SysFont("Arial", 80, bold=True)

    running = True
    while running:
        dt = clock.tick(60)
        # 🦖 游戏主循环开始

       

        dino_run_imgs = load_images("assets/run", 6, (100, 100))
        dino_jump_imgs = load_images("assets/jump", 6, (100, 100))
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

        
        barrel_img = pygame.image.load("assets/barrel.png").convert_alpha()
        barrel_img = pygame.transform.scale(barrel_img, (60, 80))


        boss_imgs = load_images("assets/boss", 5, scale=(120, 120))  # if you want animation


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
        bg_img1 = pygame.transform.scale(pygame.image.load("assets/background1.png").convert(), (VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
        bg_img2 = pygame.transform.scale(pygame.image.load("assets/background2.png").convert(), (VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
        bg_img3 = pygame.transform.scale(pygame.image.load("assets/background3.png").convert(), (VIRTUAL_WIDTH, VIRTUAL_HEIGHT))


        bg_x = 0

        game_over_img1 = pygame.transform.scale(pygame.image.load("assets/gameover1.png"), (VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
        game_over_img2 = pygame.transform.scale(pygame.image.load("assets/gameover2.png"), (VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
        game_over_img3 = pygame.transform.scale(pygame.image.load("assets/gameover3.png"), (VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
        game_over_img4 = pygame.transform.scale(pygame.image.load("assets/gameover4.png"), (VIRTUAL_WIDTH, VIRTUAL_HEIGHT))



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
        BG_COLOR = (25, 25, 45) 
        #addboss
        RED = (255, 50, 50)
        GROUND_Y = VIRTUAL_HEIGHT - 75  # 👈 你可以微调这个值，比如 -78 或 -72 来控制 Dino 靠地板更近或更远



        # Dino setup
        dino = pygame.Rect(50, GROUND_Y, 40, 60)
    
        gravity = 1.2
        jump_velocity = -20
        dino_velocity_y = 0
        is_jumping = False

       


        #boss add
        boss = pygame.Rect(VIRTUAL_WIDTH + 100, -100, 100, 100)
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

        boss_target_x = VIRTUAL_WIDTH - 250
        boss_target_y = 100









        def draw_text(text, x, y, color=(0, 0, 0)):
            font = pygame.font.SysFont("Arial", 36, bold=True)
            surface = font.render(text, True, color)
            virtual_surface.blit(surface, (x, y))





        def spawn_obstacle():
            if level == 1:
                kind = random.choice(["tree", "bird"])
            elif level == 2:
                kind = random.choice(["tree", "bird", "car1", "car2"])
            elif level == 3:
                kind = random.choice(["barrel", "bird"])  # 🔥 Level 3 uses barrel + bird

            if kind == "tree" :
                rect = pygame.Rect(VIRTUAL_WIDTH, VIRTUAL_HEIGHT - 80, 40, 60)
            if kind == "barrel":
                rect = pygame.Rect(VIRTUAL_WIDTH, VIRTUAL_HEIGHT - 80, 40, 60)
                
            
            elif kind == "bird":
                bird_y = random.choice([VIRTUAL_HEIGHT  - 160, VIRTUAL_HEIGHT  - 140])
                rect = pygame.Rect(VIRTUAL_WIDTH, bird_y + 10, 40, 25)
            elif kind == "car1" or kind == "car2":
                rect = pygame.Rect(VIRTUAL_WIDTH, VIRTUAL_HEIGHT - 70, 60, 40)

            enemies.append({"rect": rect, "type": kind})

        
        
        def spawn_foods():
            food_rect = pygame.Rect(VIRTUAL_WIDTH, random.randint(VIRTUAL_HEIGHT - 120, VIRTUAL_HEIGHT - 60), 25, 25)
            foods.append(food_rect)

        def draw_level_timer(elapsed, level, LEVEL_DURATIONS):
            cumulative = 0
            for i in range(1, 4):
                cumulative += LEVEL_DURATIONS[i]
                if elapsed < cumulative:
                    current_level = i
                    break
            else:
                current_level = 3

            level_start_time = sum(LEVEL_DURATIONS[i] for i in range(1, current_level))
            level_elapsed = elapsed - level_start_time
            level_total = LEVEL_DURATIONS[current_level]

            progress_width = 200
            fill_width = int(progress_width * (level_elapsed / level_total))

            pygame.draw.rect(virtual_surface, (255, 255, 255), (950, 20, progress_width, 20), 2)
            pygame.draw.rect(virtual_surface, (0, 200, 0), (950, 20, fill_width, 20))



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
                        print("🟥 Collision Triggered - Game Over")
                        return game_over()

            for b in boss_bullets:
                if dino.colliderect(pygame.Rect(b["x"], b["y"], 10, 10)):
                    if now - last_damage_time > damage_cooldown:
                        stamina -= 20
                        last_damage_time = now
                        hurt_sound.play()
                    if stamina <= 0:
                        print("🟥 Collision Triggered - Game Over")
                        return game_over()

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
            global first_time_no
            choosing = True
            state = 1  # 1: Yes, 2: No, 3: Warning, 4: Warning后只给Yes
            state3_start_time = None

            while choosing:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        # ✅ allow left/right only in state 1 or 2
                        if state == 1 and event.key == pygame.K_RIGHT:
                            state = 2
                        elif state == 2 and event.key == pygame.K_LEFT:
                            state = 1

                        # ✅ press Enter on NO (state 2)
                        elif state == 2 and event.key == pygame.K_RETURN:
                            if first_time_no:
                                state = 3
                                state3_start_time = pygame.time.get_ticks()
                                first_time_no = False
                            else:
                                print("🟥 Second No — exiting game")
                                pygame.quit()
                                sys.exit()

                        # ✅ press Enter on YES (state 1 or 4)
                        elif state in [1, 4] and event.key == pygame.K_RETURN:
                            print("🔁 Restarting game...")
                            return "restart"

                # ✅ 延迟切换到 gameover4（只能按 YES）
                if state == 3 and state3_start_time:
                    elapsed = pygame.time.get_ticks() - state3_start_time
                    if elapsed >= 1500:
                        state = 4
                        state3_start_time = None

                # ✅ 显示对应的 game over 图片
                if state == 1:
                    virtual_surface.blit(game_over_img1, (0, 0))
                elif state == 2:
                    virtual_surface.blit(game_over_img2, (0, 0))
                elif state == 3:
                    virtual_surface.blit(game_over_img3, (0, 0))
                elif state == 4:
                    virtual_surface.blit(game_over_img4, (0, 0))

                scaled_surface = pygame.transform.scale(virtual_surface, (WIDTH, HEIGHT))
                screen.blit(scaled_surface, (0, 0))
                pygame.display.flip()











        


        def win_game():
            # 显示工厂背景
            factory_bg = pygame.image.load("assets/background3.png").convert()
            factory_bg = pygame.transform.scale(factory_bg, (VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
            fireball_img = pygame.image.load("assets/bullet.png").convert_alpha()
            fireball_img = pygame.transform.scale(fireball_img, (40, 40))
            dino_shoot = pygame.image.load("assets/shoot4.png").convert_alpha()
            dino_shoot = pygame.transform.scale(dino_shoot, (100, 100))
            explosion = pygame.image.load("assets/explosion.png").convert_alpha()
            explosion = pygame.transform.scale(explosion, (300, 250))

            fire_x = 100
            fire_y = VIRTUAL_HEIGHT // 2
            fire_target = VIRTUAL_WIDTH - 200

            shoot_sound = pygame.mixer.Sound("music/shoot.mp3")
            explosion_sound = pygame.mixer.Sound("music/explosion.mp3")

            shoot_sound.play()

            while fire_x < fire_target:
                virtual_surface.blit(factory_bg, (0, 0))
                virtual_surface.blit(dino_shoot, (50, fire_y - 30))
                virtual_surface.blit(fireball_img, (fire_x, fire_y))
                fire_x += 15

                scaled_surface = pygame.transform.scale(virtual_surface, (WIDTH, HEIGHT))
                screen.blit(scaled_surface, (0, 0))
                pygame.display.flip()
                pygame.time.wait(30)

            # 撞到 -> 爆炸
            explosion_sound.play()
            for _ in range(3):
                virtual_surface.blit(factory_bg, (0, 0))
                virtual_surface.blit(explosion, (fire_target - 50, fire_y - 80))
                scaled_surface = pygame.transform.scale(virtual_surface, (WIDTH, HEIGHT))
                screen.blit(scaled_surface, (0, 0))
                pygame.display.flip()
                pygame.time.wait(200)

            # 烟雾 + 字幕
            for alpha in range(0, 200, 10):
                smoke = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
                smoke.fill((100, 100, 100, alpha))
                virtual_surface.blit(smoke, (0, 0))
                scaled_surface = pygame.transform.scale(virtual_surface, (WIDTH, HEIGHT))
                screen.blit(scaled_surface, (0, 0))
                pygame.display.flip()
                pygame.time.wait(100)

            # 剧情文字
            font = pygame.font.SysFont("Arial", 48, bold=True)
            line1 = font.render("You destroyed the factory!", True, (255, 255, 255))
            line2 = font.render("Nature is safe again.", True, (200, 255, 200))
            line3 = font.render("Thanks for playing!", True, (255, 255, 0))

            virtual_surface.blit(line1, (VIRTUAL_WIDTH // 2 - 250, 200))
            virtual_surface.blit(line2, (VIRTUAL_WIDTH // 2 - 230, 260))
            virtual_surface.blit(line3, (VIRTUAL_WIDTH // 2 - 210, 320))

            scaled_surface = pygame.transform.scale(virtual_surface, (WIDTH, HEIGHT))
            screen.blit(scaled_surface, (0, 0))
            pygame.display.flip()

            pygame.time.wait(12000)
            pygame.quit()
            sys.exit()




        def level_up():
            nonlocal bullets, stamina

            pygame.event.clear()
            
            big_food = pygame.transform.scale(food_img, (100, 100))
            big_mana = pygame.transform.scale(mana_img, (100, 100))

            choosing = True
            
            while choosing:
                virtual_surface.fill(BG_COLOR)
                
                font = pygame.font.SysFont("Arial", 40, bold=True)
                hint_font = pygame.font.SysFont("Arial", 36, bold=True)

                # 图标更大
                

                # 中心点
                center_x = VIRTUAL_WIDTH // 2
                top_y = VIRTUAL_HEIGHT // 2 - 160

                # 顶部标题
                title_surface = font.render("Level Up! Choose a reward:", True, (100, 160, 255))
                title_rect = title_surface.get_rect(center=(center_x, top_y))
                virtual_surface.blit(title_surface, title_rect)

                # 左选项（mana）
                left_text = font.render("Press M to Refill Mana", True, (100, 160, 255))
                left_text_x = center_x - 480  # 再往左一点
                left_text_y = top_y + 100
                virtual_surface.blit(left_text, (left_text_x, left_text_y))
                virtual_surface.blit(big_mana, (left_text_x + 120, left_text_y + 45))  # 文字下方居中放图

                # 右选项（stamina）
                right_text = font.render("Press S to Boost Stamina", True, (100, 160, 255))
                right_text_x = center_x + 80
                right_text_y = top_y + 100
                virtual_surface.blit(right_text, (right_text_x, right_text_y))
                virtual_surface.blit(big_food, (right_text_x + 150, right_text_y + 45))

                # 底部提示
                hint_surface = hint_font.render("Press twice to confirm.", True, (180, 180, 180))
                hint_rect = hint_surface.get_rect(center=(center_x, VIRTUAL_HEIGHT // 2 + 200))
                virtual_surface.blit(hint_surface, hint_rect)


                    # ✅ 显示画面
                scaled_surface = pygame.transform.scale(virtual_surface, (WIDTH, HEIGHT))
                screen.blit(scaled_surface, (0, 0))
                pygame.display.flip()

                # 监听按键
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            bullets = 5
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

            # ✅ 拷贝当前 virtual_surface 内容作为背景
            pause_bg = pygame.transform.scale(virtual_surface.copy(), (WIDTH, HEIGHT))

            clock = pygame.time.Clock()
            while paused:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        paused = False

                screen.blit(pause_bg, (0, 0))
                screen.blit(pause_text, text_rect)
                pygame.display.flip()
                clock.tick(30)  # 用 clock 控制帧率




        running = True
        while running:
            dt = clock.tick(60)

            prev_dino_state = dino_state  # Save the previous state for comparison

        
        
            elapsed = pygame.time.get_ticks() - start_time
            screen.fill(BG_COLOR)

            game_speed = 5 + level + (elapsed / 15000)

            # ✅ 第三关跑到终点就胜利，不用杀 boss
            if level == 3:
                level3_start = sum(LEVEL_DURATIONS[i] for i in range(1, 3))  # 累加前两关
                level3_elapsed = elapsed - level3_start
                if level3_elapsed >= LEVEL_DURATIONS[3] - 5000:
                    print("✅ Win by reaching end of Level 3")
                    return win_game()  # 确保返回值传到主循环




        
        
        
        
        # Move and draw scrolling background
            bg_x -= int(game_speed * 0.5)  # Adjust speed for parallax effect
            if bg_x <= -VIRTUAL_WIDTH:
                bg_x = 0

        # Draw background images side-by-side for looping
            current_bg = bg_img1 if level == 1 else bg_img2 if level == 2 else bg_img3
            virtual_surface.blit(current_bg, (bg_x, 0))
            virtual_surface.blit(current_bg, (bg_x + VIRTUAL_WIDTH, 0))

            # === Add white gradient overlay ===
            overlay = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
            for y in range(VIRTUAL_HEIGHT):
                alpha = int(140 * ((y / VIRTUAL_HEIGHT) ** 2))  # 渐变公式，下方更白
                pygame.draw.line(overlay, (255, 255, 255, alpha), (0, y), (VIRTUAL_WIDTH, y))

            virtual_surface.blit(overlay, (0, 0))  # ✅ 一定要 blit 在 virtual_surface 上


            for y in range(HEIGHT):
                alpha = int(140 * ((y / HEIGHT) ** 2))  # 下越大，上越小
                pygame.draw.line(overlay, (255, 255, 255, alpha), (0, y), (WIDTH, y))
            virtual_surface.blit(overlay, (0, 0))



            # Animate birds
            bird_frame_timer += 1
            if bird_frame_timer > 5:
                bird_frame_index = (bird_frame_index + 1) % len(bird_imgs)
                bird_frame_timer = 0

            

# 计算当前关卡
            cumulative = 0
            for i in range(1, 4):
                cumulative += LEVEL_DURATIONS[i]
                if elapsed < cumulative:
                    current_level = i
                    break
            else:
                current_level = 3

            # 更新关卡并执行切换逻辑
            if current_level != level:
                level = current_level
                if level <= 3:
                    level_up()
                if level == 2:
                    pygame.mixer.music.load("music/level2_bgm.mp3")
                    pygame.mixer.music.play(-1)
                elif level == 3:
                    pygame.mixer.music.load("music/level3_bgm.mp3")
                    pygame.mixer.music.play(-1)
                    boss_appearing = True
                    boss_active = False
                    boss_entry_timer = pygame.time.get_ticks()
                    boss.x = WIDTH + 100
                    boss.y = -100
                    boss_intro_active = True
                    boss_intro_timer = pygame.time.get_ticks()


                
                
                
                
                
                
                if level <= 3:
                    level_up()
            #bossadd
                if level == 3:
                    boss_appearing = True
                    boss_active = False
                    boss_entry_timer = pygame.time.get_ticks()
                    boss.x = WIDTH + 100  # 右侧外部
                    boss.y = -100         # 屏幕上方外部
 
                    
                    boss_intro_active = True
                    boss_intro_timer = pygame.time.get_ticks()
                    #pygame.mixer.Sound("sounds/boss_warning.wav").play()


            
            #bossadd
                if level > 3:
                    boss_active = False  # stop boss if still alive
                    win_game()

            

            # ✅ 每秒减少一点 stamina，但不会影响碰撞的 cooldown
                if pygame.time.get_ticks() - last_stamina_drain > 1000:
                    stamina -= 3
                    last_stamina_drain = pygame.time.get_ticks()
                    if stamina <= 0:
                        print("🟥 Collision Triggered - Game Over")
                        result = game_over()
                        if result == "restart":
                            return "restart"
                        else:
                            pygame.quit()
                            sys.exit()
           
           
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

            # ✅ 每秒减少一点 stamina（只有移动时）
            if pygame.time.get_ticks() - last_stamina_drain > 1000:
                if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT] or keys[pygame.K_UP]:  # 移动才扣
                    stamina -= 1
                    last_stamina_drain = pygame.time.get_ticks()
                    if stamina <= 0:
                        print("🟥 Stamina depleted - Game Over")
                        result = game_over()
                        if result == "restart":
                            return "restart"
                        elif result == "menu":
                            return "menu"




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
                if dino.y >= GROUND_Y:
                    dino.y = GROUND_Y
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
                
                
                #pygame.draw.rect(virtual_surface, (255, 0, 0), dino, 2)  # Red outline, thickness 2

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


            result = handle_collisions()
            if result == "restart":
                return "restart"
            elif result == "menu":
                return "menu"
            # ❌ 不要在 else 直接退出游戏，应该继续运行






            # === Boss延迟登场（飞入）动画 ===
            if level == 3 and boss_appearing:
                time_since_entry = pygame.time.get_ticks() - boss_entry_timer

    # boss缓缓滑入
                target_x = VIRTUAL_WIDTH - 300
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
                    boss_width, boss_height = 120, 120  # 👈 和你 boss 图片尺寸一致
                    if random.random() < 0.7:
                        # 🟡 飞在上方，靠右、远离玩家
                        boss_target_x = random.randint(VIRTUAL_WIDTH - 350, VIRTUAL_WIDTH - 200)  # 更靠右
                        boss_target_y = random.randint(100, 150)  # 上半区
                    else:
                        # 🔴 飞下来攻击，靠右下角，更低更难打
                        boss_target_x = random.randint(VIRTUAL_WIDTH - 200, VIRTUAL_WIDTH - 100)
                        boss_target_y = random.randint(350, 460)  # ✅ 更低

                    boss_target = pygame.Vector2(boss_target_x, boss_target_y)





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
                if boss_attack_type == "bullet_fan" and now - last_fan_fire > 900:
                    last_fan_fire = now
                    base_angle = math.pi
                    for i in range(-4, 5):
                        angle = base_angle + i * 0.2
                        boss_bullets.append({
                            "x": boss.centerx,
                            "y": boss.centery,
                            "vx": 8 * math.cos(angle),
                            "vy": 8 * math.sin(angle)
                        })


            # Spiral bullet
                if boss_attack_type == "spiral" and now - last_fan_fire > 70:
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

                # Draw boss bullets as orange
                #for b in boss_bullets:
                    #pygame.draw.rect(virtual_surface, (255, 165, 0), pygame.Rect(b["x"], b["y"], 10, 10))  # orange



            # Check collision: Boss bullets → player
                for b in boss_bullets:
                    if dino.colliderect(pygame.Rect(b["x"], b["y"], 10, 10)):
                        if now - last_damage_time > damage_cooldown:
                            stamina -= 20
                            last_damage_time = now
                            hurt_sound.play()
                        if stamina <= 0:
                            print("🟥 Collision Triggered - Game Over")
                            result = game_over()
                            if result == "restart":
                                return "restart"
                            else:
                                return "exit" # quit
           


            # Check collision: Your bullets → boss
                for bullet in bullets_fired[:]:
                    if boss.colliderect(bullet["rect"]):
                        bullets_fired.remove(bullet)
                        boss_health -= 1
                        if boss_health <= 0:
                            boss_active = False
                            boss_bullets.clear()
                            
                            print("Boss defeated!")












            # Draw Dino
           # Dino image offset (to align with hitbox)
            image_offset_x = -35  # 保持原本对齐
            image_offset_y = -20# 👈 比如原本是 -20，你可以改小让它15

            # 在绘图阶段使用偏移，不改变 hitbox
            if dino_state == "run":
                virtual_surface.blit(dino_run_imgs[dino_frame_index], (dino.x + image_offset_x, dino.y + image_offset_y))
            elif dino_state == "jump":
                virtual_surface.blit(dino_jump_imgs[dino_frame_index], (dino.x + image_offset_x, dino.y + image_offset_y))
            elif dino_state == "shoot":
                virtual_surface.blit(dino_shoot_imgs[dino_frame_index], (dino.x + image_offset_x, dino.y + image_offset_y))




            # addboss
            if boss_active:
                boss_img = boss_imgs[(pygame.time.get_ticks() // 100) % len(boss_imgs)]
                virtual_surface.blit(boss_img, (boss.x, boss.y))

                pygame.draw.rect(virtual_surface, WHITE, (450, 20, 200, 20), 2)
                pygame.draw.rect(virtual_surface, RED, (450, 20, boss_health * 66, 20))
                hint = "!!!" if boss_attack_type == "bullet_fan" else ">:("
                draw_text(hint, boss.centerx - 10, boss.y - 30, (255, 255, 255))  # White face text







            # Draw Boss Bullets
            for b in boss_bullets:
                pygame.draw.circle(virtual_surface, RED, (int(b["x"]), int(b["y"])), 5)













            # Draw enemies
            for enemy in enemies:
                if enemy["type"] == "tree":
                    virtual_surface.blit(tree_img, (enemy["rect"].x - 10, enemy["rect"].y))  
                elif enemy["type"] == "bird":
                    virtual_surface.blit(bird_imgs[bird_frame_index], (enemy["rect"].x, enemy["rect"].y - 10))
                elif enemy["type"] == "car1":
                    virtual_surface.blit(car1_img, (enemy["rect"].x-10, enemy["rect"].y - 20))  
                elif enemy["type"] == "car2":
                    virtual_surface.blit(car2_img, (enemy["rect"].x-10, enemy["rect"].y - 20))
                elif enemy["type"] == "barrel":
                    BARREL_OFFSET_X = -10
                    BARREL_OFFSET_Y = -10  # 👈 往上抬一点就减少 Y 值

                    virtual_surface.blit(barrel_img, (
                        enemy["rect"].x + BARREL_OFFSET_X,
                        enemy["rect"].y + BARREL_OFFSET_Y
))


                    # 🛠 DEBUG: Draw enemy hitboxes
                #pygame.draw.rect(virtual_surface, (255, 0, 0), enemy["rect"], 2)

            # DRAW TIMER HERE
            draw_level_timer(elapsed, level, LEVEL_DURATIONS)

            # Draw fruits and bullets
            for food in foods:
                virtual_surface.blit(food_img, food)

            for bullet in bullets_fired:
                virtual_surface.blit(bullet_img, (bullet["x"], bullet["y"]))

            if boss_intro_active:
                time_since_intro = pygame.time.get_ticks() - boss_intro_timer
                if time_since_intro < 3000:  # 播放 3 秒
                    if (time_since_intro // 500) % 2 == 0:  # 每 0.5 秒闪一下
                        warning_text = big_font.render("WARNING!", True, (255, 0, 0))
                        text_rect = warning_text.get_rect(center=(VIRTUAL_WIDTH // 2, VIRTUAL_HEIGHT // 2))  # ✅
                        virtual_surface.blit(warning_text, text_rect)
                else:
                    boss_intro_active = False






            # Draw UI
            draw_text(f"Level: {level}", 20, 10, (255, 255, 255))  # White and shifted up


            # Code for stamina bar
            bar_x, bar_y = 20, 50
            bar_width, bar_height = 100, 20
            bar_fill = int((stamina / 100) * bar_width)

            pygame.draw.rect(virtual_surface, (255,255,255), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(virtual_surface, (255,0,0), (bar_x, bar_y, bar_fill, bar_height))

            stamina_index = int((stamina / 100) * (len(stamina_bar_imgs) - 1))
            stamina_index = stamina_index = max(0, min(7, 7 - stamina // 13))


            stamina_img = stamina_bar_imgs[stamina_index]

            virtual_surface.blit(stamina_img, (bar_x + bar_width + 10, bar_y - 10))

            # Mana bullets display
            for i in range(bullets):
                virtual_surface.blit(mana_img, (bar_x + bar_width + 50 + i * 35, bar_y - 10))
            
            
            scaled_surface = pygame.transform.scale(virtual_surface, (WIDTH, HEIGHT))
            screen.blit(scaled_surface, (0, 0))
            pygame.display.flip()



def load_images(prefix, count, scale):
    return [
        pygame.transform.scale(pygame.image.load(f"{prefix}{i}.png").convert_alpha(), scale)
        for i in range(1, count + 1)
    ]

# ✅ 加载资源
print("Loading background...")
bg_image = pygame.image.load("assets/bg/cutscene_bg.png").convert()
print("Loading portraits...")
portraits = load_images('assets/portrait', count=6, scale=(400,400))

# ✅ 主入口只写一遍
if __name__ == "__main__":
    while True:
        show_start_screen()
        tutorial(screen, bg_image, portraits)
        print("✅ Cutscene ended or skipped, now entering game.")
        result = run_game()
        if result == "exit":
            break
        elif result == "menu":
            continue



