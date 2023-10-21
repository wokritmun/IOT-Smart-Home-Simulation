import paho.mqtt.client as mqtt
import time
from threading import Timer

class SmartDevice:
    def __init__(self, device_id, broker_ip):
        self.device_id = device_id
        self.status = "OFF"
        self.power_consumption = 0.0
        self.client = mqtt.Client()
        self.broker_ip = broker_ip
        self.topic_base = f"home/device/{device_id}"
        self.connect_to_broker()
    
    def on_message(self, client, userdata, message):
        payload = message.payload.decode()
        if message.topic == f"{self.topic_base}/status":
            if payload == "ON":
                self.turn_on()
            elif payload == "OFF":
                self.turn_off()

    def connect_to_broker(self):
        self.client.connect(self.broker_ip)
        self.client.subscribe(f"{self.topic_base}/#")
        print(f"Connected to broker and subscribed to {self.topic_base}/#")  # Diagnostic print
        self.client.on_message = self.on_message
        self.client.loop_start()

    def calculate_power_consumption(self):
        """Calculate power consumption. To be overridden by child devices."""
        return 0  # default is 0 for devices that don't have power consumption calculation

    def report_energy_consumption(self):
        """Report energy consumed over a specific interval."""
        interval_hours = 0.1  # hypothetical interval of 0.1 hours = 6 minutes
        energy_consumed = self.calculate_power_consumption() * interval_hours  # in watt-hours
        self.client.publish(f"{self.topic_base}/energy_consumption", str(energy_consumed))
    def disconnect_from_broker(self):
        self.client.loop_stop()
        self.client.disconnect()

    def turn_on(self):
        self.status = "ON"
        self.client.publish(f"{self.topic_base}/status", "ON")

    def turn_off(self):
        self.status = "OFF"
        self.client.publish(f"{self.topic_base}/status", "OFF")

    def start_periodic_reporting(self, interval=360):  # default interval of 6 minutes in seconds
        """Starts periodic reporting of energy consumption."""
        self.report_energy_consumption()  # report immediately
        Timer(interval, self.start_periodic_reporting).start()  # schedule the next report





