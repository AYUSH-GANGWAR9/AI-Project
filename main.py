# main.py

from models.cloud_environment import CloudEnvironment
from rl_agent.rl_agent import RLAgent
from resource_allocation.allocation import allocate_resources
from simulations.simulation import run_simulation

def main():
    # Initialize the cloud environment
    cloud_env = CloudEnvironment(host_count=200, vm_count=150)

    # Initialize the reinforcement learning agent
    rl_agent = RLAgent(cloud_env)

    # Set up the simulation parameters
    simulation_days = 7
    workload_data = cloud_env.get_workload_data()

    # Add this print statement to check the workload data
    print(f"Workload Data: {workload_data}")

    # Run the simulation for the specified number of days
    for day in range(simulation_days):
        print(f"Running simulation for Day {day + 1}...")
        
        # Allocate resources using the RL agent
        allocated_resources = allocate_resources(rl_agent, workload_data[day])
        
        # Run the simulation for allocated resources
        run_simulation(cloud_env, allocated_resources)

        # Calculate and print performance metrics
        cloud_env.calculate_metrics()


if __name__ == "__main__":
    main()
