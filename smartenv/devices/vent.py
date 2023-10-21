from ..smart_device import SmartDevice
from ..import weather_util

class SmartVent(SmartDevice):
    POWER_USAGE = 10  # 10 watts when adjusting
    
    def __init__(self, device_id, broker_ip):
        super().__init__(device_id, broker_ip)
        self.angle = 0
        self.energy_consumed = 0
        self.vent_status = "closed"
        self.external_data = weather_util.get_weather_data()
        self.adjust_vent_based_on_external_data()

    def calculate_energy(self, operation_time):
        return (self.POWER_USAGE * operation_time) / 3600

    def adjust_angle(self, new_angle, operation_time=5):  # default adjustment time is 5 seconds
        self.angle = new_angle
        self.energy_consumed += self.calculate_energy(operation_time)
        self.client.publish(f"{self.topic_base}/angle", str(new_angle))
        print(f"Vent angle adjusted to: {new_angle} degrees. Energy consumed: {self.energy_consumed}Wh")

    def open_vent(self):
        self.vent_status = "open"
        self.client.publish(f"{self.topic_base}/vent_status", "open")
        print("Vent opened.")

    def close_vent(self):
        self.vent_status = "closed"
        self.client.publish(f"{self.topic_base}/vent_status", "closed")
        print("Vent closed.")

    def adjust_vent_based_on_external_data(self):
        apparent_temp = self.external_data["hourly"]["apparent_temperature"][0]
        humidity = self.external_data["hourly"]["relativehumidity_2m"][0]
        weather_code = self.external_data["hourly"]["weathercode"][0]

        if apparent_temp > 85:  # Too hot outside
            self.open_vent()
            self.adjust_angle(45)  # Slightly open
        elif humidity > 80 or (weather_code >= 200 and weather_code < 600):  # Raining or high humidity
            self.close_vent()
            self.adjust_angle(0)  # Fully closed
        else:
            self.open_vent()
            self.adjust_angle(25)  # Slightly open but not fully

    def report_energy_consumption(self):
        """Report total energy consumed by the blinds."""
        self.client.publish(f"{self.topic_base}/energy_consumption", str(self.energy_consumed))
        print(f"Energy consumed by the vent: {self.energy_consumed}Wh")

if __name__ == "__main__":
    vent = SmartVent("test_vent", "localhost")
