import pygame
import time
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.winning_score = 5  # default
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.font = pygame.font.SysFont("Arial", 30)
        self.reset_scores()  # start with 0-0

        # Load sound effects
        self.sound_paddle = pygame.mixer.Sound("sounds/paddle_hit.wav")
        self.sound_wall = pygame.mixer.Sound("sounds/wall_bounce.wav")
        self.sound_score = pygame.mixer.Sound("sounds/score.wav")
        self.ball.game_engine = self  # let ball access sounds

    def reset_scores(self):
        self.player_score = 0
        self.ai_score = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        if self.ball.x <= 0:
            self.ai_score += 1
            self.sound_score.play()
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.sound_score.play()
            self.ball.reset()

        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

    def check_game_over(self, screen):
        winner_text = None
        if self.player_score >= self.winning_score:
            winner_text = "Player Wins!"
        elif self.ai_score >= self.winning_score:
            winner_text = "AI Wins!"

        if winner_text:
            screen.fill((0, 0, 0))
            text_surface = self.font.render(winner_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.width//2, self.height//2))
            screen.blit(text_surface, text_rect)
            pygame.display.flip()
            pygame.time.delay(1500)  # show winner briefly

            # Show replay menu (resets scores and ball)
            self.show_replay_menu(screen)

        # Always return False so main loop continues
        return False


    def show_replay_menu(self, screen):
        menu_font = pygame.font.SysFont("Arial", 28)
        options = [
            "Press 3 for Best of 3",
            "Press 5 for Best of 5",
            "Press 7 for Best of 7",
            "Press ESC to Exit"
        ]

        while True:
            screen.fill((0, 0, 0))
            for i, option in enumerate(options):
                text_surface = menu_font.render(option, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(self.width//2, self.height//2 - 60 + i*40))
                screen.blit(text_surface, text_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.unicode == "3":
                        self.winning_score = 3
                    elif event.unicode == "5":
                        self.winning_score = 5
                    elif event.unicode == "7":
                        self.winning_score = 7
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                    else:
                        continue

                    # Reset game for new round
                    self.reset_scores()
                    self.ball.reset()
                    return  # exit menu and continue game
