from logger import log_event
import random
import pygame
import circleshape
import constants

PRELOADED_ASTEROIDS = []
def get_random_asteroid_img():
    if not PRELOADED_ASTEROIDS:
        for i in range(1, 11):
            img = pygame.image.load(f"assets/ast{i}.png").convert_alpha()
            PRELOADED_ASTEROIDS.append(img)
            
    return random.choice(PRELOADED_ASTEROIDS)
        
class Asteroid(circleshape.CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

        base_ast = get_random_asteroid_img()

        # using smoothscale to try to maintain high res while shrinking
        self.asteroid = pygame.transform.smoothscale(base_ast, (self.radius * 2, self.radius *2))
        self.mask = pygame.mask.from_surface(self.asteroid)

    def draw(self, screen: pygame.Surface) -> None:
        # pygame.draw.circle(screen, "white", self.position, self.radius, constants.LINE_WIDTH)
        centered_rect = self.asteroid.get_rect(center=self.position)
        screen.blit(self.asteroid, centered_rect)

    def update(self, dt) -> None:
        self.position += self.velocity * dt

    def split(self) -> None:
        self.kill()
        if self.radius <= constants.ASTEROID_MIN_RADIUS:
            return
            
        log_event("asteroid_split")
        angle = random.uniform(20, 50)
        vec1 = self.velocity.rotate(angle)
        vec2 = self.velocity.rotate(-angle)
        new_rad = self.radius - constants.ASTEROID_MIN_RADIUS

        pos = self.position

        new_ast1  = Asteroid(pos.x, pos.y, new_rad)
        new_ast2 = Asteroid(pos.x, pos.y, new_rad)

        new_ast1.velocity = vec1 * 1.2
        new_ast2.velocity = vec2 * 1.2