import pygame
from src.game import ReplayGame
import argparse

def main():
    parser = argparse.ArgumentParser(description='Flappy Bird Game')
    parser.add_argument('file', nargs='?', default=None, help='Plik replay do odtworzenia')
    
    args = parser.parse_args()

    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("Flappy Bird")

    replay_file = args.file

    game = ReplayGame(screen, replay_file)
    game.run()

    pygame.quit()

if __name__ == "__main__":
    main()