from maze4 import Maze
from configs import PYGAME
from memory import MemoryM



class Rl:
 def __init__(self):
    self.configs=PYGAME()
    self.memory=MemoryM()
    self.maze=Maze()
     
 def train_and_save(self,agent, num_paths=300, episodes=1000):
    all_paths = []
    all_mazes = []

    for path_index in range(num_paths):
        print(f"\nEntrenando ruta #{path_index + 1}")
        best_path = []
        min_steps = float('inf')
        epsilon = 1.0
        epsilon_min = 0.2
        epsilon_decay = 0.999
        best_maze = None

        for ep in range(episodes):
            maze = self.maze.create_maze()
            state = self.configs.start
            step_count = 0
            episode_path = []
            total_reward = 0

            for _ in range(100):
                flat_state = agent.flatten_state(state)
                action = agent.get_action(flat_state, epsilon)
                next_state = agent.step(state, action, maze)

                reward = -0.1
                done = next_state == self.configs.goal
                if done:
                    reward = 50

                agent.remember(flat_state, action, reward, agent.flatten_state(next_state), done)
                agent.train()

                episode_path.append(action)
                state = next_state
                total_reward += reward
                step_count += 1
                if done:
                    break

            if state == self.configs.goal and step_count < min_steps:
                best_path = episode_path
                min_steps = step_count
                best_maze = maze

            epsilon = max(epsilon_min, epsilon * epsilon_decay)
            print(f"  Episodio {ep + 1}/{episodes} | Pasos: {step_count} | Recompensa total: {total_reward:.2f} | Epsilon: {epsilon:.3f}")

        if best_path:
            print(f"Ruta #{path_index + 1} encontrada con {min_steps} pasos.")
            all_paths.append(best_path)
            all_mazes.append(best_maze)
        else:
            print(f"No se encontró una ruta válida para el intento #{path_index + 1}.")

    
    self.save_paths_and_mazes(all_paths, all_mazes)
