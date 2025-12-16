# optimizer.py
import random
import copy
import config

def check_constraints(solution):
    """
    Validation Logic [cite: 225-227, 210-213].
    Ensures a solution (Genome) obeys two main rules:
    1. Precedence: Locate < Deliver < Assess for every target.
    2. Capability: Search Drones don't do Cargo tasks.
    """
    # Track the last completed stage for each target
    # -1 = Not started, 0 = Located, 1 = Delivered, 2 = Assessed
    target_progress = {t: -1 for t in range(1, config.NUM_TARGETS + 1)}
    
    for step in solution:
        # Step format: [TaskID, UavID, Cost, TargetID]
        target_id = step[3]
        uav_id = step[1]
        
        # Decode the task type (0, 1, or 2) from the TaskID
        # We reversed the ID formula: Task_Stage = (TaskID - 1) % 3
        # E.g. Task 1 -> (0) Locate. Task 2 -> (1) Deliver.
        task_stage = (step[0] - 1) % 3
        
        # RULE 1: Precedence Check
        # The current task_stage must be exactly 1 greater than previous progress
        if task_stage != target_progress[target_id] + 1:
            return False # Invalid order (e.g., Deliver before Locate)
        
        # Update progress
        target_progress[target_id] = task_stage
        
        # RULE 2: Capability Check
        required_type = config.CAPABILITY_MAP[task_stage]
        if uav_id not in config.UAV_TYPES[required_type]:
            return False # Wrong drone type
            
    return True

def apply_swap_operator(solution):
    """
    Operator A [cite: 409-412].
    Randomly swaps two tasks in the timeline.
    Returns the new solution if valid, otherwise returns None.
    """
    new_solution = copy.deepcopy(solution)
    n = len(new_solution)
    
    # Pick two random indices to swap
    idx1, idx2 = random.sample(range(n), 2)
    
    # Perform the swap (Task, UAV, Cost, Target all move together)
    new_solution[idx1], new_solution[idx2] = new_solution[idx2], new_solution[idx1]
    
    # Check if this swap broke the rules
    if check_constraints(new_solution):
        return new_solution
    else:
        return None # Swap failed validation

def run_optimization(initial_solution, env, evaluate_fn, iterations=1000):
    """
    Simple Hill Climbing Loop.
    1. Tries to Swap.
    2. If the new plan has a better (lower) score, keep it.
    """
    current_solution = initial_solution
    current_score, _ = evaluate_fn(current_solution, env)
    
    print(f"Starting Score: {current_score:.2f}")
    
    for i in range(iterations):
        # 1. Try to modify the solution
        candidate = apply_swap_operator(current_solution)
        
        # 2. If modification was valid (not None)
        if candidate is not None:
            # 3. Grade the new solution
            new_score, _ = evaluate_fn(candidate, env)
            
            # 4. Acceptance Criteria (Is it better?)
            if new_score < current_score:
                print(f"Iter {i}: Improved Score {current_score:.2f} -> {new_score:.2f}")
                current_solution = candidate
                current_score = new_score
                
    return current_solution, current_score



def apply_substitute_operator(solution, env):
    """
    Operator C.
    Instead of changing the order, we change the RESOURCE (The UAV).
    Useful for balancing load (e.g., if Drone A is doing too much, give task to Drone B).
    """
    new_solution = copy.deepcopy(solution)
    
    # 1. Pick a random step to modify
    idx = random.randint(0, len(new_solution) - 1)
    step = new_solution[idx]
    
    # Step format: [TaskID, UavID, Cost, TargetID]
    task_id = step[0]
    
    # 2. Identify Task Type (0=Locate, 1=Deliver, 2=Assess)
    task_stage = (task_id - 1) % 3
    
    # 3. Find OTHER compatible UAVs
    # We look up which type (Search/Cargo) is required
    req_type = config.CAPABILITY_MAP[task_stage]
    candidates = config.UAV_TYPES[req_type]
    
    # 4. Assign a new random UAV from the candidate list
    new_uav = random.choice(candidates)
    
    # Update the step
    new_solution[idx][1] = new_uav
    
    # No need to check constraints here because we forced a compatible choice.
    # But for safety/consistency, we can return it directly.
    return new_solution