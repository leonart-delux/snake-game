from Logic.gamelogic import *

class SinglePlayerGameLogic(BaseGameLogic):
    def __init__(self, obstacles, ui, initial_pos):
        super().__init__(obstacles, (ui.rows, ui.cols), initial_pos)
        self.ui = ui

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and self.move_direction != [0, 1]:
                self.move_direction = [0, -1]
            elif event.key == pygame.K_RIGHT and self.move_direction != [0, -1]:
                self.move_direction = [0, 1]
            elif event.key == pygame.K_UP and self.move_direction != [1, 0]:
                self.move_direction = [-1, 0]
            elif event.key == pygame.K_DOWN and self.move_direction != [-1, 0]:
                self.move_direction = [1, 0]
    
    def one_frame_data_process(self):
        self.update_snake_position()
                
    def update_screen(self):
        self.ui.draw_food((self.food_row, self.food_col), self.ui.light_red)
        self.ui.draw_snake(self.snake_list, self.ui.red)
