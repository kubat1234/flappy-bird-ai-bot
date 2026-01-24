import pygame
import random

class Pipe:
    WIDTH = 100
    def __init__(self, x, gap=400, velocity=10):
        self.x = x
        self.gap = gap
        self.vel = velocity
        
        self.height = 0
        self.top = 0
        self.bottom = 0
        
        self.pipe_top = pygame.Rect(0, 0, Pipe.WIDTH, 0)
        self.pipe_bottom = pygame.Rect(0, 0, Pipe.WIDTH, 0)
        
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - 600
        self.bottom = self.height + self.gap 
        
        self.pipe_top.x = self.x
        self.pipe_top.y = self.top
        self.pipe_top.height = 600
        
        self.pipe_bottom.x = self.x
        self.pipe_bottom.y = self.bottom
        self.pipe_bottom.height = 600
        
    def move(self):
        self.x -= self.vel
        self.pipe_top.x = self.x
        self.pipe_top.y = self.top
        self.pipe_bottom.x = self.x
        self.pipe_bottom.y = self.bottom

    def draw(self, win):
        pygame.draw.rect(win, (0, 200, 0), self.pipe_top)
        pygame.draw.rect(win, (0, 200, 0), self.pipe_bottom)

    def collide(self, bird):
        if self.pipe_top.colliderect(bird.rect) or self.pipe_bottom.colliderect(bird.rect):
            return True
        return False
