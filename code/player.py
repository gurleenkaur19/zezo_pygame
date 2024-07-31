from settings import *
from os.path import join
from sprites import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.hitbox_rect = self.rect.inflate(-60, 0)

        # movement
        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites
        
    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        # Move horizontally and check for collisions
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        
        # Move vertically and check for collisions
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        
        # Update the rect position
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:  # Moving right
                        self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0:  # Moving left
                        self.hitbox_rect.left = sprite.rect.right
                    self.direction.x = 0  # Stop horizontal movement
                elif direction == 'vertical':
                    if self.direction.y > 0:  # Moving down
                        self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0:  # Moving up
                        self.hitbox_rect.top = sprite.rect.bottom
                    self.direction.y = 0  # Stop vertical movement

        # Ensure the player remains within the visible area
        # self.hitbox_rect.clamp_ip(pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))

    def update(self, dt):
        self.input()
        self.move(dt)