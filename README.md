## Vehicle Fleet Monitoring System

### Introduction
This project is a simple fleet monitoring system that analyzes speed, temperature, and fuel data for multiple vehicles. It demonstrates object-oriented programming (OOP), file handling with CSV, and robust exception management. The program computes fleet-wide averages and generates per-vehicle alerts for overheating and low fuel conditions.

### System Requirements
- **Python**: 3.9+ (tested on 3.13)
- **Editor**: VS Code (recommended)
- **Testing**: Python's built-in `unittest`

### Project Structure
```text
vehicle.py         # Vehicle dataclass with validation
fleet_manager.py   # FleetManager for averages and alerts (configurable thresholds)
main.py            # Entry point: reads CSV, prints summary and alerts
vehicles.csv       # Sample input data
tests/test_fleet.py# Unit and integration tests (unittest)
README.md          # This file
```

### Classes, Constants, and Key Functions
- **Vehicle** (`vehicle.py`)
  - **Attributes**: `id: str`, `speed: float`, `temperature: float`, `fuel: float`
  - **Validation** (in `__post_init__`):
    - `fuel` must be in [0, 100]
    - `speed` must be in [0, 300] km/h
    - `temperature` must be in [-50, 200] °C

- **FleetManager** (`fleet_manager.py`)
  - **Constants**:
    - `MAX_TEMP = 110.0`
    - `MIN_FUEL = 15.0`
    - `INCLUDE_EDGE_TEMPERATURE = False` (False → only temperature > MAX_TEMP triggers)
    - `INCLUDE_EDGE_FUEL = False` (False → only fuel < MIN_FUEL triggers)
  - **Constructor**: raises `ValueError` if initialized with an empty list of vehicles
  - **Methods**:
    - `average_speed() -> float`
    - `average_temperature() -> float`
    - `average_fuel() -> float`
    - `generate_alerts() -> list[str]` — returns messages like "V1: Critical Overheating" and "V1: Low Fuel Warning"
    - `summary() -> str` — formatted averages string

- **CSV Handling** (`main.py`)
  - `read_vehicles_from_csv(path)` uses `csv.DictReader` with header validation
  - Skips malformed rows with a warning message and continues processing
  - Raises a clear error if the file is missing, has no headers, or has no valid data rows

### Usage
- **Run with the sample CSV** (from the project root):
```bash
python main.py
```
- **Run with a custom CSV path**:
```bash
python main.py path\to\your\vehicles.csv
```

### Configuring Thresholds
Edit the constants in `fleet_manager.py` to change thresholds or whether edge values trigger:
```python
MAX_TEMP: float = 110.0
MIN_FUEL: float = 15.0
INCLUDE_EDGE_TEMPERATURE: bool = False  # False => triggers only when temperature > MAX_TEMP
INCLUDE_EDGE_FUEL: bool = False         # False => triggers only when fuel < MIN_FUEL
```

### Sample Input (CSV) and Expected Output
- **Sample CSV** (`vehicles.csv`):
```csv
id,speed,temperature,fuel
V1,120,130,10
V2,80,90,40
V3,0,85,50
V4,60,110,15
```

- **Expected Output** (with edges excluded as configured above):
```text
Average Speed: 65.00 km/h
Average Temperature: 103.75 °C
Average Fuel: 28.75 %

Alerts:
- V1: Critical Overheating
- V1: Low Fuel Warning
```

### Testing
Run the unit and integration tests with `unittest`:
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```
Tests cover:
- **Unit**: alert triggering above/below thresholds and non-trigger at edge values
- **Integration**: average speed calculation across a small fleet
- **Error Handling**: initializing `FleetManager` with an empty vehicle list raises `ValueError`

### Error Handling Notes
- The program will print warnings and skip malformed CSV rows (e.g., non-numeric values)
- It will stop with an informative message if:
  - The CSV file is missing or unreadable
  - The CSV has no headers or is empty
  - All rows are invalid after validation


