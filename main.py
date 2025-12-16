# main.py
from environment import DisasterReliefEnv
from objective import evaluate_fitness
from optimizer import apply_swap_operator, apply_substitute_operator
from rl_agent import QLearningAgent

def run_rl_optimization(initial_solution, env, iterations=3000):
    current_solution = initial_solution
    current_score, _ = evaluate_fitness(current_solution, env)
    
    # Initialize the Brain
    # Action 0 = Swap, Action 1 = Substitute
    agent = QLearningAgent(num_actions=2)
    
    print(f"Starting Score: {current_score:.2f}")
    
    # Paper uses State 1 for Improvement, State 2 for No Change 
    state = 2 
    
    for i in range(iterations):
        # 1. Ask Agent what to do
        action = agent.choose_action(state)
        agent.last_action = action
        
        # 2. Perform the chosen operator
        if action == 0:
            candidate = apply_swap_operator(current_solution)
        else:
            candidate = apply_substitute_operator(current_solution, env)
            
        # 3. Evaluate Result
        if candidate is None:
            # Invalid move (e.g. constraints broken)
            reward = 0
            next_state = 2 # Failure state
        else:
            new_score, _ = evaluate_fitness(candidate, env)
            
            if new_score < current_score:
                # SUCCESS! Improvement found
                current_solution = candidate
                current_score = new_score
                reward = 1     # Reward = 1 
                next_state = 1 # State = 1 (Improved) 
                if i % 500 == 0:
                    print(f"Iter {i}: Improved via Action {action} -> {new_score:.2f}")
            else:
                # Failure (Score got worse or stayed same)
                reward = 0
                next_state = 2
                
        # 4. Teach the Agent
        agent.learn(next_state, reward)
        state = next_state
        
    return current_solution, current_score, agent

def main():
    print("--- Project 2: RL-PDSTA Disaster Logistics ---")
    
    # 1. Setup
    env = DisasterReliefEnv()
    print(f"Map: {len(env.targets)} Targets, {len(env.risk_zones)} Storms")
    
    initial_solution = env.generate_feasible_solution()
    initial_score, breakdown = evaluate_fitness(initial_solution, env)
    
    print(f"\n[Phase 1] Random Plan Score: {initial_score:.2f}")
    print(f"Distance: {breakdown[0]:.2f}km | Risk: {breakdown[2]:.2f}")
    
    # 2. Run RL Optimization
    print("\n[Phase 2] Training RL Agent to optimize plan...")
    best_sol, best_score, agent = run_rl_optimization(initial_solution, env)
    
    # 3. Final Analysis
    final_score, final_breakdown = evaluate_fitness(best_sol, env)
    improvement = ((initial_score - final_score) / initial_score) * 100
    
    print("-" * 30)
    print(f"FINAL RESULTS:")
    print(f"Score: {initial_score:.2f} -> {final_score:.2f} (Improved {improvement:.2f}%)")
    print(f"Final Dist: {final_breakdown[0]:.2f}km")
    print(f"Final Risk: {final_breakdown[2]:.2f}")
    
    # Inspect the Brain
    print("\n[Phase 3] What did the AI learn?")
    print("Q-Table Values (Higher = AI prefers this action):")
    print(f"State 'Improved' -> Swap Value: {agent.q_table[1][0]:.4f} | Sub Value: {agent.q_table[1][1]:.4f}")
    print(f"State 'Stagnant' -> Swap Value: {agent.q_table[2][0]:.4f} | Sub Value: {agent.q_table[2][1]:.4f}")

if __name__ == "__main__":
    main()