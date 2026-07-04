import sys
import pygame
import constants
import player
import asteroid
import asteroidfield
import shot
from logger import log_state, log_event

def main():
    pygame.init()
    clock = pygame.time.Clock()
    
    dt: float = 0.0
    x = constants.SCREEN_WIDTH / 2
    y = constants.SCREEN_HEIGHT / 2

    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    
    # groups
    asteroids = pygame.sprite.Group()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    player.Player.containers = (updatable, drawable)
    asteroid.Asteroid.containers = (asteroids, updatable, drawable)
    asteroidfield.AsteroidField.containers = updatable
    shot.Shot.containers = (shots, drawable, updatable)

    asteroidfield1 = asteroidfield.AsteroidField()
    player1 = player.Player(x, y)
    while True:
        log_state()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
                
        dt = clock.tick(60) / 1000

        updatable.update(dt)
        
        for ast in asteroids:
            if ast.collides_with(player1):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

        for ast in asteroids:
            for e_shot in shots:
                if ast.collides_with(e_shot):
                    log_event("asteroid_shot")
                    pygame.sprite.Sprite.kill(e_shot)
                    pygame.sprite.Sprite.kill(ast)
        
        screen.fill("black")        
        for drawables in drawable:
            drawables.draw(screen)
            
        pygame.display.flip()

if __name__ == "__main__":
    main()