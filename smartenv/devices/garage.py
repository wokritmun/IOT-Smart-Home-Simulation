from ..smart_device import SmartDevice

class SmartGarageDoor(SmartDevice):
    POWER_USAGE = 150  # 150 watts when operating

    def __init__(self, device_id, broker_ip):
        super().__init__(device_id, broker_ip)
        self.door_status = "closed"
        self.energy_consumed = 0

    def calculate_energy(self, operation_time):
        return (self.POWER_USAGE * operation_time) / 3600
        
    def open_door(self, operation_time=20):
        self.door_status = "open"
        self.energy_consumed += self.calculate_energy(operation_time)
        self.client.publish(f"{self.topic_base}/door_status", "open")
        
    def close_door(self,operation_time=20):
        self.door_status = "closed"
        self.energy_consumed += self.calculate_energy(operation_time)
        self.client.publish(f"{self.topic_base}/door_status", "closed")

    def report_energy_consumption(self):
        """Report total energy consumed by the blinds."""
        self.client.publish(f"{self.topic_base}/energy_consumption", str(self.energy_consumed))