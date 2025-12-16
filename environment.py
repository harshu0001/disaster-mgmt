# environment.py
import random
import numpy as np
import config

class DisasterReliefEnv:
    def __init__(self):
        self.targets = list(range(1, config.NUM_TARGETS + 1))
        
        # 1. Generate Coordinates for Base and Targets
        # Base Station is at (0,0)
        self.locations = {0: (0, 0)} 
        for t in self.targets:
            self.locations[t] = (
                random.randint(0, config.MAP_SIZE), 
                random.randint(0, config.MAP_SIZE)
            )
            
        # 2. Generate Storm Zones (Risk Areas)
        # Format: (x, y, radius)
        self.risk_zones = []
        for _ in range(config.NUM_RISK_ZONES):
            self.risk_zones.append((
                random.randint(20, 80),
                random.randint(20, 80),
                random.randint(*config.RISK_RADIUS_RANGE)
            ))

    def get_valid_uav(self, task_stage):
        """Finds a random UAV capable of performing the specific task stage."""
        required_type = config.CAPABILITY_MAP[task_stage]
        candidates = config.UAV_TYPES[required_type]
        return random.choice(candidates)

    def generate_feasible_solution(self):
        """
        [cite_start]Implements Algorithm 1 [cite: 332-341].
        Generates a random but VALID sequence where Locate comes before Deliver.
        """
        # Track pending tasks: [0=Locate, 1=Deliver, 2=Assess]
        remaining_tasks = {t: [0, 1, 2] for t in self.targets}
        
        genome = [] # Stores the plan: [TaskID, UavID, Cost, TargetID]
        active_targets = list(self.targets)
        
        while active_targets:
            # [cite_start]Randomly pick a target that needs help [cite: 334]
            selected_target = random.choice(active_targets)
            
            # Enforce Order: Always pop the first available task (0->1->2)
            task_stage = remaining_tasks[selected_target].pop(0)
            
            # Create Unique Task ID
            global_task_id = (selected_target - 1) * 3 + (task_stage + 1)

            # [cite_start]Assign a compatible UAV [cite: 335]
            uav_id = self.get_valid_uav(task_stage)
            
            # [cite_start]Assign random Cost (Time to complete task) [cite: 336]
            cost = round(random.uniform(10, 50), 1)

            # Save step: [Task_ID, UAV_ID, Cost, Target_ID]
            genome.append([global_task_id, uav_id, cost, selected_target])
            
            # If target has no tasks left, remove from active list
            if not remaining_tasks[selected_target]:
                active_targets.remove(selected_target)

        return genome