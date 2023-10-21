from ..smart_device import SmartDevice
class SmartDoorbell(SmartDevice):
    POWER_USAGE = 5  # 5 watts when ringing

    def __init__(self, device_id, broker_ip):
        super().__init__(device_id, broker_ip)
        self.ringing = False
        self.energy_consumed = 0

    def calculate_energy(self, ring_duration):
        return (self.POWER_USAGE * ring_duration) / 3600
        
    def ring(self, ring_duration):
        self.ringing = True
        self.energy_consumed += self.calculate_energy(ring_duration)
        self.client.publish(f"{self.topic_base}/ringing", "True")
        
    def stop_ring(self):
        self.ringing = False
        self.client.publish(f"{self.topic_base}/ringing", "False")

    def report_energy_consumption(self):
        """Report total energy consumed by the blinds."""
        self.client.publish(f"{self.topic_base}/energy_consumption", str(self.energy_consumed))
