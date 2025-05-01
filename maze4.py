import pygame
import numpy as np
import random

# Configuraciones generales
width, height = 600, 600
Row, Col = 10, 10
Celda = width // Col

# Colores
White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Blue = (0, 100, 255)
Green = (0, 255, 0)
class Maze:
 def __init__(self, width=600, height=600 ):
     self.width=width
     self.height=height

 def create_maze(self,obstacle_ratio=0.2, start=(0, 0), goal=(9, 9)):
     maze = np.zeros((Row, Col), dtype=int)
     total_cells = Row * Col
     num_obstacles = int(total_cells * obstacle_ratio)

     while True:
        maze[:] = 0
        obstacles = set()

        while len(obstacles) < num_obstacles:
            r = random.randint(0, Row - 1)
            c = random.randint(0, Col - 1)
            if (r, c) != start and (r, c) != goal:
                obstacles.add((r, c))

        for r, c in obstacles:
            maze[r][c] = 1

        # Validar que haya al menos un camino
        if self.is_path_possible(maze, start, goal):
            break

     return maze

 def is_path_possible(self, maze, start, goal):
     from collections import deque
     visited = np.zeros_like(maze, dtype=bool)
     queue = deque([start])

     while queue:
        r, c = queue.popleft()
        if (r, c) == goal:
            return True
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < Row and 0 <= nc < Col and not visited[nr][nc] and maze[nr][nc] == 0:
                visited[nr][nc] = True
                queue.append((nr, nc))

     return False

 def draw_grid(self, window, maze, Clu_pos, finish):
    window.fill(White)

    for R in range(Row):
        for C in range(Col):
            rect = pygame.Rect(C * Celda, R * Celda, Celda, Celda)
            color = Black if maze[R][C] == 1 else White
            pygame.draw.rect(window, color, rect)
            pygame.draw.rect(window, Blue, rect, 1)

    FR, FC = finish
    pygame.draw.rect(window, Green, (FC * Celda, FR * Celda, Celda, Celda))

    AR, AC = Clu_pos
    pygame.draw.circle(window, Red, (AC * Celda + Celda // 2, AR * Celda + Celda // 2), Celda // 3)

    pygame.display.update()
