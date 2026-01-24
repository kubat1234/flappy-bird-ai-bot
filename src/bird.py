import pygame

class Bird:
    GRAVITY = 0.6
    JUMP_POWER = 15
    TERMINAL_VELOCITY = 15
    COLOR = (255, 255, 0)
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 0.0
        
        self.rect = pygame.Rect(x, y, 34, 24)

    def jump(self):
        self.vel = -self.JUMP_POWER

    def move(self):
        self.vel += self.GRAVITY
        
        if self.vel > self.TERMINAL_VELOCITY:
            self.vel = self.TERMINAL_VELOCITY

        self.y += self.vel
        self.rect.y = self.y

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, self.rect)