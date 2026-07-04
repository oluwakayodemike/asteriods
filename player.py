from shot import Shot
import pygame
import circleshape
import constants

class Player(circleshape.CircleShape):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, constants.PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cool_down_timer = 0
        
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def rotate(self, dt) -> None:
        self.rotation += constants.PLAYER_TURN_SPEED * dt

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        self.shot_cool_down_timer -= dt
        
        if keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_UP]:
            self.move(dt)
        if keys[pygame.K_DOWN]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
                self.shoot()

    def move(self, dt) -> None:
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * constants.PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self) -> None:
        if self.shot_cool_down_timer > 0:
            return

        self.shot_cool_down_timer = constants.PLAYER_SHOOT_COOLDOWN_SECONDS
        pos = self.position
        shot = Shot(pos.x, pos.y)
        unit_velocity = pygame.Vector2(0, 1)
        rotated_vector = unit_velocity.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * constants.PLAYER_SHOOT_SPEED

        shot.velocity += rotated_with_speed_vector