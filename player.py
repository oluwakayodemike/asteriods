from shot import Shot
import pygame
import circleshape
import constants

class Player(circleshape.CircleShape):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, constants.PLAYER_RADIUS)
        self.rotation = 0
        self.health = 3
        self.invisible_timer = 0
        
        self.shot_cool_down_timer = 0
        self.spaceship = pygame.image.load("assets/spaceship.pod.1.png").convert_alpha()

        # fit spaceship into circle 
        self.spaceship = pygame.transform.scale(self.spaceship, (self.radius * 3, self.radius * 3))
        
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface) -> None:
        if self.invisible_timer > 0:
            # flash spaceship on and off every 100ms
            if (pygame.time.get_ticks() // 100) % 2 == 0:
               return # skip drawing this frame  
        
        image = self.spaceship
        
        # since spaceship image points up but our game logic treats Vector2(0, 1) [down] as forward, we must add a 180deg to rotation  
        rotated = pygame.transform.rotate(image, (-self.rotation + 180))
        centered_rect = rotated.get_rect(center=(self.position))
        screen.blit(rotated, centered_rect)
        
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

        if self.invisible_timer > 0:
            self.invisible_timer -= dt
            if self.invisible_timer < 0:
                self.invisible_timer = 0

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

    def collides_with(self, other) -> bool:
        # collision shield
        if self.invisible_timer > 0:
            return False
            
        if self.position.distance_to(other.position) > (self.radius * 2 + other.radius):
            return False

        # generating mask from the ship's current rotated image
        rotated_image = pygame.transform.rotate(self.spaceship, (-self.rotation + 180))
        ship_rect = rotated_image.get_rect(center=self.position)
        ship_mask = pygame.mask.from_surface(rotated_image)

        # circular mask matching the asteroid's shape/size
        circle_surface = pygame.Surface((other.radius * 2, other.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(circle_surface, (255, 255, 255), (other.radius, other.radius), other.radius)
        asteroid_mask = pygame.mask.from_surface(circle_surface)

        # distance between top-left corner of both objects
        offset_x = int((other.position.x - other.radius) - ship_rect.x)
        offset_y = int((other.position.y - other.radius) - ship_rect.y)

        # overlap() returns the first point of contact or None if they're missed.
        return ship_mask.overlap(asteroid_mask, (offset_x, offset_y)) is not None
        