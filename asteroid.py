from logger import log_event
import random
import pygame
import circleshape
import constants

class Asteroid(circleshape.CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", self.position, self.radius, constants.LINE_WIDTH)

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