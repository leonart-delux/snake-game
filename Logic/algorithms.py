import random
from collections import deque
import heapq
class Pathfinding:
    def __init__(self, map_size):
        self.numb_rows, self.numb_cols = map_size
        self.path_algorithm = {
            'bfs': self.bfs,
            'dfs': self.dfs,
            'astar': self.a_star,
            'hill': self.hill_climbing,
            'beam': self.beam_search
        }
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    def find_path(self, start, goal, obstacles, algorithm):
        return algorithm(start, goal, obstacles)
    
    def get_neighbors(self, position):
        """
        Return the neighbors of a given position that does not accross boudaries.
        """
        row, col = position
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (0 <= new_row < self.numb_rows) and (0 <= new_col < self.numb_cols):
                neighbors.append((new_row, new_col))

        return neighbors
        
    def bfs(self, start, goal, obstacles_list):
        queue = deque([start])
        came_from = { start: None }

        while queue:
            current = queue.popleft()
            if current == goal:
                path = []
                while current:
                    path.append(current)
                    current = came_from[current]
                return path[::-1][1:]

            for direction in self.directions:
                neighbor = (current[0] + direction[0], current[1] + direction[1])
                
                # Neighbor accrosses boudary
                if (neighbor[0] < 0) or (neighbor[0] >= self.numb_rows) or (neighbor[1] < 0) or (neighbor[1] >= self.numb_cols):
                    continue
                
                # Neighbor is visited or neighbor is obstacles_list (grid obstacles and snake included)
                if neighbor in came_from or neighbor in obstacles_list:
                    continue
                
                # True case
                queue.append(neighbor)
                came_from[neighbor] = current

        return []
        
    def dfs(self, start, goal, obstacles_list):
        stack = [start]
        came_from = {start: None}

        while stack:
            current = stack.pop()
            if current == goal:
                path = []
                while current:
                    path.append(current)
                    current = came_from[current]
                return path[::-1][1:]

            for direction in self.directions:
                neighbor = (current[0] + direction[0], current[1] + direction[1])
                
                if (neighbor[0] < 0) or (neighbor[0] >= self.numb_rows) or (neighbor[1] < 0) or (neighbor[1] >= self.numb_cols):
                    continue
                
                if neighbor in came_from or neighbor in obstacles_list:
                    continue
                
                stack.append(neighbor)
                came_from[neighbor] = current

        return []
    
    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def a_star(self, start, goal, obstacles_list):
        open_set = [] # Priority queue
        heapq.heappush(open_set, (0, start))
        came_from = {start: None}
        g_score = {start: 0}

        while open_set:
            # Get the node with the lowest f_score / (score, node)
            current_priority, current = heapq.heappop(open_set)

            if current == goal:
                # Reconstruct the path
                path = []
                while current:
                    path.append(current)
                    current = came_from[current]
                return path[::-1][1:]

            for direction in self.directions:
                neighbor = (current[0] + direction[0], current[1] + direction[1])

                # Check if the neighbor is out of bounds
                if (neighbor[0] < 0 or neighbor[0] >= self.numb_rows or
                    neighbor[1] < 0 or neighbor[1] >= self.numb_cols):
                    continue

                # Check if the neighbor is an obstacle or already visited
                if neighbor in obstacles_list or neighbor in came_from:
                    continue

                # Actual cost from start to neighbor, use to check if the path is shorter
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor))
                    came_from[neighbor] = current

        return []

    def hill_climbing(self, start, goal, obstacles_list):
        current = start
        came_from = {start: None}

        while current != goal:
            neighbors = []
            
            for direction in self.directions:
                neighbor = (current[0] + direction[0], current[1] + direction[1])

                if (neighbor[0] < 0 or neighbor[0] >= self.numb_rows or
                    neighbor[1] < 0 or neighbor[1] >= self.numb_cols):
                    continue

                if neighbor in obstacles_list or neighbor in came_from:
                    continue

                neighbors.append((self.heuristic(neighbor, goal), neighbor))

            # If no valid neighbors, we are stuck. Backtrack to the previous node can solve this but I think it's not necessary due to our purpose of making this game.
            if not neighbors:
                return []

            # Select the neighbor with the best heuristic value (greedy choice)
            next_step = min(neighbors, key=lambda x: x[0])[1]
            
            came_from[next_step] = current
            current = next_step

        path = []
        while current:
            path.append(current)
            current = came_from[current]
        
        return path[::-1][1:]

    def beam_search(self, start, goal, obstacles_list, beam_width=2):
        open_set = [(self.heuristic(start, goal), start)] 
        came_from = {start: None}
        g_score = {start: 0}

        while open_set:
            # Use new_open_set to store the best nodes
            new_open_set = []
            
            for _, current in open_set:
                if current == goal:  
                    path = []
                    while current:
                        path.append(current)
                        current = came_from[current]
                    return path[::-1][1:] 

                for direction in self.directions:
                    neighbor = (current[0] + direction[0], current[1] + direction[1])

                    if (neighbor[0] < 0 or neighbor[0] >= self.numb_rows or
                        neighbor[1] < 0 or neighbor[1] >= self.numb_cols):
                        continue
                    
                    if neighbor in obstacles_list or neighbor in came_from:
                        continue
                    
                    tentative_g_score = g_score[current] + 1
                    f_score = tentative_g_score + self.heuristic(neighbor, goal)

                    new_open_set.append((f_score, neighbor))
                    came_from[neighbor] = current
                    
                    g_score[neighbor] = tentative_g_score

            # Choose the best nodes from new_open_set
            open_set = sorted(new_open_set, key=lambda x: x[0])[:beam_width]
            
        return [] 
        
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
    
    def find_safe_move(self, obstacles, head_pos):
        """
        Find the best move that has the most empty cells around it.
        """
        neighbors = self.get_neighbors(head_pos)
        max_space = 0
        best_move = None

        for neighbor in neighbors:
            if neighbor not in obstacles:
                # Count the number of reachable cells from this neighbor
                space = self.flood_fill(neighbor, obstacles)
                if space > max_space:
                    max_space = space
                    best_move = neighbor

        return best_move
    
