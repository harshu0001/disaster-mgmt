# config.py

# --- SIMULATION SETTINGS ---
MAP_SIZE = 100        # 100x100 km grid
NUM_TARGETS = 5       # Number of Survivor Clusters
NUM_RISK_ZONES = 3    # Number of Storms
RISK_RADIUS_RANGE = (10, 20) # Size of storms in km

# --- DRONE SETTINGS ---
# IDs 0 & 1 are "Search Drones" (Fast, Camera)
# IDs 2 & 3 are "Cargo Drones" (Heavy, Payload)
UAV_TYPES = {
    "Search": [0, 1],
    "Cargo":  [2, 3]
}

# --- TASK DEFINITIONS ---
# 0: Locate (Must be done first)
# 1: Deliver (Must be done second)
# 2: Assess (Must be done last)
TASK_STAGES = {
    0: "Locate",
    1: "Deliver",
    2: "Assess"
}

# [cite_start]Which drone can do which task? [cite: 63, 210-211]
# Search Drones do Locate(0) and Assess(2).
# Cargo Drones do Deliver(1).
CAPABILITY_MAP = {
    0: "Search",
    1: "Cargo",
    2: "Search"
}

# [cite_start]--- SCORING WEIGHTS [cite: 196] ---
# How important is each factor?
WEIGHT_DISTANCE = 0.5  # Flight distance
WEIGHT_TIME = 0.3      # Time taken
WEIGHT_RISK = 0.2      # Flying through storms