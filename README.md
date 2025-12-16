# Disaster Relief Logistics Optimization (RL-PDSTA)
A Python implementation of the RL-PDSTA (Reinforcement Learning and Population-based Discrete State Transition Algorithm) adapted for humanitarian disaster relief.This project solves the Multi-UAV Cooperative Task Allocation Problem (M-CMTAP). It uses an intelligent "Brain" (Q-Learning Agent) to dynamically schedule a fleet of heterogeneous drones (Search Drones vs. Cargo Drones) to Locate, Deliver Supplies, and Assess survivors in a disaster zone while avoiding dangerous storm risks.
## 📌 Project Overview
This project is based on the research paper: 
"A reinforcement learning and population-based discrete state transition algorithm for solving the multi-UAV task allocation problem with complex constraints"

We have translated the military logic into a civilian context:

| Research Term | Civilian Adaptation | Description |
| :--- | :--- | :--- |
| **Target ($T$)** | **Survivor Cluster** | [cite_start]A location requiring aid[cite: 133]. |
| **Observe ($M_1$)** | **Locate Task** | [cite_start]Verify coordinates (requires camera) [cite: 136-137]. |
| **Attack ($M_2$)** | **Deliver Task** | [cite_start]Drop supplies (requires payload) [cite: 136-137]. |
| **Evaluate ($M_3$)** | **Assess Task** | [cite_start]Verify success (requires camera) [cite: 136-137]. |
| **Scout UAV** | **Search Drone** | [cite_start]Fast, light drone for *Locate* and *Assess* tasks[cite: 140]. |
| **Fight UAV** | **Cargo Drone** | [cite_start]Heavy drone for *Deliver* tasks[cite: 140]. |
| **Radar Zone** | **Storm Zone** | [cite_start]Dangerous weather area to avoid [cite: 176-179]. |

## 📂 Project Structure

DisasterReliefOptimizer/
│
├── config.py           # Central configuration (Map size, Drone types, Task definitions)
├── environment.py      # Map generation and Logic for creating valid mission plans
├── objective.py        # The "Scorecard" - Calculates Distance, Time, and Risk
├── optimizer.py        # The "Mechanic" - Swaps tasks and reassigns drones
├── rl_agent.py         # The "Brain" - Q-Learning agent that learns which operator to use
├── main.py             # Entry point - Runs the full simulation
└── requirements.txt    # Dependencies

## 🚀 Installation & Usage
Prerequisites: Ensure you have Python installed.
Install Dependencies:Bash :- pip install -r requirements.txt
(Note: numpy is the primary requirement).
Run the Simulation:Bash :- python main.py

## 🧠 How It Works (Detailed File Breakdown)
1. config.py
    This file acts as the control center. It defines the "Rules of Engagement":
    Constraints: Defines that Search Drones can only perform Locate (Stage 0) and Assess (Stage 2) tasks, while Cargo Drones handle Deliver (Stage 1)
    Weights: Sets how much we care about Distance vs. Time vs. Risk ($w_1, w_2, w_3$) 
2. environment.py
   This file handles the Feasible Initialization.
    Map Generation: Randomly places Survivors and Storm Zones.
    Algorithm 1 Implementation: Instead of creating a random invalid schedule, this generates a mathematically valid schedule by forcing the order: Locate -> Deliver -> Assess

3. objective.py
    This calculates the Fitness Score (lower is better).
    Distance (f1): Calculates the total Euclidean distance flown by all drones 4.
    Risk (f3): Calculates a penalty if a flight path intersects a Storm Zone (adapted from Radar Detection)
    Total Fitness: Combines these metrics using a Weighted Sum approach.
4. optimizer.py
    This contains the Operators that modify the plan to find better solutions.
    Constraint Checking: Ensures no modification breaks the rules (e.g., ensuring supplies aren't delivered before the survivor is found).
    Swap Operator (Operator A): Swaps two tasks in the timeline to reduce flight distance .
    Substitute Operator (Operator C): Reassigns a task to a different compatible drone to balance the workload .
5. rl_agent.py
    This implements the Reinforcement Learning logic .
    Q-Learning: The agent maintains a Q-Table to track which action (Swap vs. Substitute) yields better rewards in specific states.
    State Space: Simple binary states based on whether the previous iteration improved the score or not ($S=1$ for improvement, $S=2$ for none)11.
    Reward System: Gives the agent +1 point if it lowers the mission cost, 0 if it fails .
6. main.py
    The execution loop:
    Initializes the map.
    Generates a random valid plan.
    Runs the Optimization Loop for 3,000+ iterations.
    Prints the improvement percentage and what the AI learned (Q-Table values).

## 📜 Citation
This code is based on the logic presented in:
Zhou, X., Xia, R., & Huang, T. (2025). A reinforcement learning and population-based discrete state transition algorithm for solving the multi-UAV task allocation problem with complex constraints. Knowledge-Based Systems, 325, 113910.