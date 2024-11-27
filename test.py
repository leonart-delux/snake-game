import pygame

class ComboBox:
    def __init__(self, x, y, w, h, options, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.options = options
        self.font = font
        self.selected = options[0]
        self.is_open = False
        self.option_rects = [pygame.Rect(x, y + (i + 1) * h, w, h) for i in range(len(options))]
    
    def draw(self, screen):
        # Draw the main box
        # pygame.draw.rect(screen, (200, 200, 200), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2, 5)
        
        # Draw the selected option
        text_surface = self.font.render(self.selected, True, (0, 0, 0))
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 5))
        
        # If open, draw the dropdown options
        if self.is_open:
            for i, rect in enumerate(self.option_rects):
                pygame.draw.rect(screen, (220, 220, 220), rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)
                option_text = self.font.render(self.options[i], True, (0, 0, 0))
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
                        self.is_open = False
                        return self.selected
        return None

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)

# ComboBox setup
options = ["BFS", "DFS", "A*", "Dijkstra"]
combo_box = ComboBox(50, 50, 150, 30, options, font)

running = True
while running:
    screen.fill((255, 255, 255))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Handle ComboBox events
        selected_option = combo_box.handle_event(event)
        if selected_option:
            print(f"Selected: {selected_option}")
    
    # Draw ComboBox
    combo_box.draw(screen)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
