from logger import log_event
import random
import pygame
import circleshape
import constants

PRELOADED_ASTEROIDS = []
def get_random_asteroid_img():
    if not PRELOADED_ASTEROIDS:
        for i in range(1, 11):
            try: 
                img = pygame.image.load(f"assets/ast{i}.png").convert_alpha()

                # getting bounding box for non-transparent pixels and crop out empty space using it.
                # then we save a copy into the mem.
                bounding_box = img.get_bounding_rect()
                cropped_img = img.subsurface(bounding_box).copy()
                
                PRELOADED_ASTEROIDS.append(cropped_img)
            except FileNotFoundError:
                print(f"could not find assets/ast{i}.png...")
            
    return random.choice(PRELOADED_ASTEROIDS)
        
class Asteroid(circleshape.CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

        base_ast = get_random_asteroid_img()

        # smoothscale req. ints 
        size = int(self.radius * 2)

        # using smoothscale to try to maintain high res while shrinking
        self.asteroid = pygame.transform.smoothscale(base_ast, (size, size))
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