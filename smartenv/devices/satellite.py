# devices/satellite_comm.py
from ..smart_device import SmartDevice

class SmartSatelliteComm(SmartDevice):
    def __init__(self, device_id, broker_ip):
        super().__init__(device_id, broker_ip)
        self.signal_strength = 0  # percentage

    def update_signal_strength(self, value):
        """Updates the signal strength for communication."""
        self.signal_strength = value
        self.client.publish(f"{self.topic_base}/signal_strength", str(self.signal_strength))
