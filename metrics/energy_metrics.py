# energy_metrics.py

class EnergyMetrics:
    def __init__(self):
        self.total_energy_consumed = 0.0
        self.total_power_usage = 0.0
        self.total_infrastructure_efficiency = 0.0
        self.total_vm_count = 0

    def update_energy_consumption(self, energy):
        """ Update total energy consumed. """
        self.total_energy_consumed += energy

    def update_power_usage(self, power_usage):
        """ Update total power usage. """
        self.total_power_usage += power_usage

    def calculate_pue(self):
        """ Calculate Power Usage Effectiveness (PUE). """
        if self.total_power_usage > 0:
            return self.total_energy_consumed / self.total_power_usage
        return 0.0

    def calculate_dcie(self):
        """ Calculate Data Center Infrastructure Efficiency (DCiE). """
        pue = self.calculate_pue()
        if pue > 0:
            return 1 / pue * 100  # Convert to percentage
        return 0.0

    def add_vm_count(self, count):
        """ Update total VM count. """
        self.total_vm_count += count

    def reset_metrics(self):
        """ Reset metrics for new simulation. """
        self.total_energy_consumed = 0.0
        self.total_power_usage = 0.0
        self.total_infrastructure_efficiency = 0.0
        self.total_vm_count = 0
