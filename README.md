# 🏭 OPC UA Workstation Simulation

This project simulates an industrial workstation system using OPC UA (Open Platform Communications Unified Architecture).
It is designed for testing and developing OPC UA-based automation systems with virtual devices, live measurements, and resettable methods.

## 📁 Details

### 🔧 `server.py`
Main entry point. Sets up the OPC UA server:
- Initializes namespace and endpoint
- Creates one workstation (`W1`) with 5 devices:
  - Drill
  - Turn Table
  - Checker
  - Ejector A
  - Ejector B
- Registers resettable OPC UA methods for each device.
- Updates all device measurements every 5 seconds with simulated data.

### 🛠️ `WorkStationSimulator.py`
Simulates real-time behavior of the devices:
- Generates random boolean, int, and datetime values.
- Maintains a `heartbeat` counter.
- Returns a list of updated values to mimic sensor input.

### Device.py
Defines a Device class that contains a list of Measurement objects.

### Measurement.py
Defines the Measurement class with ID, tag, type, and value attributes.
