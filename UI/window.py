import pygame

class UI:
    def __init__(self):
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')

        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.light_blue = (173, 216, 230)  
        self.light_red = (255, 182, 193)  
        
        self.font_path = r'assets/fonts/PressStart2P-Regular.ttf'
        
        self.snake_block = 10
        
        self.rows = self.height // self.snake_block
        self.cols = self.width // self.snake_block

    def draw_snake(self, snake_block, snake_list, color):
        for position in snake_list:
            grid_x, grid_y = self.get_grid_position(position[0], position[1])
            pygame.draw.rect(self.screen, color, [grid_x * self.snake_block, grid_y * self.snake_block, self.snake_block, self.snake_block])

    def draw_food(self, food_position, color):
        food_x, food_y = self.get_grid_position(food_position[0], food_position[1])
        pygame.draw.rect(self.screen, color, [food_x * self.snake_block, food_y * self.snake_block, self.snake_block, self.snake_block])

    def display_message(self, message):
        font_style = pygame.font.Font(self.font_path, 15)
        mesg = font_style.render(message, True, self.red)
        self.screen.blit(mesg, [self.width / 6, self.height / 3])

    def refresh_screen(self):
        pygame.display.update()

    def clear_screen(self):
        self.screen.fill(self.black)

    def get_grid_position(self, x, y):
        grid_x = int(x // self.snake_block)
        grid_y = int(y // self.snake_block)
        return grid_x, grid_y

    def draw_grid(self):
        for row in range(self.rows):
            pygame.draw.line(self.screen, self.blue, (0, row * self.snake_block), (self.width, row * self.snake_block))
        for col in range(self.cols):
            pygame.draw.line(self.screen, self.blue, (col * self.snake_block, 0), (col * self.snake_block, self.height))

    def display_text(self, text, x, y, color, size):
        font = pygame.font.Font(self.font_path, size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
        
        
