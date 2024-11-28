import pygame

pygame.init()

# Cửa sổ
screen = pygame.display.set_mode((800, 600))

# Màu sắc
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Nút
button_rect = pygame.Rect(300, 250, 200, 100)

running = True
while running:
    screen.fill(WHITE)
    mouse_pos = pygame.mouse.get_pos()

    # Kiểm tra hover
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, GREEN, button_rect)

        # Kiểm tra click chuột trái
        if pygame.mouse.get_pressed()[0]:
            pygame.draw.rect(screen, BLUE, button_rect)  # Đổi màu khi nhấn
    else:
        pygame.draw.rect(screen, RED, button_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
