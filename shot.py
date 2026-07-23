import pygame
import constants
import circleshape

class Shot(circleshape.CircleShape):
    def __init__(self, x: float, y: float, rotation) -> None:
        super().__init__(x, y, constants.SHOT_RADIUS)
        self.laser = pygame.image.load("assets/laser.png").convert_alpha()

    def draw(self, screen: pygame.Surface) -> None:
        # pygame.draw.circle(screen, "white", self.position, self.radius, constants.LINE_WIDTH)
        centered_rect = self.laser.get_rect(center=self.position)
        screen.blit(self.laser, centered_rect)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt