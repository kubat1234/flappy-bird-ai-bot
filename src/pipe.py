import pygame
import random

class Pipe:
    WIDTH = 100
    def __init__(self, x, win_height, gap=350, velY=2, velX=6):
        self.x = x
        self.win_height = win_height
        self.gap = gap
        self.velY = velY
        self.velX = velX
        
        self.gap_pos = 0 
        
        self.passed = False
        self.set_height()

    def set_height(self):
        self.gap_pos = random.randrange(
            int(self.win_height * 0.1), 
            int(self.win_height * 0.9 - self.gap)
        )
        
    def move(self):
        self.x -= self.velX
        self.gap_pos += self.velY
        if self.gap_pos + self.gap > self.win_height * 0.9 or self.gap_pos < self.win_height * 0.1:
            self.velY *= -1

    def draw(self, win):
        pygame.draw.rect(win, (0, 200, 0), (self.x, 0, self.WIDTH, self.gap_pos))
        
        bottom_y = self.gap_pos + self.gap
        bottom_height = self.win_height - bottom_y
        pygame.draw.rect(win, (0, 200, 0), (self.x, bottom_y, self.WIDTH, bottom_height))

    def collide(self, bird):
        pipe_top_rect = pygame.Rect(self.x, 0, self.WIDTH, self.gap_pos)
        pipe_bottom_rect = pygame.Rect(self.x, self.gap_pos + self.gap, self.WIDTH, self.win_height)
        
        if pipe_top_rect.colliderect(bird.rect) or pipe_bottom_rect.colliderect(bird.rect):
            return True
        return False
