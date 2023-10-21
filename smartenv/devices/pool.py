from ..smart_device import SmartDevice
from .. import weather_util

class SmartPoolController(SmartDevice):
    POWER_USAGE_FILTER = 750
    POWER_USAGE_HEAT = 5000

    def __init__(self, device_id, broker_ip):
        super().__init__(device_id, broker_ip)
        self.temperature = 75
        self.filter_status = "off"
        self.heat_status = "off"
        self.energy_consumed = 0
        self.weather_data = self.fetch_weather_data()

    def fetch_weather_data(self):
        return weather_util.get_weather_data()

    def update_state_based_on_weather(self):
        external_temp = self.weather_data["hourly"]["temperature_2m"][0]
        humidity = self.weather_data["hourly"]["relativehumidity_2m"][0]
        rain_prob = self.weather_data["hourly"]["precipitation_probability"][0]
        
        print(f"External Temperature: {external_temp}")
        print(f"Relative Humidity: {humidity}")
        print(f"Chance of Rain: {rain_prob}%")

        if external_temp + 10 < self.temperature:
            self.start_heating()
        else:
            self.stop_heating()

        if humidity < 40 and external_temp > 85:
            print("Increased evaporation expected. You might want to check the pool water level.")
            self.start_filter(run_time=5400)  # increased run time to 1.5 hours
        
        if rain_prob > 50:
            print("High chance of rain. Adjusting pool systems...")
            self.stop_heating()
            self.start_filter(run_time=7200)  # run filter longer after rain


    def calculate_energy(self, run_time, mode="filter"):
        power_usage = self.POWER_USAGE_FILTER if mode == "filter" else self.POWER_USAGE_HEAT
        return (power_usage * run_time) / 3600
    
    def start_filter(self, run_time=3600):  # default run time is 1 hour
        self.filter_status = "on"
        self.energy_consumed += self.calculate_energy(run_time, mode="filter")
        self.client.publish(f"{self.topic_base}/filter_status", "on")
    
    def start_heating(self, run_time=3600):
        self.heat_status = "on"
        self.energy_consumed += self.calculate_energy(run_time, mode="heat")
        self.client.publish(f"{self.topic_base}/heat_status", "on")

    def stop_filter(self):
        self.filter_status = "off"
        self.client.publish(f"{self.topic_base}/filter_status", "off")

    def stop_heating(self):
        self.heat_status = "off"
        self.client.publish(f"{self.topic_base}/heat_status", "off")
    
    def set_temperature(self, temp):
        self.temperature = temp
        self.client.publish(f"{self.topic_base}/temperature", temp)

    def report_energy_consumption(self):
        """Report total energy consumed by the blinds."""
        self.client.publish(f"{self.topic_base}/energy_consumption", str(self.energy_consumed))

    def report(self):
        self.report_energy_consumption()
        print(f"Pool Temperature: {self.temperature}F")
        print(f"Heating Status: {self.heat_status}")
        print(f"Filter Status: {self.filter_status}")
        print(f"Total Energy Consumed: {self.energy_consumed} kWh")

if __name__ == "__main__":
    pool_controller = SmartPoolController("test_pool", "localhost")
    pool_controller.update_state_based_on_weather()
    pool_controller.report()