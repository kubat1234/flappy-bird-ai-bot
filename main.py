import pygame
import os
from src.bird import Bird
from src.pipe import Pipe

WIN_WIDTH = 1000
WIN_HEIGHT = 800
FPS = 60

def draw_window(win, bird, pipes):
    win.fill((135, 206, 235))
    
    bird.draw(win)
    
    for pipe in pipes:
        pipe.draw(win)
    
    pygame.display.flip()

def main():
    pygame.init()
    
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.DOUBLEBUF | pygame.HWSURFACE)
    pygame.display.set_caption("Flappy Bird")
    
    clock = pygame.time.Clock()
    
    bird = Bird(WIN_WIDTH // 4, WIN_HEIGHT // 2)

    PIPE_DISTANCE = 300
    pipes = [Pipe(WIN_WIDTH + Pipe.WIDTH)]
    score = 0
    
    run = True
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
                if event.key == pygame.K_ESCAPE:
                    run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                bird.jump()

        bird.move()

        if bird.y + bird.rect.height >= WIN_HEIGHT or bird.y < 0:
            print("BUM! Koniec gry.")
            run = False

        rem = []
        add_pipe = False

        for pipe in pipes:
            pipe.move()
            
            if pipe.collide(bird):
                print("BUM! Koniec gry.")
                run = False
                
            if pipe.x + Pipe.WIDTH < 0:
                rem.append(pipe)
            
            if pipes[-1].x < WIN_WIDTH - PIPE_DISTANCE:
                add_pipe = True

        if add_pipe:
            score += 1
            pipes.append(Pipe(WIN_WIDTH + Pipe.WIDTH))

        for r in rem:
            pipes.remove(r)

        draw_window(win, bird, pipes)

    pygame.quit()

if __name__ == "__main__":
    main()