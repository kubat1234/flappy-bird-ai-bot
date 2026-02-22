import os
import pickle
import random
import neat
import pygame
from src.game import GameSettings, TrainGame
import sys
import argparse

generation = 0

def main():
    parser = argparse.ArgumentParser(description='Flappy Bird Game')
    parser.add_argument('--difficulty', '-d', nargs='?', default='easy', 
                        help='Poziom trudności')
    parser.add_argument('--save', '-s', action='store_true', help='Zapisz najlepszego genom po zakończeniu treningu')
    
    args = parser.parse_args()

    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("Flappy Bird")

    config_file = 'config-neat.txt'

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)
    
    difficulty = args.difficulty
    
    settings_file = f'difficulties/{difficulty}.yaml'
    
    try:
        settings = GameSettings.from_file(settings_file)
        print(f"Wczytano ustawienia z: {settings_file}")
    except FileNotFoundError:
        settings = GameSettings()

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    num_generations = 50

    if not os.path.exists('saves'):
        os.makedirs('saves')

    num = 1
    save_folder = 'saves/training_' + difficulty
    while os.path.exists(f'{save_folder}_{num}'):
        num += 1
    
    save_folder = f'{save_folder}_{num}'

    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    if not os.path.exists('bots'):
        os.makedirs('bots')

    bot_file = f'bots/bot_{difficulty}_{num}.pkl'

    generation = 0

    def eval_genomes(genomes, config):
        global generation
        generation += 1
        # game = TrainGame(screen, random.randint(0, 999999), genomes, config, settings=GameSettings.from_file(f'difficulties/custom.yaml'))
        for genome_id, genome in genomes:
            genome.fitness = 0

        game = TrainGame(screen, random.randint(0, 999999), genomes, config, settings=settings)
        result = game.run()
        if args.save:
            save_file = f'{save_folder}/game_{generation}.pkl'
            game.save_game(save_file)
        if result == 'quit':
            pygame.quit()
            sys.exit()

    winner = p.run(eval_genomes, num_generations)

    with open(bot_file, "wb") as f:
        pickle.dump(winner, f)
    print(f"\nNajlepszy genom zapisany jako: {bot_file}")

if __name__ == "__main__":
    main()