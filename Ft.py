#ft= FINE -TUNING
from configs import PYGAME
from maze4 import Maze
import time 
import pygame

maze=Maze()
configs=PYGAME()

class FT:
   def __init__(self):
      self.maze=Maze()
      self.configs=PYGAME()
   def visualize_new_maze_and_solution(self,agent, new_maze):
     state = self.configs.start
     epsilon = 0.2
     path = []
     step_count = 0
     tours=0
     completed_tours=0
     while True:
      tours +=1
      state=self.configs.start
      step_count=0
      path=[]

      for _ in range(300):  # Limite de 200 pasos
         flat_state = agent.flatten_state(state)
         action = agent.get_action(flat_state, epsilon)
         next_state = agent.step(state, action, new_maze)
         reward = -0.1
         done = next_state == self.configs.goal
         if done:
                reward = 50
         agent.remember(flat_state, action, reward, agent.flatten_state(next_state), done)
         agent.train()
         path.append(action)
         state = next_state
         step_count += 1

         # Dibujar el laberinto y el estado actual del agente
         self.maze.draw_grid(self.configs.window, new_maze, state, self.configs.goal)
         pygame.display.update()  # Actualizar la pantalla para ver el movimiento del agente
         time.sleep(0.1)  # Espera breve para poder visualizar el movimiento del agente

         if state == self.configs.goal:
            print(f"El agente llego a la meta en {step_count} pasos.")
            completed_tours+=1
            print(f"tours completados: {completed_tours} de {tours}")
            break  # El agente llegó a la meta
      else:
          print(f"El agente NO llego a la meta despues de {step_count} pasos.")
          print(f"van {tours} tours")
      new_maze=self.maze.create_maze()
      for event in pygame.event.get():
       if event.type == pygame.QUIT:
        pygame.quit()
        exit()

      if tours ==100:
       porcentaje=(completed_tours/tours)*100
       print("======================================================")
       print(f"Se completaron {tours} tours en total.")
       print(f"El agente llego a la meta en {completed_tours} de ellos.")
       print(f"Porcentaje de exito: {porcentaje:.2f}%")
       break