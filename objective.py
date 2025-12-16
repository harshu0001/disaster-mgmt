# objective.py
import math
import config

def calculate_distance(p1, p2):
    """Euclidean distance between two points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def calculate_risk_exposure(p1, p2, risk_zones):
    """
    Checks if a flight path intersects a Storm Zone.
    [cite_start]Simplified 'Radar Detection' logic [cite: 180-183].
    """
    penalty = 0
    # Check midpoint of path against every storm
    midpoint = ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2)
    
    for (zx, zy, r) in risk_zones:
        dist_to_zone = calculate_distance(midpoint, (zx, zy))
        if dist_to_zone < r:
            # Add penalty if inside the radius
            penalty += (r - dist_to_zone) * 10
            
    return penalty

def evaluate_fitness(solution, env):
    """
    [cite_start]Calculates the 3 objectives[cite: 164, 172, 186].
    """
    total_dist = 0
    total_time = 0
    total_risk = 0

    # Group tasks by UAV to see where each drone flies
    # Flatten the list of lists from config
    all_uav_ids = [u for sublist in config.UAV_TYPES.values() for u in sublist]
    uav_paths = {u_id: [] for u_id in all_uav_ids}
    
    # 'solution' is a list of [TaskID, UavID, Cost, TargetID]
    for step in solution:
        u_id = step[1]
        cost = step[2]
        target_id = step[3]
        
        uav_paths[u_id].append(target_id)
        total_time += cost # Objective 2: Time Cost

    # Calculate Flight Path Metrics
    for u_id, path in uav_paths.items():
        if not path:
            continue
            
        # Start at Base (0,0)
        current_pos = env.locations[0]
        
        for target_id in path:
            next_pos = env.locations[target_id]
            
            # Obj 1: Distance
            total_dist += calculate_distance(current_pos, next_pos)
            
            # Obj 3: Risk
            total_risk += calculate_risk_exposure(current_pos, next_pos, env.risk_zones)
            
            current_pos = next_pos
            
        # Return to Base
        total_dist += calculate_distance(current_pos, env.locations[0])

    # [cite_start]Final Weighted Score (Minimize this!) [cite: 196]
    fitness = (config.WEIGHT_DISTANCE * total_dist) + \
              (config.WEIGHT_TIME * total_time) + \
              (config.WEIGHT_RISK * total_risk)
    
    return fitness, (total_dist, total_time, total_risk)