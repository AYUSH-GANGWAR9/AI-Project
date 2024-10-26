# models/power_model.py

class PowerModel:
    def __init__(self, base_power, max_power, efficiency_curve):
        self.base_power = base_power  # Base power consumption when idle
        self.max_power = max_power      # Maximum power consumption
        self.efficiency_curve = efficiency_curve  # Efficiency curve coefficients

    def calculate_power(self, utilization):
        """
        Calculate the power consumption based on host utilization.
        Utilization is a value between 0 and 1.
        """
        if utilization < 0:
            utilization = 0
        elif utilization > 1:
            utilization = 1

        # Using a simple model to estimate power based on utilization
        power = self.base_power + (self.max_power - self.base_power) * (utilization ** self.efficiency_curve)
        return power

    def calculate_energy(self, power, time):
        """
        Calculate the energy consumed over a period of time.
        Power is in kW, time is in hours.
        """
        energy = power * time  # Energy = Power x Time
        return energy
