import pygame

class Bird:
    GRAVITY = 0.6
    JUMP_POWER = 15
    TERMINAL_VELOCITY = 15
    COLOR = (255, 255, 0)
    MAX_ROTATION = 30
    MIN_ROTATION = -75
    ROT_VEL = 7
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 0.0
        self.tilt = 20
        
        self.img = pygame.Surface((34, 24), pygame.SRCALPHA) 
        self.img.fill((255, 255, 0))
        
        self.rect = self.img.get_rect(topleft=(x, y))

    def jump(self):
        self.vel = -self.JUMP_POWER

    def move(self):
        self.vel += self.GRAVITY
        
        if self.vel > self.TERMINAL_VELOCITY:
            self.vel = self.TERMINAL_VELOCITY

        self.y += self.vel
        self.rect.y = self.y

        if self.vel < 0:
            self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > self.MIN_ROTATION:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        
        new_rect = rotated_image.get_rect(center=self.rect.center)
        
        win.blit(rotated_image, new_rect.topleft)