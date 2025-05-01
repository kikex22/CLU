import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import random
import time
import pygame
from Clu_Model import CLU
from maze4 import Maze
from memory import MemoryM 
from configs import PYGAME 
from Rl import Rl
maze=Maze()
memory=MemoryM()
configs=PYGAME()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")



class CluAgent:
    def __init__(self):
        self.model = CLU().to(device)
        self.memory = []
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.criterion = nn.MSELoss()
        self.start=(0,0)
        self.gamma = 0.95
        self.batch_size = 64

    def get_action(self, state, epsilon):
        if random.random() < epsilon:
            return random.randint(0, 3)
        state = torch.tensor(state, dtype=torch.float32).to(device)
        with torch.no_grad():
            q_values = self.model(state)
        return torch.argmax(q_values).item()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        if len(self.memory) > 10000:
            self.memory.pop(0)

    def train(self):
        if len(self.memory) < self.batch_size:
            return
        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.tensor(np.array(states), dtype=torch.float32).to(device)
        next_states = torch.tensor(np.array(next_states), dtype=torch.float32).to(device)
        actions = torch.tensor(actions).unsqueeze(1).to(device)
        rewards = torch.tensor(rewards).to(device)
        dones = torch.tensor(dones).to(device)

        q_values = self.model(states).gather(1, actions).squeeze()
        max_next_q = self.model(next_states).max(1)[0]
        target = rewards + (1.0 - dones.float()) * self.gamma * max_next_q

        loss = self.criterion(q_values, target.detach())
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def flatten_state(self, state):
        flat = np.zeros((10, 10))
        flat[state] = 1
        return flat.flatten()

    def step(self, state, action, maze):
        r, c = state
        dr, dc = configs.action_map[configs.actions[action]]
        nr, nc = r + dr, c + dc
        if 0 <= nr < 10 and 0 <= nc < 10 and maze[nr][nc] == 0:
            return (nr, nc)
        return state

    def run_path(self, path, maze):
        state = self.start
        for action in path:
            next_state = self.step(state, action, maze)
            state = next_state
            maze.draw_grid(self.window, maze, state, configs.goal)
            pygame.display.update()
            time.sleep(0.3)

