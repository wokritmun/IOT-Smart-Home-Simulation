from ..smart_device import SmartDevice
from .solar import SmartSolarPanel 

class SmartBattery(SmartDevice):
    CHARGE_RATE = 0.5  # kWh per hour
    DISCHARGE_RATE = 0.6  # kWh per hour
    MAX_CYCLES = 5000  # After which the battery starts to degrade
    DEGRADATION_RATE = 0.002  # 0.2% reduction in max capacity after each cycle beyond MAX_CYCLES

    def __init__(self, device_id, broker_ip, panel: SmartSolarPanel = None, max_capacity=10.0):
        super().__init__(device_id, broker_ip)
        self.max_capacity = max_capacity 
        self.stored_energy = 0.0  # kWh
        self.charge_level = 0  # percentage
        self.panel = panel
        self.cycles = 0

    def charge_from_panel(self):
        if self.panel:
            available_energy = min(self.CHARGE_RATE, self.panel.energy_production)
            self.update_stored_energy(self.stored_energy + available_energy)
            self.cycles += 1
            if self.cycles > self.MAX_CYCLES:
                self.degrade_battery()
            print(f"Charged battery with {available_energy} kWh from solar panel.")

    def discharge(self, required_energy):
        energy_to_discharge = min(self.DISCHARGE_RATE, required_energy)
        if self.stored_energy >= energy_to_discharge:
            self.stored_energy -= energy_to_discharge
            self.update_stored_energy(self.stored_energy)
            return energy_to_discharge
        return 0

    def degrade_battery(self):
        self.max_capacity -= (self.max_capacity * self.DEGRADATION_RATE)
    
    def update_stored_energy(self, value):
        self.stored_energy = min(value, self.max_capacity)  # Ensure stored energy never exceeds max capacity
        self.charge_level = int((self.stored_energy / self.max_capacity) * 100)
        self.client.publish(f"{self.topic_base}/stored_energy", str(self.stored_energy))
        self.client.publish(f"{self.topic_base}/charge_level", str(self.charge_level))

