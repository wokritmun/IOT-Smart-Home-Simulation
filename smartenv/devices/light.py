from ..smart_device import SmartDevice
from threading import Timer


class SmartLight(SmartDevice):
    def __init__(self, device_id, broker_ip):
        super().__init__(device_id, broker_ip)
        self.brightness = 100  # Percentage, 100% being the brightest
        self.color = "white"  # Default color
        self.inactivity_timer = None

    def set_brightness(self, level):
        """Set the light's brightness."""
        self.brightness = level
        self.client.publish(f"{self.topic_base}/brightness", level)

    def change_color(self, color):
        """Change the light color."""
        self.color = color
        self.client.publish(f"{self.topic_base}/color", color)

    def activate_sleep_mode(self, duration):
        """Turn off the light after a certain duration of inactivity."""
        if self.inactivity_timer:
            self.inactivity_timer.cancel()  # Reset the timer if already active

        self.inactivity_timer = Timer(duration, self.turn_off)
        self.inactivity_timer.start()

    def calculate_power_consumption(self):
        """Calculate power based on brightness."""
        base_consumption = 10  # Hypothetical base power consumption
        return base_consumption * (self.brightness / 100)