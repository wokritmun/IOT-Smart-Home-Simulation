from ..smart_device import SmartDevice
from ..import weather_util

class SmartHumidifier(SmartDevice):
    POWER_USAGE = 30  # 30 watts when operating
    LOW_HUMIDITY_THRESHOLD = 30  # Turn on humidifier if below this threshold
    HIGH_HUMIDITY_THRESHOLD = 70  # Turn off humidifier if above this threshold

    def __init__(self, device_id, broker_ip):
        super().__init__(device_id, broker_ip)
        self.status = "off"
        self.energy_consumed = 0
        self.humidity = 50  # default to 50% humidity
        self.adjust_humidity()

    def calculate_energy(self, run_time):
        return (self.POWER_USAGE * run_time) / 3600

    def start(self, run_time=3600):  # default run time is 1 hour
        self.status = "on"
        self.energy_consumed += self.calculate_energy(run_time)
        self.client.publish(f"{self.topic_base}/status", "on")
        print("Humidifier started.")

    def stop(self):
        self.status = "off"
        self.client.publish(f"{self.topic_base}/status", "off")
        print("Humidifier stopped.")

    def set_humidity(self, level):
        self.humidity = level
        self.client.publish(f"{self.topic_base}/humidity", level)

    def report_energy_consumption(self):
        """Report total energy consumed by the blinds."""
        self.client.publish(f"{self.topic_base}/energy_consumption", str(self.energy_consumed))
        print(f"Energy consumed: {self.energy_consumed}kWh")

    def adjust_humidity(self):
        """Adjust the humidifier's status based on the external humidity."""
        weather_data = weather_util.get_weather_data()
        external_humidity = weather_data['hourly']['relativehumidity_2m'][0]

        if external_humidity < self.LOW_HUMIDITY_THRESHOLD:
            self.start()
        elif external_humidity > self.HIGH_HUMIDITY_THRESHOLD:
            self.stop()

        self.set_humidity(external_humidity)
        print(f"External humidity: {external_humidity}%")

if __name__ == "__main__":
    # Test the SmartHumidifier class
    humidifier = SmartHumidifier("test_humidifier", "localhost")
    humidifier.report_energy_consumption()
