import pygame

class UI:
    def __init__(self):
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')

        # Màu sắc
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)

    def draw_snake(self, snake_block, snake_list):
        for x in snake_list:
            pygame.draw.rect(self.screen, self.green, [x[0], x[1], snake_block, snake_block])

    def draw_food(self, foodx, foody, snake_block):
        pygame.draw.rect(self.screen, self.white, [foodx, foody, snake_block, snake_block])

    def display_message(self, message):
        font_style = pygame.font.SysFont("bahnschrift", 25)
        mesg = font_style.render(message, True, self.red)
        self.screen.blit(mesg, [self.width / 6, self.height / 3])

    def refresh_screen(self):
        pygame.display.update()

    def clear_screen(self):
        self.screen.fill(self.black)
