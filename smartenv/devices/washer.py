from ..smart_device import SmartDevice

class SmartWasher(SmartDevice):
    def __init__(self, device_id, broker_ip):
        super().__init__(device_id, broker_ip)
        self.cycle_status = "Idle"  # Default cycle status

    def set_cycle(self, cycle):
        """Set the washer's current cycle."""
        self.cycle_status = cycle
        self.client.publish(f"{self.topic_base}/cycle_status", cycle)

    def calculate_power_consumption(self):
        """Calculate power based on the cycle status."""
        if self.cycle_status == "Washing":
            return 50  # Power usage during washing cycle (hypothetical value)
        elif self.cycle_status == "Rinsing":
            return 40  # Power usage during rinsing cycle (hypothetical value)
        elif self.cycle_status == "Spinning":
            return 60  # Power usage during spinning cycle (hypothetical value)
        else:
            return 0  # No power consumption when idle

    def report_power_consumption(self):
        """Publish power consumption data to MQTT."""
        power_data = self.calculate_power_consumption()
        self.client.publish(f"{self.topic_base}/power_consumption", power_data)