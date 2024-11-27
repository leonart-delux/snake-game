from Logic.gamelogic import *
from Logic.algorithms import Pathfinding

class AIPlayerGameLogic(BaseGameLogic):
    def __init__(self, obstacles, ui, initial_pos):
        super().__init__(obstacles, (ui.rows, ui.cols), initial_pos)
        self.pathfinding = Pathfinding((self.numb_rows, self.numb_cols))
        
        self.ui = ui
        self.path = []
        self.algorithm = self.pathfinding.path_algorithm['BFS']

    def find_move(self, temp_obstacles):
        """
        temp_obstacles is temporary obstacles (snake or other ones)
        """
        if not self.path:
            # Union obstacles and snake position
            obstacles_and_snake = self.obstacles | temp_obstacles 
            start = (self.head_row, self.head_col)
            goal = (self.food_row, self.food_col)
            self.path = self.pathfinding.find_path(start, goal, obstacles_and_snake, self.algorithm)
            
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
            
    def one_frame_process(self, temp_obstacles):
        """
        temp_obstacles is for temporary obtacles in 1 process (snake other ones)
        """
        self.find_move(temp_obstacles)
        self.update_snake_position()
        self.check_collisions()
        self.check_boundaries()
        self.check_eat_food()

    def update_screen(self):
        self.ui.draw_food((self.food_row, self.food_col), self.ui.light_red)
        self.ui.draw_snake(self.snake_list, self.ui.red)
        
            