import pygame

class UI:
    def __init__(self):
        self.width, self.height = 1000, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()

        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (207, 72, 72)
        self.green = (90, 166, 110)
        self.blue = (69, 190, 230)
        self.light_blue = (173, 216, 230)  
        self.light_red = (255, 182, 193)  
        self.dark_green = (7, 90, 102)
        self.dark_blue = (34, 87, 122)
        self.gray = (34, 34, 34)
        self.purple = (142, 91, 227)
        self.yellow = (224, 197, 61)
        
        self.snake_color = [ self.yellow, self.purple, self.green, self.blue, self.red ]
        
        # For null path exception
        self.default_img_path = r'assets/images/brick.pngf'

        # Load font   
        self.logo_font = pygame.font.Font( r'assets/fonts/KnightWarrior-w16n8.otf', 100)
        self.title_font = pygame.font.Font( r'assets/fonts/KnightWarrior-w16n8.otf', 40)
        self.subtitle_font = pygame.font.Font( r'assets/fonts/PressStart2P-Regular.ttf', 25)
        self.text_font = pygame.font.Font( r'assets/fonts/PressStart2P-Regular.ttf', 15)
        self.text_font_2 = pygame.font.Font( r'assets/fonts/KnightWarrior-w16n8.otf', 15)
        self.small_text_font = pygame.font.Font( r'assets/fonts/PressStart2P-Regular.ttf', 10)
        
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
    
    def get_snake_color(self):
        return self.snake_color.pop(0)
    
    def return_snake_color(self, color):
        self.snake_color.append(color)

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
        if (border_width > 0):
            pygame.draw.rect(self.screen, border_color, button_rect, border_width, border_radius=radius) # Border
        
        # Display text
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)
        return button_rect
    
    def display_border(self, coordinate, size, color, width, radius):
        return pygame.draw.rect(self.screen, color, (coordinate, size), width, radius)
    
    def draw_slider(self, x, y, length, value, min_value, max_value, handle_color, track_color):
        # Track
        track_height = 4
        handle_radius = 5
        pygame.draw.rect(self.screen, track_color, (x, y - track_height // 2, length, track_height), border_radius=2)
        
        # Handle position
        handle_x = x + ((value - min_value) / (max_value - min_value)) * length
        pygame.draw.circle(self.screen, handle_color, (int(handle_x), y), handle_radius)
        
        return handle_x  # Handle position

class ComboBox:
    def __init__(self, w, h, options, font, text_color, box_color, border_color, option_color):
        self.width = w
        self.height = h
        self.options = options
        self.font = font
        self.text_color = text_color
        self.box_color = box_color
        self.border_color = border_color
        self.option_color = option_color
        self.selected = options[0]
        self.is_open = False
    
    def draw(self, screen, x, y):
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.option_rects = [pygame.Rect(x - self.width, y - i * self.height, self.width, self.height) for i in range(len(self.options))]
        
        # Draw the main box
        pygame.draw.rect(screen, self.box_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 2)
        
        # Draw the selected option
        text_surface = self.font.render(self.selected, False, self.text_color)
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 5))
        
        # If open, draw the dropdown options
        if self.is_open:
            for i, rect in enumerate(self.option_rects):
                pygame.draw.rect(screen, self.option_color, rect)
                pygame.draw.rect(screen, self.border_color, rect, 1)
                option_text = self.font.render(self.options[i], False, self.text_color)
                screen.blit(option_text, (rect.x + 10, rect.y + 5))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                # Toggle dropdown
                self.is_open = not self.is_open
            elif self.is_open:
                # Check if an option is clicked
                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(event.pos):
                        self.selected = self.options[i]
                        break
                self.is_open = False
        return None
    
class Slider:
    def __init__(self, x, y, length, min_value, max_value, initial_value, handle_color, track_color):
        self.x = x
        self.y = y
        self.length = length
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.handle_color = handle_color
        self.track_color = track_color
        self.handle_radius = 5
        self.track_height = 3
        self.acceptable_click_range = self.handle_radius + 5
        self.dragging = False

    def draw(self, screen):
        # Draw track
        pygame.draw.rect(screen, self.track_color, (self.x, self.y - self.track_height // 2, self.length, self.track_height), border_radius=2)
        # Calculate handle position
        self.handle_x = self.x + ((self.value - self.min_value) / (self.max_value - self.min_value)) * self.length
        # Draw handle
        pygame.draw.circle(screen, self.handle_color, (int(self.handle_x), self.y), self.handle_radius)
        # Return handle position for event

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            mouse_x, mouse_y = event.pos
            # Check if mouse is click on handle
            if abs(mouse_x - self.handle_x) <= self.handle_radius + 5 and abs(mouse_y - self.y) <= self.handle_radius + 5:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Unhold left click
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x, _ = event.pos
            # Limit mouse_x position
            mouse_x = max(self.x, min(self.x + self.length, mouse_x))
            # Calculate value of slider
            self.value = self.min_value + ((mouse_x - self.x) / self.length) * (self.max_value - self.min_value)

    def get_value(self):
        return int(self.value)