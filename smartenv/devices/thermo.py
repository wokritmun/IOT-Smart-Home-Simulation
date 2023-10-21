

from ..smart_device import SmartDevice
from .. import weather_util
  # Assuming the weather_util is in a utils directory at the root level

class SmartThermostat(SmartDevice):
    def __init__(self, device_id, broker_ip):
        super().__init__(device_id, broker_ip)
        self.current_temperature = 72  # Default current temperature in Fahrenheit
        self.desired_temperature = 72  # Default desired temperature
        self.mode = "off"  # Can be "heating", "cooling", or "off"
        self.external_temperature = self.get_external_temperature()
        self.apparent_temperature = self.get_apparent_temperature()
        print(f"Thermostat Initialized. Current temp: {self.current_temperature}F, Desired temp: {self.desired_temperature}F, Mode: {self.mode}")

    def set_temperature(self, temp):
        """Set the desired temperature."""
        self.desired_temperature = temp
        self.adjust_mode()
        self.client.publish(f"{self.topic_base}/desired_temperature", temp)
        print(f"Desired temperature set to {temp}F")

    def update_current_temperature(self, temp=None):
        """Update the current temperature. If temp is not provided, get it from the external source."""
        if not temp:
            temp = self.get_external_temperature()
        self.current_temperature = temp
        self.adjust_mode()
        print(f"Current temperature updated to {self.current_temperature}F")

    def adjust_mode(self):
        """Adjust the mode based on the current and desired temperatures."""
        previous_mode = self.mode
        difference = self.apparent_temperature - self.current_temperature
        if difference > 2:
            self.mode = "heating"
        elif difference < -2:
            self.mode = "cooling"
        else:
            self.mode = "off"

        if previous_mode != self.mode:
            print(f"Thermostat mode changed from {previous_mode} to {self.mode}")
        self.client.publish(f"{self.topic_base}/mode", self.mode)

    def calculate_power_consumption(self):
        """Calculate power based on the mode."""
        if self.mode == "heating":
            power = 1500
        elif self.mode == "cooling":
            power = 1200
        else:
            power = 0
        print(f"Power consumption: {power}W")
        return power

    def get_external_temperature(self):
        """Fetch the current external temperature from the weather_util."""
        temp = weather_util.get_weather_data()['hourly']['temperature_2m'][0]
        print(f"Fetched external temperature: {temp}F")
        return temp

    def get_apparent_temperature(self):
        """Fetch the current apparent temperature, which factors in humidity."""
        temp = weather_util.get_weather_data()['hourly']['apparent_temperature'][0]
        print(f"Fetched apparent temperature: {temp}F")
        return temp
    
    # Add this at the end of your thermo.py
if __name__ == "__main__":
    # Assuming you have a MQTT broker running at "localhost"
    thermostat = SmartThermostat("test_thermostat", "localhost")
    thermostat.set_temperature(75)
    thermostat.update_current_temperature()
    thermostat.calculate_power_consumption()
