from ..smart_device import SmartDevice

class SmartRefrigerator(SmartDevice):
    def __init__(self, device_id, broker_ip):
        super().__init__(device_id, broker_ip)
        self.current_temperature = 37  # Default temperature in Fahrenheit
        self.door_open = False  # Track the door status

    def set_temperature(self, temp):
        """Set the refrigerator's temperature."""
        self.current_temperature = temp
        self.client.publish(f"{self.topic_base}/temperature", temp)

    def open_door(self):
        """Handle the event when the refrigerator door is opened."""
        self.door_open = True
        self.client.publish(f"{self.topic_base}/door_status", "OPEN")

    def close_door(self):
        """Handle the event when the refrigerator door is closed."""
        self.door_open = False
        self.client.publish(f"{self.topic_base}/door_status", "CLOSED")

    def calculate_power_consumption(self):
        """Calculate power based on door and temperature status."""
        if self.door_open:
            return 20  # Power usage is high when door is open (hypothetical value)
        elif self.current_temperature > 40:
            return 15  # Power usage is higher when the refrigerator is warmer (hypothetical value)
        else:
            return 10  # Base power consumption (hypothetical value)

    def report_power_consumption(self):
        """Publish power consumption data to MQTT."""
        power_data = self.calculate_power_consumption()
        self.client.publish(f"{self.topic_base}/power_consumption", power_data)




