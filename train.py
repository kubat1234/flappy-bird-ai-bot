import pickle
import random
import neat
import pygame
from src.game import GameSettings, TrainGame
import sys
import argparse
    

def main():
    parser = argparse.ArgumentParser(description='Flappy Bird Game')
    
    args = parser.parse_args()

    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("Flappy Bird")

    config_file = 'config-neat.txt'

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    num_generations = 50

    def eval_genomes(genomes, config):
        for _ in range(5):
            game = TrainGame(screen, random.randint(0, 1000000), genomes, config=config, settings=GameSettings.from_file('difficulties/custom.yaml'))
            result = game.run()
            if result == 'quit':
                pygame.quit()
                sys.exit()

    winner = p.run(eval_genomes, num_generations)

    with open("best_bird.pkl", "wb") as f:
        pickle.dump(winner, f)
    print("\nNajlepszy genom zapisany!")

if __name__ == "__main__":
    main()