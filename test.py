import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Cửa sổ chính
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Confirmation Dialog")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Font chữ
font = pygame.font.Font(None, 36)

# Hộp thoại xác nhận
def confirmation_dialog(screen, message):
    """Hiển thị hộp thoại xác nhận, trả về True/False tùy thuộc vào lựa chọn."""
    dialog_rect = pygame.Rect(200, 200, 400, 200)  # Kích thước hộp thoại
    yes_button = pygame.Rect(250, 300, 100, 50)  # Nút Yes
    no_button = pygame.Rect(450, 300, 100, 50)   # Nút No

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if yes_button.collidepoint(mouse_pos):
                    return True
                if no_button.collidepoint(mouse_pos):
                    return False

        # Vẽ hộp thoại
        pygame.draw.rect(screen, GRAY, dialog_rect)
        pygame.draw.rect(screen, GREEN, yes_button)
        pygame.draw.rect(screen, RED, no_button)

        # Vẽ viền
        pygame.draw.rect(screen, BLACK, dialog_rect, 2)
        pygame.draw.rect(screen, BLACK, yes_button, 2)
        pygame.draw.rect(screen, BLACK, no_button, 2)

        # Hiển thị văn bản
        text_surface = font.render(message, True, BLACK)
        screen.blit(text_surface, text_surface.get_rect(center=dialog_rect.center))

        yes_text = font.render("Yes", True, BLACK)
        screen.blit(yes_text, yes_text.get_rect(center=yes_button.center))

        no_text = font.render("No", True, BLACK)
        screen.blit(no_text, no_text.get_rect(center=no_button.center))

        pygame.display.flip()

# Chương trình chính
def main():
    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Hiển thị hộp thoại xác nhận
                result = confirmation_dialog(screen, "Do you want to quit?")
                if result:
                    print("User chose Yes")
                    running = False
                else:
                    print("User chose No")

        # Hiển thị thông báo chính
        message = font.render("Press SPACE to confirm quitting.", True, BLACK)
        screen.blit(message, (200, 100))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
