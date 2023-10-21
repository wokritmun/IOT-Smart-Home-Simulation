# devices/cooking_fire.py
from ..smart_device import SmartDevice

class SmartCookingFire(SmartDevice):
    def __init__(self, device_id, broker_ip):
        super().__init__(device_id, broker_ip)
        self.fire_status = "OFF"
    
    def ignite(self):
        """Starts the fire for cooking."""
        self.fire_status = "ON"
        self.client.publish(f"{self.topic_base}/fire_status", self.fire_status)
    
    def extinguish(self):
        """Stops the fire."""
        self.fire_status = "OFF"
        self.client.publish(f"{self.topic_base}/fire_status", self.fire_status)
