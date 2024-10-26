# allocation.py

from rl_agent.rl_agent import RLAgent
from models.cloud_environment import CloudEnvironment
from metrics.energy_metrics import EnergyMetrics

class ResourceAllocator:
    def __init__(self, cloud_environment: CloudEnvironment, agent: RLAgent, metrics: EnergyMetrics):
        self.cloud_environment = cloud_environment
        self.agent = agent
        self.metrics = metrics

    def allocate_resources(self, workload):
        """ Allocate resources to VMs based on workload using the RL agent. """
        for vm in self.cloud_environment.vm_list:
            # Assume 'workload' is a dict with VM ID as key and CPU demand as value
            cpu_demand = workload.get(vm.vm_id, 0)
            host = self.agent.select_host(vm, self.cloud_environment.host_list)

            if host is not None:
                self.cloud_environment.assign_vm_to_host(vm, host)
                energy_used = self.cloud_environment.calculate_energy_consumption(host)
                self.metrics.update_energy_consumption(energy_used)
                self.metrics.add_vm_count(1)

    def report_metrics(self):
        """ Report the performance metrics after allocation. """
        pue = self.metrics.calculate_pue()
        dcie = self.metrics.calculate_dcie()
        print(f"PUE: {pue:.2f}, DCiE: {dcie:.2f}, Total Energy Consumed: {self.metrics.total_energy_consumed:.2f} kWh")
