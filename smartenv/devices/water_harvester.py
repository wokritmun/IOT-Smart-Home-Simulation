import time
from ..smart_device import SmartDevice
from ..weather_util import get_weather_data

class SmartWaterHarvester(SmartDevice):
    def __init__(self, device_id, broker_ip):
        super().__init__(device_id, broker_ip)
        self.water_collected = 0.0  # liters

    def calculate_water_collection(self, humidity, temperature):
        """Calculate water collected based on humidity and temperature.
        This is a hypothetical formula. Real-life data may differ."""
        return (humidity / 100) * (temperature / 10)  # liters per hour

    def update_water_collection(self):
        """Updates water collected from the air."""
        weather_data = get_weather_data()
        hourly_data = weather_data['hourly']
        humidity = hourly_data['relativehumidity_2m'][0]
        temperature = hourly_data['temperature_2m'][0]
        
        # Calculate and update
        collected = self.calculate_water_collection(humidity, temperature)
        self.water_collected += collected
        self.client.publish(f"{self.topic_base}/water_collected", str(self.water_collected))

        print(f"Water collected: {collected}L. Total water: {self.water_collected}L")

    def run(self):
        """Continuously update water collection every hour."""
        while True:
            self.update_water_collection()
            time.sleep(3600)  # Wait for 1 hour

if __name__ == "__main__":
    harvester = SmartWaterHarvester("test_harvester", "localhost")
    harvester.run()
