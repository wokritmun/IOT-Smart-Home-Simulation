from ..smart_device import SmartDevice
from ..import weather_util

class SmartBlinds(SmartDevice):
    POWER_USAGE = 50 

    def __init__(self, device_id, broker_ip):
        super().__init__(device_id, broker_ip)
        self.position = "closed"
        self.energy_consumed = 0 
        self.adjust_blinds_based_on_weather()  # Initial adjustment of blinds based on current weather

    def calculate_energy(self, operation_time):
        """Calculate energy consumed during an operation in watt-hours"""
        return (self.POWER_USAGE * operation_time) / 3600

    def open_blinds(self, operation_time=10):
        if self.position == "open":
            print(f"{self.device_id} blinds are already open.")
            return

        print(f"Opening {self.device_id} blinds...")
        self.position = "open"
        self.energy_consumed += self.calculate_energy(operation_time)
        self.client.publish(f"{self.topic_base}/position", "open")

    def close_blinds(self, operation_time=10):
        if self.position == "closed":
            print(f"{self.device_id} blinds are already closed.")
            return

        print(f"Closing {self.device_id} blinds...")
        self.position = "closed"
        self.energy_consumed += self.calculate_energy(operation_time)
        self.client.publish(f"{self.topic_base}/position", "closed")

    def report_energy_consumption(self):
        """Report total energy consumed by the blinds."""
        self.client.publish(f"{self.topic_base}/energy_consumption", str(self.energy_consumed))

    def adjust_blinds_based_on_weather(self):
        """Adjust the blinds' position based on current weather data."""
        weather_data = weather_util.get_weather_data()

        # Example conditions to determine when to open/close blinds
        temp = weather_data['hourly']['temperature_2m'][0]
        cloud_cover = weather_data['hourly']['cloudcover'][0]

        if temp > 85 or cloud_cover < 50:  # arbitrary values
            self.close_blinds()
        else:
            self.open_blinds()

if __name__ == "__main__":
    blinds = SmartBlinds("test_blinds", "localhost")
    blinds.report_energy_consumption()
