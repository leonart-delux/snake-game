import random
from collections import deque

class Pathfinding:
    def __init__(self, grid_size, block_size):
        self.grid_size = grid_size
        self.block_size = block_size

    def bfs(self, start, goal, obstacles):
        queue = deque([start])
        came_from = {start: None}
        directions = [(0, self.block_size), (0, -self.block_size), (self.block_size, 0), (-self.block_size, 0)]

        while queue:
            current = queue.popleft()
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

    def find_path(self, start, goal, obstacles):
        return self.dfs(start, goal, obstacles)
