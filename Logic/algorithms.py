import random
from collections import deque
import heapq
class Pathfinding:
    def __init__(self, map_size):
        self.numb_rows, self.numb_cols = map_size
        
    def bfs(self, start, goal, obstacles_list):
        queue = deque([start])
        came_from = { start: None }
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while queue:
            current = queue.popleft()
            if current == goal:
                path = []
                while current:
                    path.append(current)
                    current = came_from[current]
                return path[::-1][1:]

            for direction in directions:
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
        
    def dfs(self, start, goal, obstacles):
        stack = [start]
        came_from = {start: None}
        directions = [(0, self.block_size), (0, -self.block_size), (self.block_size, 0), (-self.block_size, 0)]

        while stack:
            current = stack.pop()
            if current == goal:
                path = []
                while current:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]

            for direction in directions:
                neighbor = (current[0] + direction[0], current[1] + direction[1])
                if 0 <= neighbor[0] < self.grid_size[0] and 0 <= neighbor[1] < self.grid_size[1]:
                    if neighbor not in came_from and neighbor not in obstacles:
                        stack.append(neighbor)
                        came_from[neighbor] = current

        return []
    
    def a_star(self, start, goal, obstacles):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {start: None}
        g_score = {start: 0}

        directions = [(0, self.block_size), (0, -self.block_size), (self.block_size, 0), (-self.block_size, 0)]

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                path = []
                while current:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]

            for direction in directions:
                neighbor = (current[0] + direction[0], current[1] + direction[1])
                if 0 <= neighbor[0] < self.grid_size[0] and 0 <= neighbor[1] < self.grid_size[1] and neighbor not in obstacles:
                    tentative_g_score = g_score[current] + 1
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        g_score[neighbor] = tentative_g_score
                        f_score = tentative_g_score + heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_score, neighbor))
                        came_from[neighbor] = current

        return []

    def hill_climbing(self, start, goal, obstacles):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        current = start
        came_from = {start: None}
        directions = [(0, self.block_size), (0, -self.block_size), (self.block_size, 0), (-self.block_size, 0)]

        while current != goal:
            next_step = None
            min_heuristic = float('inf')

            for direction in directions:
                neighbor = (current[0] + direction[0], current[1] + direction[1])
                if 0 <= neighbor[0] < self.grid_size[0] and 0 <= neighbor[1] < self.grid_size[1] and neighbor not in obstacles:
                    h = heuristic(neighbor, goal)
                    if h < min_heuristic:
                        min_heuristic = h
                        next_step = neighbor

            if not next_step:
                break  # Không thể tiến xa hơn

            came_from[next_step] = current
            current = next_step

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        return []

    def beam_search(self, start, goal, obstacles, beam_width=2):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        queue = [(start, [start])]
        directions = [(0, self.block_size), (0, -self.block_size), (self.block_size, 0), (-self.block_size, 0)]

        while queue:
            queue = sorted(queue, key=lambda x: heuristic(x[0], goal))[:beam_width]
            new_queue = []

            for current, path in queue:
                if current == goal:
                    return path

                for direction in directions:
                    neighbor = (current[0] + direction[0], current[1] + direction[1])
                    if 0 <= neighbor[0] < self.grid_size[0] and 0 <= neighbor[1] < self.grid_size[1] and neighbor not in obstacles and neighbor not in path:
                        new_queue.append((neighbor, path + [neighbor]))

            queue = new_queue

        return []


    def find_path(self, start, goal, obstacles):
        return self.bfs(start, goal, obstacles)
