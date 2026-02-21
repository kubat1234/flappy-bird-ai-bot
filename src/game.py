import pygame
import pickle
import random
import yaml
import neat

from src.bird import AIBird, SavableBird
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
    
    @staticmethod
    def get_random_settings(diff):
        diff = min(1, diff)
        def lerp(a, b):
            return int(a + diff * (b - a))
        settings = GameSettings()
        settings.DISTANCE_MIN = random.randint(lerp(400, 200), lerp(500, 250))
        settings.DISTANCE_MAX = random.randint(settings.DISTANCE_MIN, lerp(600, 300))
        settings.GAP_MIN = random.randint(lerp(400, 250), lerp(450, 300))
        settings.GAP_MAX = random.randint(settings.GAP_MIN, lerp(500, 350))
        settings.VEL_X = random.uniform(lerp(3, 8), lerp(5, 12))
        settings.VEL_Y = random.uniform(lerp(1, 5), lerp(3, 7))
        return settings

class Game:
    BASE_HEIGHT = 20
    FPS = 60

    def __init__(self, screen, seed, settings = GameSettings()):
        self.win = screen

        self.clock = pygame.time.Clock()

        self.settings = settings

        self.seed = seed
        self.rng = random.Random(seed)

        self.score = 0

        self.pipes = [Pipe(self.win.get_width() + Pipe.WIDTH, self.win.get_height(), seed = self.rng.randint(0, 1000000), velX=self.settings.VEL_X, velY=self.settings.VEL_Y, gap_min=self.settings.GAP_MIN, gap_max=self.settings.GAP_MAX)]

        self.passed_pipes = []


    def draw_window(self):
        self.win.fill((135, 206, 235))
    
        for pipe in self.pipes:
            pipe.draw(self.win)

        for pipe in self.passed_pipes:
            pipe.draw(self.win)

        for bird in self.birds:
            bird.draw()
        
        self.win.fill((150, 75, 0), (0, self.win.get_height() - self.BASE_HEIGHT, self.win.get_width(), self.BASE_HEIGHT))

        font = pygame.font.Font(None, 70)
        score_text = font.render(str(self.score), True, (0, 0, 0))
        self.win.blit(score_text, (10, 10))
        
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
                if not bird.alive:
                    continue
                if bird.y < self.win.get_height() - bird.rect.height - self.BASE_HEIGHT:
                    bird.move()

                if bird.y < 0 or bird.y + bird.rect.height >= self.win.get_height() - self.BASE_HEIGHT:
                    bird.die()
                    birds_alive -= 1

                if self.pipes[0].collide(bird):
                    bird.die()
                    birds_alive -= 1

            if birds_alive > 0:
                for pipe in self.pipes:
                    pipe.move()
                for pipe in self.passed_pipes:
                    pipe.move()

                if self.pipes[0].x + self.pipes[0].WIDTH < self.birds[0].x:
                    self.passed_pipes.append(self.pipes.pop(0))
                    self.score += 1

                if self.pipes[-1].x < self.win.get_width() - pipe_distance:
                    self.pipes.append(Pipe(self.win.get_width() + Pipe.WIDTH, self.win.get_height(), seed = self.rng.randint(0, 1000000), velX=self.settings.VEL_X, velY=self.settings.VEL_Y, gap_min=self.settings.GAP_MIN, gap_max=self.settings.GAP_MAX))
                    pipe_distance = self.rng.randint(self.settings.DISTANCE_MIN, self.settings.DISTANCE_MAX)

                if self.passed_pipes and self.passed_pipes[0].x + self.passed_pipes[0].WIDTH < 0:
                    self.passed_pipes.pop(0)

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
    def __init__(self, screen, seed, settings=None):
        super().__init__(screen, seed=seed, settings=settings)
        self.birds = [SavableBird(screen)]

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
    def __init__(self, win, filename):
        with open(filename, 'rb') as f:
            data = pickle.load(f)

        super().__init__(win, seed=data['seed'], settings=data['settings'])

        self.birds = [ReplayBird(win, move_history) for move_history in data['birds']]

