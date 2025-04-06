
#Starting up Pygame
import pygame, sys

pygame.init()



#Playing background music
#pygame.mixer.music.load("bgm.mp3")
#pygame.mixer.music.set_volume(0.5)  # set volume to 50%
#pygame.mixer.music.play(-1)  


# Creating the game window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("College Decision Game")

# Font
font = pygame.font.SysFont("Arial", 24)

# Writing text on the screen，x = how far from the left the text will start  ,y = how far from the top the text will start
def draw_text(text, x, y):
    rendered = font.render(text, True, (0, 0, 0))
    screen.blit(rendered, (x, y))

# List of scenarios (questions + choices)
scenarios = [
    {
        "question": "You have an exam tomorrow. What do you do?",
        "choices": [
            {"text": "Study hard", "grades": +10, "social": -5},
            {"text": "Go to a party", "grades": -5, "social": +10}
        ]
    },
    {
        "question": "You’re invited to join a club. Do you join?",
        "choices": [
            {"text": "Yes, join the club", "grades": 0, "social": +10},
            {"text": "No, focus on academics", "grades": +5, "social": 0}
        ]
    },
    {
        "question": "Your friend asks for help with homework. What do you do?",
        "choices": [
            {"text": "Help them", "grades": +5, "social": +5},
            {"text": "Say no, you're too busy", "grades": +10, "social": -5}
        ]
    }
]

# Player’s current scores
player_state = {
    "grades": 50,
    "social": 50
}


#Game state trackers
current_scenario_index = 0
game_started = False




# Show one scenario and its choices
def draw_scenario(scenario):
    draw_text(scenario["question"], 50, 100)
    draw_text("1. " + scenario["choices"][0]["text"], 70, 160)
    draw_text("2. " + scenario["choices"][1]["text"], 70, 200)



# Show current players scores
def draw_scores():
    draw_text(f"Grades: {player_state['grades']}", 600, 20)
    draw_text(f"Social: {player_state['social']}", 600, 50)



# Handle what happens when the player chooses
def handle_choice(choice_index):
    global current_scenario_index
    if current_scenario_index < len(scenarios):
        scenario = scenarios[current_scenario_index]
        choice = scenario["choices"][choice_index]



        # Update player stats
        player_state["grades"] += choice["grades"]
        player_state["social"] += choice["social"]

        # Move to next scenario
        current_scenario_index += 1

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if not game_started and event.key == pygame.K_SPACE:
                game_started = True
            elif game_started:
                if event.key == pygame.K_1:
                    handle_choice(0)
                elif event.key == pygame.K_2:
                    handle_choice(1)

    # Background
    screen.fill((255, 255, 255))

    if not game_started:
        draw_text("College Decision Game!", 280, 200)
        draw_text("Press SPACE to start", 300, 260)
    else:
        if current_scenario_index < len(scenarios):
            draw_scenario(scenarios[current_scenario_index])
            draw_scores()
        else:
            draw_text("Game Over!", 330, 250)
            draw_scores()

    # This refreshes the screen, check for inputs
    pygame.display.flip()
