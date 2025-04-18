import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Cutscene Test")

# Dummy background and portraits
background = pygame.Surface(screen.get_size())
background.fill((100, 150, 200))

dummy_portrait = pygame.Surface((300, 300))
dummy_portrait.fill((200, 100, 100))

class Cutscene:
    def __init__(self, screen, background, events=None):
        self.screen = screen
        self.background = background
        self.font = pygame.font.Font(None, 48)
        self.events = events or []
        self.clock = pygame.time.Clock()
        self.finished = False
        self.current_event_index = 0

        self.white_opacity = 120
        self.white_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.white_surface.fill((255, 255, 255, self.white_opacity))

    def play(self):
        running = True

        while running:
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.white_surface, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.current_event_index += 1
                    if self.current_event_index >= len(self.events):
                        running = False
                        self.finished = True

            if self.current_event_index < len(self.events):
                current = self.events[self.current_event_index]

                if "portrait" in current and current["portrait"]:
                    portrait = pygame.transform.scale(current["portrait"], (400, 400))
                    portrait_x = (self.screen.get_width() - portrait.get_width()) // 2
                    portrait_y = 50
                    self.screen.blit(portrait, (portrait_x, portrait_y))

                if current.get("text"):
                    lines = wrap_text(current["text"], self.font, 1000)
                    for i, line in enumerate(lines):
                        text_surface = self.font.render(line, True, (0, 0, 0))
                        text_x = (self.screen.get_width() - text_surface.get_width()) // 2
                        text_y =0
                        self.screen.blit(text_surface, (text_x, text_y))

            pygame.display.update()
            self.clock.tick(60)

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ''
    for word in words:
        test_line = current_line + word + ' '
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + ' '
    if current_line:
        lines.append(current_line.strip())
    return lines

# Sample cutscene event
events = [
    {"text": "Hey, my name is Dante the Dinosaur!", "portrait": dummy_portrait},
    {"text": "I’m part Pentaceratops, Pterodactylus, and T-Rex!", "portrait": dummy_portrait},
]

# Run cutscene
cutscene = Cutscene(screen, background, events)
cutscene.play()
 