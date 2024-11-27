import pygame

class UI:
    def __init__(self):
        self.width, self.height = 1000, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')

        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (90, 166, 110)
        self.blue = (0, 0, 255)
        self.light_blue = (2, 242, 219)  
        self.light_red = (255, 182, 193)  
        self.dark_green = (7, 90, 102)
        self.dark_blue = (8, 111, 158)
        self.gray = (34, 34, 34)
        
        # For null path exception
        self.default_img_path = r'assets/images/brick.pngf'

        # Load font   
        self.logo_font = pygame.font.Font( r'assets/fonts/KnightWarrior-w16n8.otf', 100)
        self.title_font = pygame.font.Font( r'assets/fonts/KnightWarrior-w16n8.otf', 40)
        self.subtitle_font = pygame.font.Font( r'assets/fonts/PressStart2P-Regular.ttf', 25)
        self.text_font = pygame.font.Font( r'assets/fonts/PressStart2P-Regular.ttf', 15)
        self.text_font_2 = pygame.font.Font( r'assets/fonts/KnightWarrior-w16n8.otf', 15)
        
        # Define cell size
        self.snake_block = 10
        # Top and left padding for grid, grid position (top left) will start here
        self.grid_pos = self.height // 20
        # Grid height is 90% window height
        self.rows = int((self.height * 0.9) // self.snake_block)
        # Grid width is 60% window width
        self.cols = int((self.width * 0.6) // self.snake_block)
        
        # Preload images
        self.load_border()
    
    def load_border(self):
        self.left_top_border_img = self.load_and_scale_img(0.15, r'assets/images/border_top_left.png')
        self.right_top_border_img = self.load_and_scale_img(0.15, r'assets/images/border_top_right.png')
        self.right_bot_border_img = self.load_and_scale_img(0.15, r'assets/images/border_bot_right.png')
        self.left_bot_border_img = self.load_and_scale_img(0.15, r'assets/images/border_bot_left.png')

    def draw_snake(self, snake_list, color):
        for position in snake_list:
            pygame.draw.rect(self.screen, color, [self.grid_pos + position[1] * self.snake_block, self.grid_pos + position[0] * self.snake_block, self.snake_block, self.snake_block])
        
    def draw_obstacles(self, obstacles_position_list):
        obstacle_img = pygame.image.load(r'assets/images/brick.png')
        obstacle_img = pygame.transform.scale(obstacle_img, (self.snake_block, self.snake_block))
        for position in obstacles_position_list:
            self.screen.blit(obstacle_img, (self.grid_pos + position[1] * self.snake_block, self.grid_pos + position[0] * self.snake_block))

    def draw_food(self, food_position, color):
        food_row, food_col = food_position
        pygame.draw.rect(self.screen, color, [self.grid_pos + food_col * self.snake_block, self.grid_pos + food_row * self.snake_block, self.snake_block, self.snake_block])

    def clear_screen(self):
        self.screen.fill(self.black)
        # Create border
        self.screen.blit(self.left_top_border_img, (3, 0))
        self.screen.blit(self.right_top_border_img, (self.width - 67, 0))
        self.screen.blit(self.right_bot_border_img, (self.width - 67, self.height - 89))
        self.screen.blit(self.left_bot_border_img, (3, self.height - 89))

        # Dont care about this
        self.display_text_center("@ HCMUTE - 2024", self.height - 14, self.light_red, self.text_font_2)
    
    def refresh_screen(self):
        pygame.display.flip()
    
    def update_screen(self):
        pygame.display.update()
    
    def draw_grid(self):
        grid_color = self.gray
        grid_width = self.cols * self.snake_block
        grid_height = self.rows * self.snake_block
        for row in range(self.rows + 1):
            start_point_y =  self.grid_pos + row * self.snake_block
            pygame.draw.line(self.screen, grid_color, (self.grid_pos, start_point_y), (self.grid_pos + grid_width, start_point_y))
        for col in range(self.cols + 1):
            start_point_x = self.grid_pos + col * self.snake_block
            pygame.draw.line(self.screen, grid_color, (start_point_x, self.grid_pos), (start_point_x, self.grid_pos + grid_height))

    def display_text(self, text, x, y, color, font):
        text_surface = font.render(text, True, color)
        return self.screen.blit(text_surface, (x, y))
    
    def display_text_center(self, text, y, color, font):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(self.width//2, y))
        return self.screen.blit(text_surface, text_rect)
    
    def load_and_scale_img(self, scale_rate, img_path):
        image = pygame.image.load(img_path if img_path else self.default_img_path)
        return pygame.transform.scale(image, (image.get_width() * scale_rate, image.get_height() * scale_rate))
        
    def display_image(self, x, y, scale_rate, img_path):
        return self.screen.blit(self.load_and_scale_img(scale_rate, img_path), (x, y))
    
    def display_button(self, coordinate, size, text, font, text_color, button_color, border_width=0, radius=0, border_color=(0, 0, 0)):   
        # Draw button 
        button_rect = pygame.Rect(coordinate, size)
        pygame.draw.rect(self.screen, button_color, button_rect, border_radius=radius) # Fill
        pygame.draw.rect(self.screen, border_color, button_rect, border_width, border_radius=radius) # Border
        
        # Display text
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)
        return button_rect
    
    def display_border(self, coordinate, size, color, width, radius):
        return pygame.draw.rect(self.screen, color, (coordinate, size), width, radius) 