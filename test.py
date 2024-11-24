import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Thiết lập cửa sổ
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Simple Menu in Pygame")

# Chọn font chữ 
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (50, 50, 255)
BUTTON_HOVER_COLOR = (100, 100, 255)

# Các lựa chọn trong menu
menu_options = ['Start', 'Settings', 'Quit']
selected_option = 0  # Mặc định lựa chọn là 'Start'

def draw_text(text, font, color, surface, x, y):
    """Hàm vẽ văn bản tại vị trí (x, y)"""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

def draw_menu():
    """Hàm vẽ menu"""
    screen.fill(BLACK)  # Màu nền
    draw_text('Main Menu', font, WHITE, screen, 400, 100)

    # Vẽ các nút
    for index, option in enumerate(menu_options):
        y_pos = 200 + index * 100
        color = BUTTON_HOVER_COLOR if index == selected_option else BUTTON_COLOR
        pygame.draw.rect(screen, color, (300, y_pos - 30, 200, 60))
        draw_text(option, button_font, WHITE, screen, 400, y_pos)

    pygame.display.flip()

def main_game():
    screen.fill(WHITE)
    draw_text("Game Screen", font, BLACK, screen, 400, 300)
    pygame.display.flip()

def settings():
    screen.fill(WHITE)
    draw_text("Settings", font, BLACK, screen, 400, 300)
    pygame.display.flip()

def run():
    global selected_option
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if menu_options[selected_option] == 'Start':
                        main_game()
                    elif menu_options[selected_option] == 'Settings':
                        settings()
                    elif menu_options[selected_option] == 'Quit':
                        running = False

        draw_menu()

    pygame.quit()
    sys.exit()

# Chạy chương trình
run()
