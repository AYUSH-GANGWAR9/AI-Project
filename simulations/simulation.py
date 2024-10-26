# simulation.py

import random
from models.cloud_environment import CloudEnvironment
from rl_agent.rl_agent import RLAgent
from metrics.energy_metrics import EnergyMetrics
from resource_allocation.allocation import ResourceAllocator

class CloudSimulation:
    def __init__(self, cloud_environment: CloudEnvironment, agent: RLAgent, metrics: EnergyMetrics):
        self.cloud_environment = cloud_environment
        self.agent = agent
        self.metrics = metrics
        self.allocator = ResourceAllocator(cloud_environment, agent, metrics)

    def generate_workload(self, num_vms):
        """ Simulate generating random workload for a given number of VMs. """
        workload = {}
        for i in range(num_vms):
            workload[f'vm_{i}'] = random.randint(100, 1000)  # Random CPU demand in million instructions
        return workload

    def run_simulation(self, num_vms, days):
        """ Run the simulation for a specified number of VMs over a number of days. """
        for day in range(days):
            print(f"Day {day + 1}:")
            workload = self.generate_workload(num_vms)
            self.allocator.allocate_resources(workload)
            self.allocator.report_metrics()

if __name__ == "__main__":
    # Assuming the models and agents have been initialized properly
    cloud_env = CloudEnvironment()
    agent = RLAgent()
    metrics = EnergyMetrics()
    
    simulation = CloudSimulation(cloud_env, agent, metrics)
    simulation.run_simulation(num_vms=200, days=7)
