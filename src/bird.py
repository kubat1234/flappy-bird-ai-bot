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
        self.tick = 0
        self.x = x
        self.y = y
        self.vel = 0.0
        self.tilt = 20
        
        self.img = pygame.Surface((34, 24), pygame.SRCALPHA) 
        self.img.fill((255, 255, 0))
        
        self.rect = self.img.get_rect(topleft=(x, y))
        self.alive = True
        self.score = 0

        self.pipes_passed = set()

    def jump(self):
        if self.alive:
            self.vel = -self.JUMP_POWER

    def move(self):
        self.tick += 1
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

    def die(self):
        self.alive = False

    def draw(self, win):
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        
        new_rect = rotated_image.get_rect(center=self.rect.center)
        
        win.blit(rotated_image, new_rect.topleft)

class SavableBird(Bird):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.move_history = []

    def jump(self):
        self.move_history.append(self.tick)
        super().jump()

    def get_move_history(self):
        return self.move_history

class ReplayBird(Bird):
    def __init__(self, x, y, move_history):
        super().__init__(x, y)
        self.move_history = move_history

    def move(self):
        if self.move_history and self.tick == self.move_history[0]:
            self.jump()
            self.move_history.pop(0)
        super().move()