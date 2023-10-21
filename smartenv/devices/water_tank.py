# devices/water_tank.py
from ..smart_device import SmartDevice

class SmartWaterTank(SmartDevice):
    def __init__(self, device_id, broker_ip):
        super().__init__(device_id, broker_ip)
        self.water_level = 0.0  # liters

    def update_water_level(self, value):
        """Updates water level in the tank."""
        self.water_level = value
        self.client.publish(f"{self.topic_base}/water_level", str(self.water_level))
