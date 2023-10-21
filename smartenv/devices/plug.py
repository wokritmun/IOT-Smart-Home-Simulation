from ..smart_device import SmartDevice
from .powerconsumer import PowerConsumingDevice
from .powerconsumer import PriorityDevice
from .battery import SmartBattery
import time
import heapq

from abc import ABC, abstractmethod
from ..smart_device import SmartDevice



class SmartPlug(SmartDevice):
    def __init__(self, device_id, broker_ip, battery: SmartBattery):
        super().__init__(device_id, broker_ip)
        self.battery = battery
        self.devices = []  # List of connected devices
        self.last_active_time = None  # To track when the device was last active
        self.idle_threshold = 3600  # Time in seconds after which the plug is considered idle (default is 1 hour)

    def turn_on(self):
        super().turn_on()
        self.last_active_time = time.time()  # Update the last active time whenever the device is turned on

    def connect_device(self, device: PriorityDevice):
        heapq.heappush(self.devices, device)  # Maintaining a priority queue


    def total_power_consumption(self):
        """Calculate the total power consumption of all devices connected to this plug."""
        return sum(device.get_power_consumption() for device in self.devices)
    
    def check_idle(self):
        """Check if the device has been idle for more than the threshold."""
        if self.status == "ON" and time.time() - self.last_active_time > self.idle_threshold:
            self.turn_off()
            self.client.publish(f"{self.topic_base}/notification", "Turned off due to inactivity.")

    def calculate_power_consumption(self):
        """Calculate power consumption based on hypothetical values.
        For example, you can assume the device consumes more when ON and less when OFF.
        """
        if self.status == "ON":
            return 10  # Hypothetical value in watts for an active device
        else:
            return 0.5  # Hypothetical value in watts for a device in standby

    def report_power_consumption(self):
        """Publish power consumption data to MQTT."""
        power_data = self.calculate_power_consumption()
        self.client.publish(f"{self.topic_base}/power_consumption", power_data)

    def request_power(self, required_energy):
        energy_from_battery = self.battery.discharge(required_energy)
        energy_from_grid = max(0, required_energy - energy_from_battery)  # Ensure non-negative energy from grid
        print(f"Drew {energy_from_battery} kWh from battery and {energy_from_grid} kWh from grid.")


    def on_message(self, client, userdata, message):
        super().on_message(client, userdata, message)  # Handle base class on_message
        # Add more message handlers if needed for the SmartPlug

    def regulate_power(self, max_power_for_all_devices):
        """
        Sophisticated power regulation.
        Devices with higher priority get power first.
        """
        remaining_power = max_power_for_all_devices
        devices_to_reduce = []
        
        # First pass: Distribute power according to priority until we run out.
        for device in sorted(self.devices, reverse=True):  # highest priority first
            power_needed = device.get_power_consumption()
            
            if remaining_power >= power_needed:
                remaining_power -= power_needed
            else:
                devices_to_reduce.append(device)
                
        # Second pass: Distribute the remaining power among the devices that were not fully powered.
        if devices_to_reduce:
            power_per_device = remaining_power / len(devices_to_reduce)
            
            for device in devices_to_reduce:
                device.set_max_power(power_per_device)
                if power_per_device < device.get_power_consumption():
                    self.client.publish(f"{self.topic_base}/notification", 
                                        f"Reduced power for {device.device_id} to {power_per_device} watts.")
