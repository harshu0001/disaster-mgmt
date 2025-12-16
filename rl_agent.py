# rl_agent.py
import random
import numpy as np

class QLearningAgent:
    def __init__(self, num_actions=2, alpha=0.5, gamma=0.9, epsilon=0.1):
        """
        Hyperparameters from the paper[cite: 1216]:
        alpha (Learning Rate): 0.5
        gamma (Discount Factor): 0.9
        """
        self.q_table = np.zeros((3, num_actions)) # Rows: States (0,1,2), Cols: Actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon # Exploration rate
        self.last_action = None
        self.last_state = 0 # Start in neutral state

    def choose_action(self, state):
        """
        Decide whether to Swap (0) or Substitute (1).
        Uses Epsilon-Greedy strategy (Explore vs Exploit).
        """
        if random.uniform(0, 1) < self.epsilon:
            return random.randint(0, 1) # Explore: Random action
        else:
            return np.argmax(self.q_table[state]) # Exploit: Best known action

    def learn(self, current_state, reward):
        """
        Update the Q-Table using the Bellman Equation.
        Q_new = Q_old + alpha * (Reward + gamma * max(Q_next) - Q_old)
        """
        if self.last_action is not None:
            old_value = self.q_table[self.last_state, self.last_action]
            next_max = np.max(self.q_table[current_state])
            
            new_value = old_value + self.alpha * (reward + self.gamma * next_max - old_value)
            self.q_table[self.last_state, self.last_action] = new_value
            
        self.last_state = current_state