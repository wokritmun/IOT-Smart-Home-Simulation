# devices/camera.py
from ..smart_device import SmartDevice

class SmartCamera(SmartDevice):
    def __init__(self, device_id, broker_ip):
        super().__init__(device_id, broker_ip)
        self.motion_detected = False

    def detect_motion(self, motion_status):
        """Updates motion detection status."""
        self.motion_detected = motion_status
        self.client.publish(f"{self.topic_base}/motion_detected", str(self.motion_detected))
