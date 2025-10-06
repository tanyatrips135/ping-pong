import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1


    def check_collision(self, player, ai):
        ball_rect = self.rect()
        player_rect = player.rect()
        ai_rect = ai.rect()

        half_width = self.width / 2  # use this instead of radius

        # Check collision with player paddle
        if ball_rect.colliderect(player_rect):
            if self.velocity_x > 0:  # moving right
                self.x = player_rect.left - self.width
            else:  # moving left
                self.x = player_rect.right
            self.velocity_x *= -1

        # Check collision with AI paddle
        elif ball_rect.colliderect(ai_rect):
            if self.velocity_x < 0:  # moving left
                self.x = ai_rect.right
            else:  # moving right
                self.x = ai_rect.left - self.width
            self.velocity_x *= -1


    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
