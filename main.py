import pickle
import pygame
import os
from src.game import GameSettings, PlayableGame, ReplayGame
import sys
import argparse

def show_menu(screen):
    clock = pygame.time.Clock()
    font_large = pygame.font.Font(None, 74)
    font_small = pygame.font.Font(None, 36)
    
    while True:
        screen.fill((135, 206, 235))  # Niebieskie tło
        
        title = font_large.render("Flappy Bird", True, (255, 255, 255))
        title_rect = title.get_rect(center=(screen.get_width() // 2, 150))
        screen.blit(title, title_rect)
        
        start_text = font_small.render("Naciśnij SPACJĘ aby zacząć", True, (255, 255, 255))
        start_rect = start_text.get_rect(center=(screen.get_width() // 2, 300))
        screen.blit(start_text, start_rect)
        
        quit_text = font_small.render("Naciśnij ESC aby wyjść", True, (255, 255, 255))
        quit_rect = quit_text.get_rect(center=(screen.get_width() // 2, 350))
        screen.blit(quit_text, quit_rect)
        
        pygame.display.flip()
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True

def main():
    parser = argparse.ArgumentParser(description='Flappy Bird Game')
    parser.add_argument('difficulty', nargs='?', default='default', 
                        help='Poziom trudności')
    parser.add_argument('-r', '--replay', type=str, 
                        help='Odtwórz zapisaną grę z pliku')
    
    args = parser.parse_args()

    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("Flappy Bird")

    if args.replay:
        replay_file = args.replay
        replay_mode = True
        print(f"Tryb replay: {replay_file}")
    else:
        replay_mode = False
        
        difficulty = args.difficulty
        
        settings_file = f'difficulties/{difficulty}.yaml'
        
        try:
            settings = GameSettings.from_file(settings_file)
            print(f"Wczytano ustawienia z: {settings_file}")
        except FileNotFoundError:
            settings = GameSettings()

    running = True
    while running:
        if not replay_mode and not show_menu(screen):
            break
        if replay_mode:
            game = ReplayGame(screen, replay_file)
        else:
            game = PlayableGame(screen, settings=settings)
        result = game.run()

        if result == 'quit':
            break
        elif result == 'restart':
            continue
        elif result == 'save' and not replay_mode:
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