import pygame

def draw_text(screen, font, text, x, y, color=(255, 255, 255)):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def draw_stamina_bar(screen, stamina, stamina_imgs, pos=(20, 50)):
    bar_x, bar_y = pos
    bar_width, bar_height = 100, 20
    bar_fill = int((stamina / 100) * bar_width)

    pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))     # red background
    pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_fill, bar_height))      # green fill

    stamina_index = 7 - min(7, max(0, int(stamina // 13)))  # safely clamp
    screen.blit(stamina_imgs[stamina_index], (bar_x + bar_width + 10, bar_y - 10))

def draw_mana_icons(screen, mana_img, bullets, start_pos):
    for i in range(bullets):
        screen.blit(mana_img, (start_pos[0] + i * 35, start_pos[1]))

def draw_level_progress_bar(screen, elapsed, duration, WIDTH):
    progress_width = 200
    fill_width = int((elapsed / duration) * progress_width)
    fill_width = min(fill_width, progress_width)

    pygame.draw.rect(screen, (255, 255, 255), (WIDTH - 240, 20, progress_width, 20), 2)
    pygame.draw.rect(screen, (0, 200, 0), (WIDTH - 240, 20, fill_width, 20))
