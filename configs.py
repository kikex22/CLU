import pygame
from maze4 import Maze
import time 

maze=Maze()
# Configuración de Pygame
class PYGAME:
  def __init__(self, width=600, height=600, start=(0,0), goal=(9,9)):
        pygame.init()
        self.width=width
        self.height=height
        self.start=start
        self.goal=goal
        self.window= pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Clu - Multi Policy")
        self.actions=['up', 'down', 'left', 'right']
        self.action_map= {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1)
         }
 
    
  # --- Multi-policy DQN --- 
  def path_is_valid(self,agent, path, maze):
    state = self.start
    for action in path:
        next_state = agent.step(state, action, maze)
        if next_state == state:
            return False
        state = next_state
    return state == self.goal
  
  