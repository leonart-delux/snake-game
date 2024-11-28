from Logic.gamelogic import *

class SinglePlayerGameLogic(BaseGameLogic):
    def __init__(self, obstacles, ui, snake_color):
        super().__init__(obstacles, (ui.rows, ui.cols))
        self.ui = ui
        self.snake_color = snake_color
        # Indicate if direction is changed in frame loop
        self.is_changed_direction = False

    def handle_events(self, event):
        # only accept 1 move
        moved = False
        if event.type == pygame.KEYDOWN and not self.is_changed_direction:
            if event.key == pygame.K_LEFT and self.move_direction != [0, 1]:
                self.move_direction = [0, -1]
                self.is_changed_direction = True
            elif event.key == pygame.K_RIGHT and self.move_direction != [0, -1]:
                self.move_direction = [0, 1]
                self.is_changed_direction = True
            elif event.key == pygame.K_UP and self.move_direction != [1, 0]:
                self.move_direction = [-1, 0]
                self.is_changed_direction = True
            elif event.key == pygame.K_DOWN and self.move_direction != [-1, 0]:
                self.move_direction = [1, 0]
                self.is_changed_direction = True                    
    
    def one_frame_data_process(self):
        self.update_snake_position()
                
    def update_screen(self):
        self.ui.draw_food((self.food_row, self.food_col), self.snake_color)
        self.ui.draw_snake(self.snake_list, self.snake_color)

    def handle_lose(self, text):
        running_noti = True
        while self.game_over and running_noti:
            self.ui.display_button((self.ui.width // 4, self.ui.height // (10/4)), (self.ui.width // 2, self.ui.height // 10), text, self.ui.subtitle_font, self.ui.white, self.snake_color, radius=10)
            self.ui.update_screen()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    running_noti = False
