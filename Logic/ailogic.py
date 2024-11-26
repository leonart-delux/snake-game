from Logic.gamelogic import *
from Logic.algorithms import Pathfinding

class AIPlayerGameLogic(BaseGameLogic):
    def __init__(self, ui, initial_pos):
        super().__init__(set(), (ui.rows, ui.cols), initial_pos)
        self.pathfinding = Pathfinding((self.numb_rows, self.numb_cols))
        
        self.ui = ui
        self.path = []
        
    def get_neighbors(self, position):
        """
        Return the neighbors of a given position.
        """
        row, col = position
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < self.numb_rows and 0 <= new_col < self.numb_cols:
                neighbors.append((new_row, new_col))

        return neighbors

        
    def flood_fill(self, position, obstacles_list):
        """
        This function is used to count the number of reachable cells from a given position.
        """
        visited = set()
        stack = [position]
        count = 0

        while stack:
            current = stack.pop()
            if current in visited or current in obstacles_list:
                continue
            visited.add(current)
            count += 1
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited and neighbor not in obstacles_list:
                    stack.append(neighbor)

        return count
    
    def find_safe_move(self, snake_as_obstacles):
        """
        Find the best move that has the most empty cells around it.
        """
        neighbors = self.get_neighbors((self.head_row, self.head_col))
        max_space = 0
        best_move = None

        for neighbor in neighbors:
            if neighbor not in snake_as_obstacles:
                # Count the number of reachable cells from this neighbor
                space = self.flood_fill(neighbor, snake_as_obstacles)
                if space > max_space:
                    max_space = space
                    best_move = neighbor

        return best_move

    def find_move(self):
        if not self.path:
            snake_as_obstacles = set(tuple(block) for block in self.snake_list)
            start = (self.head_row, self.head_col)
            goal = (self.food_row, self.food_col)
            self.path = self.pathfinding.find_path(start, goal, snake_as_obstacles)
            
            if not self.path: # if it still can't find a path
                safe_move = self.find_safe_move(snake_as_obstacles)
                if safe_move:
                    self.path = [safe_move]
                else:
                    # If there is no safe move, the snake will move randomly and probably die
                    self.path = []
            
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

        
            