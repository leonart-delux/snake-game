from Logic.gamelogic import *
from Logic.algorithms import Pathfinding

class AIPlayerGameLogic(BaseGameLogic):
    def __init__(self, obstacles, ui, initial_pos):
        super().__init__(obstacles, (ui.rows, ui.cols), initial_pos)
        self.pathfinding = Pathfinding((self.numb_rows, self.numb_cols))
        
        self.ui = ui
        self.path = []
        self.traveled_count = 0
        self.algorithm = self.pathfinding.path_algorithm['BFS']

    def find_move(self):
        """
        temp_obstacles is temporary obstacles (snake or other ones)
        """
        # Remove self-next head in temp_obstacles
        # If don't remove --> block all directions --> move ahead
        # self.remov_next_snake_head_in_temp_obstacles()
        self.remove_food_in_temp_obstacles()
        # Union obstacles and all snake positions
        obstacles_and_snake = self.const_obstacles | self.temp_obstacles 
        start = (self.head_row, self.head_col)
        goal = (self.food_row, self.food_col)
        self.path, turn_traveled_count = self.pathfinding.find_path(start, goal, obstacles_and_snake, self.algorithm)
        self.traveled_count += turn_traveled_count
            
        if not self.path: # if it still can't find a path
            safe_move = self.pathfinding.find_safe_move(obstacles_and_snake, (self.head_row, self.head_col))
            if safe_move:
                self.path = [safe_move]
            else:
                # If there is no safe move, the snake will move randomly and probably die
                self.path = []
            
        if self.path:
            next_move = self.path.pop(0)
            self.move_direction[0] = next_move[0] - self.head_row
            self.move_direction[1] = next_move[1] - self.head_col
            
    def one_frame_data_process(self):
        self.find_move()
        self.update_snake_position()
    
    def update_screen(self):
        self.ui.draw_food((self.food_row, self.food_col), self.ui.light_red)
        self.ui.draw_snake(self.snake_list, self.ui.red)
        
            