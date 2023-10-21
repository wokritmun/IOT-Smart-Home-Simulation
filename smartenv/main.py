from .smart_device import SmartDevice
from .devices.light import SmartLight
from .devices.bell import SmartDoorbell
from .devices.blinds import SmartBlinds
from .devices.garage import SmartGarageDoor
from .devices.humid import SmartHumidifier
from .devices.lock import SmartLock
from .devices.plug import SmartPlug
from .devices.plug import PowerConsumingDevice
from .devices.plug import PriorityDevice
from .devices.pool import SmartPoolController
from .devices.refrigerator import SmartRefrigerator
from .devices.thermo import SmartThermostat
from .devices.vent import SmartVent
from .devices.washer import SmartWasher
from .devices.battery import SmartBattery
from .devices.cookingfire import SmartCookingFire
from .devices.cooling import SmartCoolingSystem
from .devices.camera import SmartCamera
from .devices.water_tank import SmartWaterTank
from .devices.water_harvester import SmartWaterHarvester
from .devices.weatheralert import SmartWeatherAlert
from .devices.satellite import SmartSatelliteComm
from .devices.solar import SmartSolarPanel

class MockFridge(PriorityDevice):
    def __init__(self, priority):
        super().__init__(priority)
        self.max_power = 75  # Just a hypothetical value

    def get_power_consumption(self):
        return self.max_power

    def set_max_power(self, power):
        self.max_power = power

    def turn_on(self):
        super().turn_on()

class MockLamp(PriorityDevice):
    def __init__(self, priority):
        super().__init__(priority)
        self.max_power = 15  # Just a hypothetical value

    def get_power_consumption(self):
        return self.max_power

    def set_max_power(self, power):
        self.max_power = power

    def turn_on(self):
        super().turn_on()

class MockFan(PriorityDevice):
    def __init__(self, priority):
        super().__init__(priority)
        self.max_power = 50  # Just a hypothetical value

    def get_power_consumption(self):
        return self.max_power

    def set_max_power(self, power):
        self.max_power = power

    def turn_on(self):
        super().turn_on()



if __name__ == "__main__":
    # Instantiate the devices
    solar_panel = SmartSolarPanel("solar_panel_001", "localhost")
    battery = SmartBattery("battery_001", "localhost", solar_panel)
    plug = SmartPlug("plug_001", "localhost", battery)

    # Fetch and update energy production for solar panel
    solar_panel.fetch_and_update_energy_production()

    # Connect devices to the smart plug
    fridge = MockFridge(priority=3)
    lamp = MockLamp(priority=1)
    fan = MockFan(priority=2)    # Middle priority

    plug.connect_device(fridge)
    plug.connect_device(lamp)
    plug.connect_device(fan)

    # Turn on the smart plug and the devices
    plug.turn_on()
    fridge.turn_on()
    lamp.turn_on()
    fan.turn_on()

    # Simulate a scenario where the plug needs to regulate power
    max_power_for_all_devices = 100  # Hypothetical max power in watts for all devices
    plug.regulate_power(max_power_for_all_devices)

    # Simulate some power consumption and request power from battery
    total_power_consumed = sum([device.get_power_consumption() for device in [fridge, lamp, fan]])
    for _ in range(5):  # This loop simulates the plug consuming power in 5 iterations
        required_energy = total_power_consumed / 1000  # Convert watts to kWh
        plug.request_power(required_energy)

    # Print the remaining energy in the battery after consumption
    print(f"Remaining energy in battery: {battery.stored_energy:.2f} kWh")

    # Print the current power consumption of each device after regulation
    print(f"Fridge power consumption: {fridge.get_power_consumption()} watts")
    print(f"Lamp power consumption: {lamp.get_power_consumption()} watts")
    print(f"Fan power consumption: {fan.get_power_consumption()} watts")
