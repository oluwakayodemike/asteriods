import os
import sys
import pygame
import constants
import player
import asteroid
import asteroidfield
import shot
from logger import log_state, log_event

def main():
    BASE_DIR = os.path.dirname(__file__)
    
    pygame.init()
    clock = pygame.time.Clock()
    
    dt: float = 0.0
    x = constants.SCREEN_WIDTH / 2
    y = constants.SCREEN_HEIGHT / 2
    score = 0

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

    try:
        # .convert creates copy that draws more quickly than .convert_alpha [trans]
        bg_image = pygame.image.load(os.path.join(BASE_DIR, "assets", "space.jpg")).convert()

        background = pygame.transform.scale(bg_image, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    except pygame.error as e:
        print("unable to load image")
        sys.exit()
    
    font = pygame.font.SysFont("Arial", 28, italic=True)
    text_surface = font.render("Welcome to Asteroids!", True, "green")

    header_rect = text_surface.get_rect()
    header_rect.center = (x, 20)
    
    while True:
        log_state()
        score_board = font.render(f"Score: {score}", False, "green")
        score_rect = score_board.get_rect()
        score_rect.center = (100, 500)
        # score_rect = score_board.get_rect(center=(100, 500))
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
                
        dt = clock.tick(60) / 1000

        updatable.update(dt)
        
        for ast in asteroids:
            if player1.collides_with(ast):
                if player1.health > 0:
                    player1.position = pygame.Vector2(x, y)

                    # kill all momentum and reset ship direction
                    player1.velocity = pygame.Vector2(0, 0)
                    player1.rotation = 0
                    
                    player1.health -= 1
                    player1.invisible_timer = constants.PLAYER_INVISIBILITY_WINDOW
                else:
                    log_event("player_hit")
                    print("Game over!")
                    print(f"your score was {score}")
                    sys.exit()

        for ast in asteroids:
            for e_shot in shots:
                if ast.collides_with(e_shot):
                    log_event("asteroid_shot")
                    e_shot.kill()
                    ast.split()
                    score += 5
        
        screen.blit(background, (0, 0))
        for drawables in drawable:
            drawables.draw(screen)
            
        screen.blit(text_surface, header_rect)
        screen.blit(score_board, score_rect)
        pygame.display.flip()

if __name__ == "__main__":
    main()