import pygame
import os
from src.bird import Bird
from src.pipe import Pipe

WIN_WIDTH = 1000
WIN_HEIGHT = 800
BASE_HEIGHT = 20
FPS = 60

def draw_window(win, bird, pipes):
    win.fill((135, 206, 235))
    
    bird.draw(win)
    
    for pipe in pipes:
        pipe.draw(win)

    win.fill((150, 75, 0), (0, WIN_HEIGHT - BASE_HEIGHT, WIN_WIDTH, BASE_HEIGHT))
    
    pygame.display.flip()

def main():
    pygame.init()
    
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.DOUBLEBUF | pygame.HWSURFACE)
    pygame.display.set_caption("Flappy Bird")
    
    clock = pygame.time.Clock()
    
    bird = Bird(WIN_WIDTH // 4, WIN_HEIGHT // 2)

    PIPE_DISTANCE = 300
    pipes = [Pipe(WIN_WIDTH + Pipe.WIDTH, WIN_HEIGHT)]
    score = 0
    
    game_active = True
    run = True
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_SPACE:
                    if game_active:
                        bird.jump()
                    else:
                        main()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                bird.jump()
        
        if game_active or bird.y < WIN_HEIGHT - bird.rect.height - BASE_HEIGHT:
            bird.move()

        if bird.y + bird.rect.height >= WIN_HEIGHT - BASE_HEIGHT or bird.y < 0:
            game_active = False
        if game_active:
            rem = []
            add_pipe = False

            for pipe in pipes:
                pipe.move()
                
                if pipe.collide(bird):
                    game_active = False
                    
                if pipe.x + Pipe.WIDTH < 0:
                    rem.append(pipe)
                
                if pipes[-1].x < WIN_WIDTH - PIPE_DISTANCE:
                    add_pipe = True

            if add_pipe:
                score += 1
                pipes.append(Pipe(WIN_WIDTH + Pipe.WIDTH, WIN_HEIGHT))

            for r in rem:
                pipes.remove(r)

        draw_window(win, bird, pipes)

    pygame.quit()

if __name__ == "__main__":
    main()