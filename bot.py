import pickle
import random
import neat
import pygame
import os
from src.game import BotGame, GameSettings, BenchmarkGame
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='Flappy Bird Game')
    parser.add_argument('file', help='Plik z zapisanym genomem')
    parser.add_argument('--difficulty', '-d', nargs='?', default='easy', 
                        help='Poziom trudności')
    parser.add_argument('--benchmark', '-b',nargs='?', type=int, default=None, const=1, help='Uruchomienie w trybie benchmarku (uruchomi grę 10 razy i poda średni wynik)')
    parser.add_argument('--fps', '-f', type=int, default=60, help='Ustawienie FPS (domyślnie 60 FPS)')
    
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

    genome_file = args.file
    config_file = 'config-neat.txt'

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    with open(genome_file, "rb") as f:
        genome = pickle.load(f)

    if args.benchmark is not None:
        total_score = 0
        runs = args.benchmark
        for _ in range(runs):
            game = BenchmarkGame(screen, random.randint(0, 1000000), genome, config, settings=settings)
            score = game.run()
            total_score += score
            print(f"Run {_ + 1}: Score = {score}")
        average_score = total_score / runs
        print(f"Average Score over {runs} runs: {average_score}")
        pygame.quit()
    else:
        game = BotGame(screen, random.randint(0, 1000000), genome, config, settings=settings)
        game.FPS = args.fps
        game.run()

    pygame.quit()

if __name__ == "__main__":
    main()