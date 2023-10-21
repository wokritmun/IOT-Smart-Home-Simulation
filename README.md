# Smart IoT Ecosystem for Sahara Rehabilitation

This project is an ambitious endeavor aimed at making regions like the Sahara Desert habitable through the seamless integration of smart devices. Leveraging the power of IoT (Internet of Things), we aim to regulate, automate, and optimize resource usage, allowing for sustainable living in challenging environments.

## Table of Contents

- [About the Project](#about-the-project)
- [Features and Devices](#features-and-devices)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [APIs Used](#apis-used)
- [Contribute](#contribute)
- [Credits](#credits)
- [License](#license)

## About the Project

**IoT Smart Home Simulation for Sahara Desert Habitation**:
- Engineered an advanced IoT Smart Home Simulation, seamlessly integrating over 20 smart devices.
- Utilized technologies such as Python and MQTT for effective device communication.
- Aims to reduce energy consumption by at least 25 percent, thereby ensuring sustainability in resource-scarce areas.
- Provides pivotal insights from simulation data, equipping decision-makers with actionable knowledge to enhance and optimize smart home systems in challenging environments.

## Features and Devices

Our integrated suite of smart devices is as follows:

- **SmartLight**: IoT enabled light with adaptive brightness and energy monitoring.
- **SmartDoorbell**: Interactive doorbell with camera and alerting system.
- **SmartBlinds**: Automated blinds adjusted based on sunlight and user preferences.
- **SmartGarageDoor**: Intelligent garage door with security and auto-lock features.
- **SmartHumidifier**: Maintains optimal humidity levels for comfort and health.
- **SmartLock**: Secure and remote-controlled door locks.
- **SmartPlug**: Manages connected devices, prioritizes power delivery, and monitors consumption.
- **SmartPoolController**: Regulates pool temperature, cleanliness, and safety.
- **SmartRefrigerator**: Energy-efficient refrigerator with inventory management.
- **SmartThermostat**: Regulates home temperature for optimal comfort.
- **SmartVent**: Automated ventilation system for optimal air quality.
- **SmartWasher**: Efficient washing machine with water and energy conservation.
- **SmartBattery**: Stores energy, manages charging, discharging, and battery health.
- **SmartCookingFire**: Monitors and controls cooking temperatures.
- **SmartCoolingSystem**: Centralized system for home cooling.
- **SmartCamera**: Home surveillance and image processing tasks using OpenCV.
- **SmartWaterTank**: Monitors and manages home water supply.
- **SmartWaterHarvester**: Extracts water from the atmosphere.
- **SmartWeatherAlert**: Provides weather alerts and suggestions.
- **SmartSatelliteComm**: (Future Implementation) Connects with satellites for advanced communications.
- **SmartSolarPanel**: Uses solar data to report energy production.

## Prerequisites

- Python 3.x
- [paho-mqtt](https://pypi.org/project/paho-mqtt/)
- [OpenCV](https://opencv.org/) (For SmartCamera)
- Internet connection

## Installation

1. Clone the repository:
```bash
git clone https://github.com/wokritmun/smart-iot-ecosystem.git
```

2. Navigate to the project directory and install required packages:

```
cd smart-iot-ecosystem
pip install -r requirements.txt
```


## Usage

1. Start the MQTT broker.
2. Run the desired modules. For example, to run the solar panel:

```
python smart_device/solar.py
``````


3. Monitor energy production, consumption, and other metrics via MQTT messages.

## APIs Used

- **Solcast**: Provides real-time solar irradiance data for `SmartSolarPanel`.

## Contribute

I welcome contributions. To contribute:

1. Fork the repository.
2. Create a new branch.
3. Make changes and commit them.
4. Push the branch to your fork.
5. Create a pull request.

## Credits

This project was developed by Wokrit Movel, inspired by a vision of a greener world and making the uninhabitable, habitable.

## License

MIT License.
