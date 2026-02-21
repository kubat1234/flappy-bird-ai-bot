import random

import pygame
import os
from src.game import GameSettings, PlayableGame
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


    running = True
    while running:
        game = PlayableGame(screen, random.randint(0, 1000000), settings)
        result = game.run()

        if result == 'quit':
            break
        elif result == 'restart':
            continue
        elif result == 'save':
            if not os.path.exists('saves'):
                os.makedirs('saves')
            save_number = 1
            while os.path.exists(f'saves/save{save_number}.pkl'):
                save_number += 1
            
            filename = f'saves/save{save_number}.pkl'
            game.save_game(filename)
            print(f"Gra zapisana jako: {filename}")

    pygame.quit()

if __name__ == "__main__":
    main()