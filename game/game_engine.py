import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine
WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # ... (other initializations) ...
        self.player = Paddle(10, height // 2 - 50, 10, 100)
        self.ai = Paddle(width - 20, height // 2 - 50, 10, 100)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.score_font = pygame.font.SysFont("Arial", 50)
        self.menu_font = pygame.font.SysFont("Arial", 30)

        self.winning_score = 5
        self.game_state = "playing"
        self.winner = None

        # --- New: Load Sound Effects ---
        self.paddle_hit_sound = pygame.mixer.Sound("assets/paddle_hit.wav")
        self.wall_bounce_sound = pygame.mixer.Sound("assets/wall_bounce.wav")
        self.score_sound = pygame.mixer.Sound("assets/score_point.wav")
        # -------------------------------

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)
    
    def handle_replay_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    self.reset_game(3)
                elif event.key == pygame.K_5:
                    self.reset_game(5)
                elif event.key == pygame.K_7:
                    self.reset_game(7)
                elif event.key == pygame.K_ESCAPE:
                    return False
        return True

    def update(self):
        self.ball.move()
        self.check_ball_collision()

        # --- New: Wall bounce logic moved here to play sound ---
        if self.ball.y <= 0 or self.ball.y + self.ball.height >= self.height:
            self.ball.velocity_y *= -1
            self.wall_bounce_sound.play()
        # --------------------------------------------------------

        # --- Updated: Play sound on score ---
        if self.ball.x <= 0:
            self.ai_score += 1
            self.score_sound.play()
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.score_sound.play()
            self.ball.reset()
        # ------------------------------------

        if self.player_score >= self.winning_score:
            self.winner = "Player"
            self.game_state = "replay"
        elif self.ai_score >= self.winning_score:
            self.winner = "AI"
            self.game_state = "replay"

        self.ai.auto_track(self.ball, self.height)

    def check_ball_collision(self):
        # --- Updated: Play sound on paddle hit ---
        if self.ball.velocity_x < 0:
            if self.ball.rect().colliderect(self.player.rect()):
                self.ball.velocity_x *= -1
                self.ball.x = self.player.x + self.player.width
                self.paddle_hit_sound.play() # Play hit sound

        if self.ball.velocity_x > 0:
            if self.ball.rect().colliderect(self.ai.rect()):
                self.ball.velocity_x *= -1
                self.ball.x = self.ai.x - self.ball.width
                self.paddle_hit_sound.play()
                self.ball.x = self.ai.x - self.ball.width

    # --- New: Resets the game for a new match ---
    def reset_game(self, winning_score):
        self.winning_score = winning_score
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.game_state = "playing"
        self.winner = None
    # --------------------------------------------

    def render(self, screen):
        # Dispatch rendering based on game state
        if self.game_state == "playing":
            self.render_game_screen(screen)
        elif self.game_state == "replay":
            self.render_replay_screen(screen)

    def render_game_screen(self, screen):
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))
        
        player_text = self.score_font.render(str(self.player_score), True, WHITE)
        ai_text = self.score_font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))
    
    # --- New: Draws the replay menu ---
    def render_replay_screen(self, screen):
        # Winner message
        winner_message = f"{self.winner} Wins!"
        text_surface = self.score_font.render(winner_message, True, WHITE)
        text_rect = text_surface.get_rect(center=(self.width / 2, self.height / 3))
        screen.blit(text_surface, text_rect)

        # Replay options
        options = [
            "Press [3] for Best of 3",
            "Press [5] for Best of 5",
            "Press [7] for Best of 7",
            "Press [ESC] to Exit"
        ]
        
        for i, option in enumerate(options):
            option_surface = self.menu_font.render(option, True, WHITE)
            option_rect = option_surface.get_rect(center=(self.width / 2, self.height / 2 + i * 40))
            screen.blit(option_surface, option_rect)