from settings import *

class Menu:
    def __init__(self):
        self.selected_option = 0
        self.options = ["Start Game", "Exit"]
        self.option_rects = []

    def navigate(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.selected_option
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, rect in enumerate(self.option_rects):
                if rect.collidepoint(mouse_pos):
                    return i
        return None

    def draw_menu(self, display_surface):
        display_surface.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        title_text = font.render("Main Menu", True, (255, 255, 255))
        display_surface.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, WINDOW_HEIGHT // 2 - title_text.get_height() // 2 - 100))

        font = pygame.font.Font(None, 50)
        self.option_rects = []
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_option else (100, 100, 100)
            option_text = font.render(option, True, color)
            option_rect = option_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + i * 50))
            self.option_rects.append(option_rect)
            display_surface.blit(option_text, option_rect)

        pygame.display.update()