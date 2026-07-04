import pygame
import constants
from logger import log_state

def main():
    pygame.init()

    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))

    while True:
        for events in pygame.event.get():
            pass

        screen.fill("black")
        pygame.display.flip()
        
    # print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    # print(f"Screen width: {constants.SCREEN_WIDTH}")
    # print(f"Screen height: {constants.SCREEN_HEIGHT}")

if __name__ == "__main__":
    main()