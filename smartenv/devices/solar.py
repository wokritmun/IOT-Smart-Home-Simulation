from ..smart_device import SmartDevice


from ..import solar_util

class SmartSolarPanel(SmartDevice):
    PANEL_EFFICIENCY = 0.20  # Hypothetical efficiency of 20%
    PANEL_AREA = 1.6  # 1.6 square meters, this is a hypothetical area for a standard solar panel

    def __init__(self, device_id, broker_ip):
        super().__init__(device_id, broker_ip)
        self.energy_production = 0.0  # kW
    
    def fetch_and_update_energy_production(self):
        solar_data = solar_util.get_solar_irradiance()
        irradiance = solar_data["estimated_actuals"][0]["ghi"]  # Global Horizontal Irradiance in W/m^2

        # Estimate energy production for the panel
        energy_produced = irradiance * self.PANEL_EFFICIENCY * self.PANEL_AREA / 1000  # kW
        self.update_energy_production(energy_produced)

        print(f"Current Solar Irradiance: {irradiance} W/m^2")
        print(f"Energy Produced: {self.energy_production} kW")

    def update_energy_production(self, value):
        """Updates the energy production and sends a message to broker."""
        self.energy_production = value
        self.client.publish(f"{self.topic_base}/energy_production", str(self.energy_production))

if __name__ == "__main__":
    solar_panel = SmartSolarPanel("test_solar", "localhost")
    solar_panel.fetch_and_update_energy_production()
