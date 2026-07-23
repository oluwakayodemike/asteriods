import pygame
import constants
import circleshape

class Shot(circleshape.CircleShape):
    def __init__(self, x: float, y: float, rotation) -> None:
        super().__init__(x, y, constants.SHOT_RADIUS)
        self.laser = pygame.image.load("assets/laser.png").convert_alpha()
        self.rotation = rotation

    def draw(self, screen: pygame.Surface) -> None:
        # pygame.draw.circle(screen, "white", self.position, self.radius, constants.LINE_WIDTH)
        rotated_image = pygame.transform.rotate(self.laser, (-self.rotation + 270))
        centered_rect = rotated_image.get_rect(center=self.position)
        screen.blit(rotated_image, centered_rect)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt