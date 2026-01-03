import os
import sys
import time
import random
import pickle

from src.environment import TicTacToe
from src.agent import QLearningAgent

def clear_screen():
    
    os.system('cls' if os.name == 'nt' else 'clear')

def play(agent):
    game = TicTacToe()
    #Randomly decide if human starts as X
    human_is_x = random.random() < 0.5 
    save_ep = agent.epsilon
    agent.epsilon = 0 
    
    setup_msg = "--- Randomized Start ---\n"
    if human_is_x:
        setup_msg += "You are X (Starting Player)\n"
    else:
        setup_msg += "AI is X (Starting Player). You are O.\n"
    setup_msg += "------------------------\n"

    while not game.game_over:
        clear_screen() 
        print(setup_msg)
        game.print_board()

        #Determine current turn
        if (game.current == "X" and human_is_x) or \
           (game.current == "O" and not human_is_x):
            
            sys.stdout.flush() 
            time.sleep(0.1)

            try:
                move_input = input(f"Your move ({game.current}) [row,col]: ")
                action = tuple(map(int, move_input.split(',')))
                
                if action not in game.avail_moves():
                    print("Invalid move. Try again.")
                    time.sleep(1)
                    continue
                
                game.make_move(action)
            except (ValueError, IndexError):
                print("Error: Please enter coordinates as 'row,col' (e.g., 0,0)")
                time.sleep(1.5)
                continue
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                time.sleep(2)
                continue
        else:
            #AI Logic
            print(f"AI ({game.current}) is thinking...")
            time.sleep(0.8) 
            
            state = game.get_state()
            action = agent.choose_action(state, game.avail_moves()) 
            
            game.make_move(action)
            print(f"AI chose: {action}")
            time.sleep(1.2)

    #Final result screen
    clear_screen()
    print(setup_msg)
    game.print_board()
    
    if game.winner == "Draw":
        print("\nIt's a Draw.")
    else:
        human_won = (game.winner == "X" and human_is_x) or \
                    (game.winner == "O" and not human_is_x)
        print(f"\nWinner: {'You' if human_won else 'AI'} ({game.winner})")

    agent.epsilon = save_ep

if __name__ == "__main__":
    #Load the trained agent from pickle file
    MODEL_PATH = 'models/q_table.pkl'
    
    # Initialize a blank agent
    trained_agent = QLearningAgent()
    
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            trained_agent.q_table = pickle.load(f)
        print("Successfully loaded trained agent.")
        time.sleep(1)
        play(trained_agent)
    else:
        print(f"ERROR: Model file not found at {MODEL_PATH}")
        print("Please run your training script first to save the agent.")