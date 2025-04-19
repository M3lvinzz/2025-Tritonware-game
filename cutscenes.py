import pygame
import sys

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
            self.screen.blit(self.background, (0, 0))  # Draw full background image

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        self.finished = True
                    elif event.key == pygame.K_SPACE:
                        self.current_event_index += 1
                        if self.current_event_index >= len(self.events):
                            running = False
                            self.finished = True

            if self.current_event_index < len(self.events):
                current = self.events[self.current_event_index]

                if "portrait" in current and current["portrait"]:
                    portrait = pygame.transform.scale(current["portrait"], (500, 500))  # Enlarge portrait
                    portrait_x = (self.screen.get_width() - portrait.get_width()) // 2
                    portrait_y = -130
                    self.screen.blit(portrait, (portrait_x, portrait_y))

                if current.get("text"):
                    lines = wrap_text(current["text"], self.font, 1000)
                    for i, line in enumerate(lines):
                        text_surface = self.font.render(line, True, (255, 255, 255))
                        text_x = (self.screen.get_width() - text_surface.get_width()) // 2
                        text_y = 400 + i * 45
                        self.screen.blit(text_surface, (text_x, text_y))

            small_font = pygame.font.Font(None, 24)
            prompt_text = small_font.render("Press [ESC] to skip or [SPACE] to continue", True, (255, 255, 255))
            prompt_rect = prompt_text.get_rect(topright=(self.screen.get_width() - 20, 20))
            self.screen.blit(prompt_text, prompt_rect)
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

def tutorial(screen, bg, portraits):    
    cutscene_events = [
        {"text": "Hey, My name is Dante the Dinosaur!", 'portrait': portraits[3]},
        {"text": "I am part Pentaceratops, Pterodactylus, and Tyrannosaurus Rex! What can I say? I am a triple threat!", 'portrait': portraits[0]},
        {"text": "Humans sure have changed nature and the forest since us dinosaur’s time.", 'portrait': portraits[2]},
        {"text": "I am not sure where home is anymore. Can you help me find home?", 'portrait': portraits[2]},
        {"text": "While I am running, press [Arrow up] to Jump!", 'portrait': portraits[3]},
        {"text": "I can't keep running forever, look at my Stamina bar!", 'portrait': portraits[5]},
        {"text": "Make sure to pick up the meat on the ground to replenish my stamina", 'portrait': portraits[0]},
        {"text": "I don't want to burn down the forest, but I allow myself to fire 3 fireballs to break any obstacle in my way!", 'portrait': portraits[4]},
        {"text": "Press [Right Arrow] to shoot a fireball. Be careful, I only get 3!", 'portrait': portraits[5]},
        {"text": "After every stage, you get to choose to replenish my fire", 'portrait': portraits[2]},
        {"text": "or increase my stamina!", 'portrait': portraits[4]},
        {"text": "To get home, I need to go through the forest, a town, and finally a factory", 'portrait': portraits[2]},
    ]
    cutscene = Cutscene(
        screen,
        bg, 
        cutscene_events,
    )
    cutscene.play()

def level1(screen, bg, portraits):
    cutscene_events = [
        {"text": "Wow, there were a lot of trees and birds in the way!", 'portrait': portraits[3]},
        {"text": "Lets try and get through the town as fast as possible", 'portrait': portraits[4]},
        {"text": "I have a bad feeling about the cars coming towards us", 'portrait': portraits[2]},
    ]
    cutscene = Cutscene(
        screen,
        bg, 
        cutscene_events,
    )
    cutscene.play()

def level2(screen, bg, portraits):
    cutscene_events = [
        {"text": "Man, the urbanization of this world is getting out of hand", 'portrait': portraits[2]},
        {"text": "It feels like I just ran through the suburbs for days", 'portrait': portraits[5]},
        {"text": "I think this part is the worst", 'portrait': portraits[5]},
        {"text": "The smoke and oil everywhere is suffocating ", 'portrait': portraits[2]},
        {"text": "Oops, I think I also attracted the attention of the factory owner", 'portrait': portraits[5]},
        {"text": "To defeat him, just have to hit 2 fireballs!", 'portrait': portraits[4]},
    ]
    cutscene = Cutscene(
        screen,
        bg, 
        cutscene_events,
    )
    cutscene.play()

def level_up_cutscene(screen, bg, portraits):
    cutscene_events = [
        {"text": "Level up!", "portrait": portraits[1]},
        {"text": "[B] to replenish fireballs", "portrait": portraits[1]},
        {"text": "[S] to increase stamina", "portrait": portraits[1]},
    ]
    cutscene = Cutscene(screen, bg, cutscene_events)
    cutscene.play()

def ending(screen, bg, portraits):
    cutscene_events = [
        {"text": "Well, that was a great adventure", 'portrait': portraits[3]},
        {"text": "Even though we explored a lot bad places like the factory", 'portrait': portraits[2]},
        {"text": "I had fun, and I hope you had fun helping me back home", 'portrait': portraits[4]},
        {"text": "See you next time and thank you for playing!", 'portrait': portraits[0]},
    ]
    cutscene = Cutscene(
        screen,
        bg, 
        cutscene_events,
    )
    cutscene.play()
    if __name__ == "__main__":
        pygame.init()
        WIDTH, HEIGHT = 1200, 500
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Cutscene Test")

        # Load background and portraits
        bg = pygame.image.load("assets/bg/cutscene_bg.png").convert()

        def load_images(prefix, count, scale):
            return [
                pygame.transform.scale(pygame.image.load(f"{prefix}{i}.png").convert_alpha(), scale)
                for i in range(1, count + 1)
            ]

        portraits = load_images("assets/portrait", count=6, scale=(60, 60))

        # Play the cutscene
        tutorial(screen, bg, portraits)


