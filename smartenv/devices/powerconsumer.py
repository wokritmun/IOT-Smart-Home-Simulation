from abc import ABC, abstractmethod
from ..smart_device import SmartDevice

class PowerConsumingDevice(ABC):
    """
    Abstract class that every power-consuming device should inherit from.
    It enforces certain methods that the SmartPlug can call.
    """
    @abstractmethod
    def get_power_consumption(self):
        """Returns the current power consumption of the device in watts."""
        pass

    @abstractmethod
    def set_max_power(self, watts):
        """Sets a limit on the maximum power this device can consume."""
        pass

class PriorityDevice(PowerConsumingDevice, ABC):
    def __init__(self, priority=0):
        super().__init__()
        self.priority = priority  # higher values mean higher priority

    @abstractmethod
    def get_power_consumption(self):
        pass

    @abstractmethod
    def set_max_power(self, watts):
        pass

    def __lt__(self, other):
        return self.priority < other.priority