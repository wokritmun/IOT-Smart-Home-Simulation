from ..smart_device import SmartDevice

class SmartLock(SmartDevice):
    POWER_USAGE = 10  # 10 watts when operating

    def __init__(self, device_id, broker_ip):
        super().__init__(device_id, broker_ip)
        self.lock_status = "locked"
        self.energy_consumed = 0

    def calculate_energy(self, operation_time):
        return (self.POWER_USAGE * operation_time) / 3600
        
    def lock(self, operation_time=5):  # default operation time is 5 seconds
        self.lock_status = "locked"
        self.energy_consumed += self.calculate_energy(operation_time)
        self.client.publish(f"{self.topic_base}/lock_status", "locked")

    def unlock(self, operation_time=5):
        self.lock_status = "unlocked"
        self.energy_consumed += self.calculate_energy(operation_time)
        self.client.publish(f"{self.topic_base}/lock_status", "unlocked")

    def report_energy_consumption(self):
        """Report total energy consumed by the blinds."""
        self.client.publish(f"{self.topic_base}/energy_consumption", str(self.energy_consumed))
        