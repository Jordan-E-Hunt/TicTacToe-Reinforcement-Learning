from src.environment import TicTacToe
from src.agent import QLearningAgent

class QLearningAgent:
  def __init__(self, alpha=0.2, epsilon=1.0,
               discount=0.95, epsilon_min=0.01, epsilon_decay=0.99996):
    self.Q = {}
    self.alpha = alpha
    self.epsilon = epsilon
    self.discount = discount
    self.epsilon_min = epsilon_min
    self.epsilon_decay = epsilon_decay

 def get_Q_value(self, state, action):
    return self.Q.get((state, action), 0.0) #Return 0.0 if no state, action pair

 def choose_action(self, state, avail_moves):
    if random.uniform(0,1) < self.epsilon:
      return random.choice(avail_moves)
    else:
      Q_values = [self.get_Q_value(state, action) for action in avail_moves]
      max_Q = max(Q_values)
      if Q_values.count(max_Q) > 1:
        best_moves = [i for i in range(len(avail_moves)) if Q_values[i] == max_Q]
        i = random.choice(best_moves)
      else:
        i = Q_values.index(max_Q)
      return avail_moves[i]

 def update_Q_value(self, state, action, reward, next_state, next_avail_moves):
    if not next_avail_moves:
      max_next_Q = 0.0
    else:
      next_Q_values = [self.get_Q_value(next_state, next_action) for next_action in next_avail_moves]
      max_next_Q = max(next_Q_values)

    current_Q = self.get_Q_value(state, action)
    td_error = reward + self.discount * max_next_Q - current_Q
    new_Q = current_Q + self.alpha * td_error

    self.Q[(state, action)] = new_Q

 def decay_epsilon(self):
    self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

 def decay_alpha(self, episode, total_episodes, start_alpha):
    # Linear decay from start_alpha down to 0.01
    min_alpha = 0.01
    self.alpha = max(min_alpha, start_alpha - (start_alpha - min_alpha) * (episode / total_episodes))

 def save_policy(self, filename="policy.pkl"):
    with open(filename, 'wb') as f:
      pickle.dump(self.q_table, f)

 def load_policy(self, filename="policy.pkl"):
    with open(filename, 'rb') as f:
      self.q_table = pickle.load(f)                   