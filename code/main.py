from settings import *
from player import Player
from sprites import *
from menu import Menu  
from random import randint, choice
from pytmx.util_pygame import load_pygame
from groups import AllSprites

class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Survivor")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "menu" 
        
        #Menu instance
        self.menu = Menu()

        # audio
        self.shoot_sound = pygame.mixer.Sound(join('audio', 'shoot.wav'))
        self.shoot_sound.set_volume(0.4)
        self.impact_sound = pygame.mixer.Sound(join('audio', 'impact.ogg'))
        self.music = pygame.mixer.Sound(join('audio', 'music.wav'))
        self.music.set_volume(0.3)
        self.music.play(loops=-1)

        # setup
        self.load_images()
        self.reset_game()

        # Game over menu
        self.selected_game_over_option = 0

    def load_images(self):
        self.bullet_surf = pygame.image.load(join('images', 'gun', 'bullet.png')).convert_alpha()

        folders = list(walk(join('images', 'enemies')))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            for folder_path, _, file_names in walk(join('images', 'enemies', folder)):
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0])):
                    full_path = join(folder_path, file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surf)

    def reset_game(self):
        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # gun timer
        self.shoot_time = 0
        self.can_shoot = True
        self.gun_cooldown = 100

        # enemy timer
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 300)
        self.spawn_positions = []

        # enemies killed counter
        self.enemies_killed = 0

        # levels
        self.level = 1
        self.level_thresholds = [15, 30, 45]  # Number of enemies killed to reach next level
        self.level_gun_cooldowns = [100, 500, 1000, 1500]  # Gun cooldown times for each level

        self.setup()

    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.shoot_sound.play()
            pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True

    def setup(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))

        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
                self.gun = Gun(self.player, self.all_sprites)
            else:
                self.spawn_positions.append((obj.x, obj.y))

    def bullet_collision(self):
        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                collision_sprites = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
                if collision_sprites:
                    self.impact_sound.play()
                    for sprite in collision_sprites:
                        sprite.destroy()
                        self.enemies_killed += 1  # Increment the counter
                        self.update_level()  # Check if level needs to be updated
                    bullet.kill()

    def player_collision(self):
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.state = "game_over" 

    def draw_game_over(self):
        self.display_surface.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, (255, 0, 0))
        self.display_surface.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - text.get_height() // 2 - 100))

        font = pygame.font.Font(None, 50)
        start_again_text = font.render("Start Again", True, (255, 255, 255) if self.selected_game_over_option == 0 else (100, 100, 100))
        exit_text = font.render("Exit", True, (255, 255, 255) if self.selected_game_over_option == 1 else (100, 100, 100))

        start_again_rect = start_again_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        exit_rect = exit_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))

        self.display_surface.blit(start_again_text, start_again_rect)
        self.display_surface.blit(exit_text, exit_rect)

        # Display the number of enemies killed
        enemies_killed_text = font.render(f"Enemies Killed: {self.enemies_killed}", True, (255, 255, 255))
        enemies_killed_rect = enemies_killed_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.display_surface.blit(enemies_killed_text, enemies_killed_rect)

        # Display the current level
        level_text = font.render(f"Level: {self.level}", True, (255, 255, 255))
        level_text_rect = level_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.display_surface.blit(level_text, level_text_rect)

        pygame.display.update()

        return start_again_rect, exit_rect

    def handle_game_over_input(self, start_again_rect, exit_rect):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_game_over_option = (self.selected_game_over_option - 1) % 2
                elif event.key == pygame.K_DOWN:
                    self.selected_game_over_option = (self.selected_game_over_option + 1) % 2
                elif event.key == pygame.K_RETURN:
                    if self.selected_game_over_option == 0:
                        self.reset_game()  # Restart the game
                        self.state = "playing"
                    elif self.selected_game_over_option == 1:
                        self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_again_rect.collidepoint(mouse_pos):
                    self.reset_game()  # Restart the game
                    self.state = "playing"
                elif exit_rect.collidepoint(mouse_pos):
                    self.running = False

    def draw_top_bar(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f"Enemies Killed: {self.enemies_killed}", True, (255, 255, 255))
        text_rect = text.get_rect(topleft=(10, 10))
        
        # Draw black rectangle as background
        pygame.draw.rect(self.display_surface, (0, 0, 0), text_rect)
        
        # Draw the text on top of the black rectangle
        self.display_surface.blit(text, text_rect)

        # Draw the level on the top right corner
        level_text = font.render(f"Level: {self.level}", True, (255, 255, 255))
        level_text_rect = level_text.get_rect(topright=(WINDOW_WIDTH - 10, 10))
        pygame.draw.rect(self.display_surface, (0, 0, 0), level_text_rect)
        self.display_surface.blit(level_text, level_text_rect)

    def draw_reload_time(self):
        font = pygame.font.Font(None, 36)
        reload_text = font.render(f"Reload Time: {self.gun_cooldown} ms", True, (255, 255, 255))
        reload_text_rect = reload_text.get_rect(midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 10))
        pygame.draw.rect(self.display_surface, (0, 0, 0), reload_text_rect)
        self.display_surface.blit(reload_text, reload_text_rect)

    def update_level(self):
        for i, threshold in enumerate(self.level_thresholds):
            if self.enemies_killed >= threshold:
                self.level = i + 2
                self.gun_cooldown = self.level_gun_cooldowns[i + 1]
            else:
                break

    def run(self):
        while self.running:
            # data time
            dt = self.clock.tick() / 1000

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if self.state == "menu":
                    selection = self.menu.navigate(event)
                    if selection == 0:
                        self.state = "playing"
                    elif selection == 1:
                        pass  # Handle Options
                    elif selection == 2:
                        self.running = False

                if event.type == self.enemy_event and self.state == "playing":
                    Enemy(choice(self.spawn_positions), choice(list(self.enemy_frames.values())),
                          (self.all_sprites, self.enemy_sprites), self.player, self.collision_sprites)

            # Update based on state
            if self.state == "menu":
                self.menu.draw_menu(self.display_surface)
            elif self.state == "playing":
                self.gun_timer()
                self.input()
                self.all_sprites.update(dt)
                self.bullet_collision()
                self.player_collision()

                # draw
                self.display_surface.fill(('black'))
                self.all_sprites.draw(self.player.rect.center)
                self.draw_top_bar()  # Draw the top bar
                self.draw_reload_time()  # Draw the reload time
                pygame.display.update()
            elif self.state == "game_over":
                start_again_rect, exit_rect = self.draw_game_over()
                self.handle_game_over_input(start_again_rect, exit_rect)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()