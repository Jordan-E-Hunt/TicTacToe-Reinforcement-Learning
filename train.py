from src.environment import TicTacToe
from src.agent import QLearningAgent
import random

def train(num_episodes, alpha = 0.2, epsilon = 1.0, discount = 0.95):
  agent = QLearningAgent(alpha, epsilon, discount)
  for i in range(num_episodes):
    game = TicTacToe()
    agent.discount = discount

    #10% chance of random training, 50% who goes first
    training_against_random = [random.random() < 0.5, random.random() < 0.5]

    #Dictionaries for memory
    prev_state = { "X": None, "O": None }
    prev_action = { "X": None, "O": None }
    prev_reward = { "X": None, "O": None }

    while not game.game_over:
      cur_player = game.current # "X" or "O"
      opp_player = "O" if cur_player == "X" else "X"

      state = game.get_state() 
      avail_moves = game.avail_moves()

      if training_against_random[0] and training_against_random[1]:
        action = random.choice(avail_moves)
        training_against_random[1] = False
      elif training_against_random[0]:
        action = agent.choose_action(state, avail_moves)
        training_against_random[1] = True
      else:
        action = agent.choose_action(state, avail_moves)

      next_state, reward, done, _ = game.make_move(action)
      avail_moves = game.avail_moves()
      
      if game.winner is not None: #If there is a winner, update both
        agent.update_Q_value(state, action, reward, next_state, [])

        other_reward = -2.0 if not game.winner == "Draw" else reward
        agent.update_Q_value(prev_state[opp_player], prev_action[opp_player], 
                            other_reward, tuple(-s for s in next_state), [])
        
      elif prev_state[opp_player] is not None: #If opponent has previous state
        agent.update_Q_value(prev_state[opp_player], prev_action[opp_player], 
                            prev_reward[opp_player], next_state, avail_moves)

      
      prev_state[cur_player] = state
      prev_action[cur_player] = action
      prev_reward[cur_player] = reward

    agent.decay_epsilon()
    agent.decay_alpha(i, num_episodes, alpha) 

  return agent                   

#Train the Q-learning agent
agent = train(num_episodes= 100000, alpha=0.2 , epsilon= 1.0, discount=1.0)

agent.save_policy("models/best_agent.pkl")
print("Training complete. Model saved to models/best_agent.pkl")