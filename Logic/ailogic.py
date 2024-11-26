from Logic.gamelogic import *
from Logic.algorithms import Pathfinding

class AIPlayerGameLogic(BaseGameLogic):
    def __init__(self, ui, initial_pos):
        super().__init__(set(), (ui.rows, ui.cols), initial_pos)
        self.pathfinding = Pathfinding((self.numb_rows, self.numb_cols))
        
        self.ui = ui
        self.path = []

    def find_move(self):
        if not self.path:
            snake_as_obstacles = set(tuple(block) for block in self.snake_list)
            start = (self.head_row, self.head_col)
            goal = (self.food_row, self.food_col)
            self.path = self.pathfinding.find_path(start, goal, snake_as_obstacles)
            
        if self.path:
            next_move = self.path.pop(0)
            self.move_direction[0] = next_move[0] - self.head_row
            self.move_direction[1] = next_move[1] - self.head_col
            
    def game_loop(self):
        self.update_screen_AI()
        while not self.game_close:
            while self.game_over:
                self.ui.clear_screen()
                self.ui.display_message("You lose! Press Q-Quit or C-Play Again")
                self.ui.refresh_screen()
                self.handle_game_close_events()

            self.find_move()
            self.update_snake_position()
            self.check_collisions()
            self.check_boundaries()
            self.check_eat_food()
            self.update_screen_AI()

            self.clock.tick(self.snake_speed)

    def update_screen_AI(self):
        self.ui.clear_screen()
        self.ui.draw_grid()
        self.ui.draw_food((self.food_row, self.food_col), self.ui.light_red)
        self.ui.draw_snake(self.snake_list, self.ui.red)
        self.ui.display_text(f"AI: {self.score}", self.ui.width - 150, 10, self.ui.red, 20)
        self.ui.refresh_screen()

        
            