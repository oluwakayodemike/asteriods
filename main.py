import pygame
import constants
import player
from logger import log_state

def main():
    pygame.init()
    clock = pygame.time.Clock()
    
    dt: float = 0.0
    x = constants.SCREEN_WIDTH / 2
    y = constants.SCREEN_HEIGHT / 2

    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    player1 = player.Player(x, y)

    while True:
        log_state()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        dt = clock.tick(60) / 1000
        
        screen.fill("black")
        player1.draw(screen)
        player1.update(dt)
        pygame.display.flip()

if __name__ == "__main__":
    main()