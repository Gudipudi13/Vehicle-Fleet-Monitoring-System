from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from vehicle import Vehicle


# Threshold constants (as requested names)
# Adjust these to configure alert edge behavior.
MAX_TEMP: float = 110.0
MIN_FUEL: float = 15.0
INCLUDE_EDGE_TEMPERATURE: bool = False  # False => temperature > threshold triggers
INCLUDE_EDGE_FUEL: bool = False         # False => fuel < threshold triggers

#INCLUDE_EDGE_TEMPERATURE: bool = True  # True => temperature >= threshold triggers
#INCLUDE_EDGE_FUEL: bool = True         # True => fuel <= threshold triggers


@dataclass
class FleetManager:
    vehicles: List[Vehicle]

    def __post_init__(self) -> None:
        if not self.vehicles:
            raise ValueError("FleetManager requires at least one vehicle.")

    @classmethod
    def from_iterable(cls, vehicles: Iterable[Vehicle]) -> "FleetManager":
        return cls(list(vehicles))

    def average_speed(self) -> float:
        if not self.vehicles:
            return 0.0
        total = sum(v.speed for v in self.vehicles)
        return total / len(self.vehicles)

    def average_temperature(self) -> float:
        if not self.vehicles:
            return 0.0
        total = sum(v.temperature for v in self.vehicles)
        return total / len(self.vehicles)

    def average_fuel(self) -> float:
        if not self.vehicles:
            return 0.0
        total = sum(v.fuel for v in self.vehicles)
        return total / len(self.vehicles)

    def generate_alerts(self) -> List[str]:
        alerts: List[str] = []
        for v in self.vehicles:
            overheat = (
                v.temperature >= MAX_TEMP
                if INCLUDE_EDGE_TEMPERATURE
                else v.temperature > MAX_TEMP
            )
            if overheat:
                alerts.append(f"{v.id}: Critical Overheating")
            low_fuel = (
                v.fuel <= MIN_FUEL
                if INCLUDE_EDGE_FUEL
                else v.fuel < MIN_FUEL
            )
            if low_fuel:
                alerts.append(f"{v.id}: Low Fuel Warning")
        return alerts

    def summary(self) -> str:
        return (
            f"Average Speed: {self.average_speed():.2f} km/h\n"
            f"Average Temperature: {self.average_temperature():.2f} °C\n"
            f"Average Fuel: {self.average_fuel():.2f} %"
        )


