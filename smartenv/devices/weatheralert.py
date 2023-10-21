from ..smart_device import SmartDevice
from ..weather_util import get_weather_data

class SmartWeatherAlert(SmartDevice):
    def __init__(self, device_id, broker_ip):
        super().__init__(device_id, broker_ip)
        self.alert_status = "No Alerts"
        self.check_weather_alerts()

    def check_weather_alerts(self):
        """Check weather data and set alerts if necessary."""
        data = get_weather_data()

        # Checking rain for the next 3 hours
        next_three_hours_rain_prob = data['hourly']['precipitation_probability'][:3]
        if all(prob > 70 for prob in next_three_hours_rain_prob):
            self.update_alert("High chance of consistent rain over the next few hours!")

        # Check for severe weather conditions based on 'weathercode' 
        # For the purpose of this example, let's assume a code '5' represents a severe weather condition
        next_three_hours_weather_code = data['hourly']['weathercode'][:3]
        if all(code == 5 for code in next_three_hours_weather_code):
            self.update_alert("Warning: Severe weather expected in the upcoming hours!")

        # Low visibility alert for the next 3 hours
        next_three_hours_visibility = data['hourly']['visibility'][:3]
        if all(visibility < 2 for visibility in next_three_hours_visibility):
            self.update_alert("Consistent low visibility expected! Potential for prolonged sandstorm conditions.")

        # Additional conditions can be added. For instance, if the temperature drops drastically, 
        # it could be an indication of an incoming cold front.
        temperature_diff = abs(data['hourly']['temperature_2m'][0] - data['hourly']['temperature_2m'][1])
        if temperature_diff > 10:
            self.update_alert("Significant temperature drop detected. Prepare for cold conditions!")

    def update_alert(self, alert_message):
        """Updates the alert message."""
        if self.alert_status != alert_message:  # Avoid repetitive alerts
            self.alert_status = alert_message
            print(f"Alert Status Updated: {self.alert_status}")
            self.client.publish(f"{self.topic_base}/alert_status", self.alert_status)
        else:
            print(f"Alert Status Remains: {self.alert_status}")

if __name__ == "__main__":
    device = SmartWeatherAlert("test_weather_alert", "localhost")
