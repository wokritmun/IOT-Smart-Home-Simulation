# devices/cooling_system.py
from ..smart_device import SmartDevice
from ..weather_util import get_weather_data

class SmartCoolingSystem(SmartDevice):
    def __init__(self, device_id, broker_ip):
        super().__init__(device_id, broker_ip)
        self.current_temperature = 30.0  # default temperature in Celsius
        self.desired_temperature = 24.0  # desired temperature
        self.mode = "off"  # Initial mode

    def fetch_and_update_current_temperature(self):
        """Fetches the external temperature and updates the system's state."""
        weather_data = get_weather_data()
        if 'hourly' in weather_data:
            self.update_current_temperature(weather_data['hourly']['temperature_2m'][0])
            self.adjust_mode()

    def adjust_mode(self):
        """Adjust the cooling system's mode based on the current and desired temperatures."""
        if self.current_temperature > self.desired_temperature:
            self.mode = "cooling"
        else:
            self.mode = "off"
        self.client.publish(f"{self.topic_base}/mode", self.mode)

    def update_current_temperature(self, value):
        """Updates the current temperature."""
        self.current_temperature = value
        self.client.publish(f"{self.topic_base}/current_temperature", str(self.current_temperature))
        print(f"Updated Current Temperature: {self.current_temperature}C")

if __name__ == "__main__":
    # Test the SmartCoolingSystem
    cooling_system = SmartCoolingSystem("test_cooling_system", "localhost")
    print("Fetching and updating current temperature...")
    cooling_system.fetch_and_update_current_temperature()
    print(f"Mode of the cooling system: {cooling_system.mode}")
