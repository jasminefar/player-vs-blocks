import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Avoid the Falling Objects!')

# Load images
player_img = pygame.image.load('player.png')
object_img = pygame.image.load('object.png')
background_img = pygame.image.load('background.png')

# Load sounds
background_music = pygame.mixer.music.load('background.mp3')
collision_sound = pygame.mixer.Sound('collision.wav')

# Play background music
pygame.mixer.music.play(-1)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

# Falling object class
class FallingObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = object_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(3, 8)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed = random.randint(3, 8)

# Initialize player and falling objects
player = Player()
falling_objects = pygame.sprite.Group()
for _ in range(10):
    falling_object = FallingObject()
    falling_objects.add(falling_object)

# Create sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(falling_objects)

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update sprites
    all_sprites.update()

    # Check for collisions
    if pygame.sprite.spritecollideany(player, falling_objects):
        collision_sound.play()
        running = False

    # Draw everything
    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)

    # Flip the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
