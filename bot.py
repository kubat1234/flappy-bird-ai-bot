import pickle
import random
import neat
import pygame
import os
from src.game import BotGame, GameSettings, PlayableGame, ReplayGame, TrainGame
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='Flappy Bird Game')
    parser.add_argument('difficulty', nargs='?', default='default', 
                        help='Poziom trudności')
    
    args = parser.parse_args()

    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("Flappy Bird")

        
    difficulty = args.difficulty
    
    settings_file = f'difficulties/{difficulty}.yaml'
    
    try:
        settings = GameSettings.from_file(settings_file)
        print(f"Wczytano ustawienia z: {settings_file}")
    except FileNotFoundError:
        settings = GameSettings()

    genome_file = "best_bird.pkl"
    config_file = 'config-neat.txt'

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    with open(genome_file, "rb") as f:
        genome = pickle.load(f)

    game = BotGame(screen, random.randint(0, 1000000), genome, config, settings=settings)
    game.run()

    pygame.quit()

if __name__ == "__main__":
    main()