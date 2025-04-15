import pygame
import sys

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
                    self.screen.blit(current["portrait"], (50, 300))

                if current.get("text"):
                    text_surface = self.font.render(current["text"], True, (255, 255, 255))
                    self.screen.blit(text_surface, current.get("pos", (100, 500)))

            pygame.display.update()
            self.clock.tick(60)

def tutorial(screen, bg, portraits):
    cutscene_events = [
    {"text": "Hey, My name is Dante the Dinosaur!", "pos": (100, 500), 'portrait': portraits[0]},
    {"text": "I am part Pentaceratops, Pterodactylus, and Tyrannosaurus Rex! What can I say? I am a triple threat!", "pos": (100, 500), 'portrait': portraits[1]},
    {"text": "Humans sure have changed nature and the forest since us dinosaur’s time.", "pos": (100, 500), 'portrait': portraits[2]},
    {"text": "I am not sure where home is anymore. Can you help me find home?", "pos": (100, 500), 'portrait': portraits[3]},
    {"text": "While I am running, press [Arrow up] to Jump!", "pos": (100, 500), 'portrait': portraits[4]},
    {"text": "I can't keep running forever, look at my Stamina bar!", "pos": (100, 500), 'portrait': portraits[5]},
    {"text": "Make sure to pick up the meat on the ground to replenish my stamina", "pos": (100, 500), 'portrait': portraits[0]},
    {"text": "I don't want to burn down the forest, but I allow myself to fire 3 fireballs to break any obstacle in my way!", "pos": (100, 500), 'portrait': portraits[1]},
    {"text": "Press [Right Arrow] to shoot a fireball. Be careful, I only get 3!", "pos": (100, 500), 'portrait': portraits[2]},
    {"text": "EX", "pos": (100, 500)},
    ]

    cutscene = Cutscene(
        screen,
        bg, 
        cutscene_events,
        )
    cutscene.play()

