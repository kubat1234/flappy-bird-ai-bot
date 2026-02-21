import neat
import pygame

class Bird:
    GRAVITY = 0.6
    JUMP_POWER = 12
    TERMINAL_VELOCITY = 15
    COLOR = (255, 255, 0)
    MAX_ROTATION = 30
    MIN_ROTATION = -75
    ROT_VEL = 7
    JUMP_DELAY = 10
    
    def __init__(self, win):
        self.win = win
        self.tick = 0
        self.x = self.win.get_width() // 4
        self.y = self.win.get_height() // 3
        self.vel = 0.0
        self.tilt = 20
        
        self.img = pygame.Surface((34, 24), pygame.SRCALPHA) 
        self.img.fill((255, 255, 0))
        
        self.rect = self.img.get_rect(topleft=(self.x, self.y))
        self.alive = True
        self.score = 0
        self.visible = True

        self.pipes_passed = set()

        self.since_last_jump = self.JUMP_DELAY * 2

    def jump(self):
        if self.alive and self.since_last_jump > self.JUMP_DELAY:
            self.vel = -self.JUMP_POWER
            self.since_last_jump = 0

    def move(self):
        self.tick += 1
        self.since_last_jump += 1
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

    def draw(self):
        if self.visible:
            rotated_image = pygame.transform.rotate(self.img, self.tilt)
            
            new_rect = rotated_image.get_rect(center=self.rect.center)
            
            self.win.blit(rotated_image, new_rect.topleft)

class SavableBird(Bird):
    def __init__(self, win):
        super().__init__(win)
        self.move_history = []

    def jump(self):
        self.move_history.append(self.tick)
        super().jump()

    def get_move_history(self):
        return self.move_history

class ReplayBird(Bird):
    def __init__(self, win, move_history):
        super().__init__(win)
        self.move_history = move_history

    def move(self):
        if self.move_history and self.tick == self.move_history[0]:
            self.jump()
            self.move_history.pop(0)
        super().move()

class AIBird(SavableBird):
    def __init__(self, win, pipes, genome, config):
        super().__init__(win)
        self.genome = genome
        self.config = config
        self.model = neat.nn.FeedForwardNetwork.create(genome, config)
        self.genome.fitness = 0
        self.pipes = pipes

    def move(self):
        if self.alive:
            inputs = self.get_inputs()
            output = self.model.activate(inputs)
            if output[0] > 0.5:
                self.jump()
        super().move()

    def get_inputs(self):
        return [
            self.y,
            self.vel,
            self.since_last_jump,
            self.pipes[0].x - self.x,
            self.pipes[0].gap_pos - self.y,
            self.pipes[0].gap_pos + self.pipes[0].gap - self.y,
            self.pipes[0].velX,
            self.pipes[0].velY,
            len(self.pipes) > 1 and self.pipes[1].x - self.x or 1000,
            len(self.pipes) > 1 and self.pipes[1].gap_pos - self.y or 0,
            len(self.pipes) > 1 and self.pipes[1].gap_pos + self.pipes[1].gap - self.y or 0,
            len(self.pipes) > 1 and self.pipes[1].velX or 0,
            len(self.pipes) > 1 and self.pipes[1].velY or 0
        ]

    def add_fitness(self, amount):
        self.genome.fitness += amount