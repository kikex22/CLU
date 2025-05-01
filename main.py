import pygame
import time
from maze4 import Maze
from clu import CluAgent
from memory import MemoryM
from configs import PYGAME
from Rl import Rl
from Ft import FT


memory=MemoryM()
configs=PYGAME()
rl=Rl()
maze=Maze()
ft=FT()


# Inicialización de Pygame


if __name__ == "__main__":
    agent = CluAgent()
    
    all_paths, all_mazes = memory.load_paths_and_mazes()

    if all_paths is None or all_mazes is None:
        print("No hay rutas entrenadas. Entrenando ahora...")
        rl.train_and_save(agent, num_paths=300)
        all_paths, all_mazes = memory.load_paths_and_mazes()

    print("Rutas y laberintos cargados. Generando un nuevo laberinto...")
    new_maze = maze.create_maze()

    print("Visualizando el nuevo laberinto y la solución...")
    ft.visualize_new_maze_and_solution(agent, new_maze)

    # Bucle de eventos de Pygame para mantener la ventana abierta
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                time.sleep(2)
                pygame.quit()
                exit()
   

                

