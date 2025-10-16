# In main.py

import pygame
from game.game_engine import GameEngine

# Initialize pygame/Start application
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game loop
engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True
    while running:
        SCREEN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- Updated game loop logic ---
        if engine.game_state == "playing":
            engine.handle_input()
            engine.update()
        elif engine.game_state == "replay":
            # The handle_replay_input method will return False if ESC is pressed
            running = engine.handle_replay_input()
        # --------------------------------

        engine.render(SCREEN) # Always render the current state
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()