class TrainGame(Game):
    def __init__(self, win, seed, genomes, config, settings=None):
        super().__init__(win, seed=seed, settings=settings)
        
        self.birds = []

        for genome_id, genome in genomes:
            self.birds.append(AIBird(win, self.pipes, genome, config))

    def run(self):
        birds_alive = len(self.birds)
        pipe_distance = self.settings.DISTANCE_MAX
        
        while birds_alive > 0:
            # self.clock.tick(self.FPS * 20)
            # self.clock.tick(0)

            for event in pygame.event.get():
                result = self.handle_input(event)
                if result != None:
                    return result

            for bird in self.birds:
                if not bird.alive:
                    continue
                
                # bird.add_fitness(0.1)
                bird.move()

                if bird.alive and (bird.y < 0 or bird.y + bird.rect.height >= self.win.get_height() - self.BASE_HEIGHT):
                    bird.die()
                    bird.visible = False
                    birds_alive -= 1
                    bird.add_fitness(-30)

                if self.pipes[0].collide(bird):
                    bird.die()
                    bird.visible = False
                    bird.add_fitness(-10)
                    birds_alive -= 1

            for pipe in self.pipes:
                pipe.move()
            for pipe in self.passed_pipes:
                pipe.move()

            if self.pipes[0].x + self.pipes[0].WIDTH < self.birds[0].x:
                self.passed_pipes.append(self.pipes.pop(0))
                self.score += 1
                for bird in self.birds:
                    if bird.alive:
                        bird.score += 1
                        bird.add_fitness(5)

            if self.pipes[-1].x < self.win.get_width() - pipe_distance:
                self.pipes.append(Pipe(self.win.get_width() + Pipe.WIDTH, self.win.get_height(), seed = self.rng.randint(0, 1000000), velX=self.settings.VEL_X, velY=self.settings.VEL_Y, gap_min=self.settings.GAP_MIN, gap_max=self.settings.GAP_MAX))
                pipe_distance = self.rng.randint(self.settings.DISTANCE_MIN, self.settings.DISTANCE_MAX)

            if self.passed_pipes and self.passed_pipes[0].x + self.passed_pipes[0].WIDTH < 0:
                self.passed_pipes.pop(0)

            # self.draw_window()

class BotGame(Game):
    def __init__(self, win, seed, genome, config, settings=None):
        super().__init__(win, seed=seed, settings=settings)
        
        self.birds = [AIBird(win, self.pipes, genome, config)]

    def die(self):
        super().die()
        print("Genom zginął na wyniku:", self.score)

    def run(self):
        birds_alive = len(self.birds)
        pipe_distance = self.settings.DISTANCE_MAX
        
        while birds_alive > 0:
            self.clock.tick(self.FPS)
            # self.clock.tick(0)

            for event in pygame.event.get():
                result = self.handle_input(event)
                if result != None:
                    return result

            for bird in self.birds:
                if not bird.alive:
                    continue
                
                bird.move()

                if bird.alive and (bird.y < 0 or bird.y + bird.rect.height >= self.win.get_height() - self.BASE_HEIGHT):
                    bird.die()
                    birds_alive -= 1

                if self.pipes[0].collide(bird):
                    bird.die()
                    birds_alive -= 1

            for pipe in self.pipes:
                pipe.move()
            for pipe in self.passed_pipes:
                pipe.move()

            if self.pipes[0].x + self.pipes[0].WIDTH < self.birds[0].x:
                self.passed_pipes.append(self.pipes.pop(0))
                self.score += 1
                for bird in self.birds:
                    if bird.alive:
                        bird.score += 1

            if self.pipes[-1].x < self.win.get_width() - pipe_distance:
                self.pipes.append(Pipe(self.win.get_width() + Pipe.WIDTH, self.win.get_height(), seed = self.rng.randint(0, 1000000), velX=self.settings.VEL_X, velY=self.settings.VEL_Y, gap_min=self.settings.GAP_MIN, gap_max=self.settings.GAP_MAX))
                pipe_distance = self.rng.randint(self.settings.DISTANCE_MIN, self.settings.DISTANCE_MAX)

            if self.passed_pipes and self.passed_pipes[0].x + self.passed_pipes[0].WIDTH < 0:
                self.passed_pipes.pop(0)

            self.draw_window()
        print("Genom zginął na wynikuu:", self.score)

        