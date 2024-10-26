# models/cloud_environment.py

class CloudEnvironment:
    def __init__(self, hosts, vms):
        self.hosts = hosts  # List of host machines
        self.vms = vms      # List of virtual machines
        self.current_utilization = {host.id: 0 for host in hosts}  # Initialize utilization for each host

    def allocate_vm(self, vm):
        best_host = self.find_best_host(vm)
        if best_host:
            best_host.allocate_vm(vm)
            self.current_utilization[best_host.id] += vm.cpu_demand
            print(f"Allocated VM {vm.id} to Host {best_host.id}")
        else:
            print(f"No suitable host found for VM {vm.id}")

    def find_best_host(self, vm):
        # Implement logic to find the best host based on VM requirements
        best_host = None
        for host in self.hosts:
            if host.can_host(vm):
                if best_host is None or host.get_utilization() < best_host.get_utilization():
                    best_host = host
        return best_host

    def get_overall_utilization(self):
        total_utilization = sum(self.current_utilization.values())
        total_hosts = len(self.hosts)
        return total_utilization / total_hosts if total_hosts > 0 else 0

    def reset_utilization(self):
        self.current_utilization = {host.id: 0 for host in self.hosts}  # Reset utilization

