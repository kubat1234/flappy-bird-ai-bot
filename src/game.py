import pygame
import pickle
import random
import yaml

from src.bird import SavableBird
from src.bird import ReplayBird
from src.pipe import Pipe

class GameSettings:
    DISTANCE_MIN = 400
    DISTANCE_MAX = 400
    GAP_MIN = 400
    GAP_MAX = 400
    VEL_X = 4
    VEL_Y = 2

    @staticmethod
    def from_file(filename):
        """Wczytuje ustawienia z pliku YAML"""
        with open(filename, 'r') as f:
            data = yaml.safe_load(f)
        
        settings = GameSettings()
        for key, value in data.items():
            setattr(settings, key, value)
        
        return settings

class Game:
    BASE_HEIGHT = 20
    FPS = 60

    def __init__(self, screen, seed=random.randint(0, 1000000), settings = GameSettings()):
        self.win = screen

        self.clock = pygame.time.Clock()

        self.settings = settings
        self.PIPE_VELX = settings.VEL_X
        self.PIPE_VELY = settings.VEL_Y

        self.seed = seed
        self.rng = random.Random(seed)

        self.pipes = [Pipe(self.win.get_width() + Pipe.WIDTH, self.win.get_height(), seed = self.rng.randint(0, 1000000), velX=self.PIPE_VELX, velY=self.PIPE_VELY, gap_min=self.settings.GAP_MIN, gap_max=self.settings.GAP_MAX)]
        self.score = 0


    def draw_window(self):
        self.win.fill((135, 206, 235))
    
        for pipe in self.pipes:
            pipe.draw(self.win)

        for bird in self.birds:
            bird.draw(self.win)
        
        self.win.fill((150, 75, 0), (0, self.win.get_height() - self.BASE_HEIGHT, self.win.get_width(), self.BASE_HEIGHT))
        
        pygame.display.flip()

    def handle_input(self, event):
        if event.type == pygame.QUIT:
                    return 'quit'
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 'quit'

    def run(self):
        birds_alive = len(self.birds)
        pipe_distance = self.settings.DISTANCE_MAX
        while True:
            self.clock.tick(self.FPS)
            
            for event in pygame.event.get():
                result = self.handle_input(event)
                if result != None:
                    return result

            for bird in self.birds:
                if bird.alive or bird.y < self.win.get_height() - bird.rect.height - self.BASE_HEIGHT:
                    bird.move()

                if bird.y < 0 or bird.y + bird.rect.height >= self.win.get_height() - self.BASE_HEIGHT:
                    bird.die()
                    birds_alive -= 1

            if birds_alive > 0:
                rem = []
                add_pipe = False

                for pipe in self.pipes:
                    pipe.move()
                    
                    for bird in self.birds:
                        if pipe.collide(bird):
                            bird.die()
                            birds_alive -= 1
                        
                    if pipe.x + Pipe.WIDTH < 0:
                        rem.append(pipe)
                    
                    if self.pipes[-1].x < self.win.get_width() - pipe_distance:
                        add_pipe = True
                        pipe_distance = self.rng.randint(self.settings.DISTANCE_MIN, self.settings.DISTANCE_MAX)

                if add_pipe:
                    self.score += 1
                    self.pipes.append(Pipe(self.win.get_width() + Pipe.WIDTH, self.win.get_height(), seed = self.rng.randint(0, 1000000), velX=self.PIPE_VELX, velY=self.PIPE_VELY, gap_min=self.settings.GAP_MIN, gap_max=self.settings.GAP_MAX))

                for r in rem:
                    self.pipes.remove(r)

            self.draw_window()

    
    def save_game(self, filename):
        with open(filename, 'wb') as f:
            data = {
                'birds': [bird.get_move_history() for bird in self.birds],
                'seed': self.seed,
                'settings': self.settings
            }
            pickle.dump(data, f)

class PlayableGame(Game):
    def __init__(self, screen, settings=None):
        super().__init__(screen, settings=settings)
        self.birds = [SavableBird(self.win.get_width() // 4, self.win.get_height() // 3)]

    def handle_input(self, event):
        if event.type == pygame.QUIT:
                    return 'quit'
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 'quit'
            if event.key == pygame.K_SPACE:
                if self.birds[0].alive:
                    self.birds[0].jump()
                else:
                    return 'restart'
            if event.key == pygame.K_s:
                if not self.birds[0].alive:
                    return 'save'
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.birds[0].alive:
                self.birds[0].jump()
            else:
                return 'restart'

class ReplayGame(Game):
    def __init__(self, screen, filename):
        with open(filename, 'rb') as f:
            data = pickle.load(f)

        super().__init__(screen, seed=data['seed'], settings=data['settings'])

        self.birds = [ReplayBird(self.win.get_width() // 4, self.win.get_height() // 3, move_history) for move_history in data['birds']]