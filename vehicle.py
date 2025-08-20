from dataclasses import dataclass


@dataclass(frozen=True)
class Vehicle:
    """Represents a vehicle with basic telemetry.

    Attributes:
        id: Unique vehicle identifier.
        speed: Current speed in km/h.
        temperature: Engine temperature in °C.
        fuel: Remaining fuel as a percentage (0-100).
    """

    id: str
    speed: float
    temperature: float
    fuel: float

    def __post_init__(self) -> None:
        # Basic validation to ensure values are within reasonable bounds
        if not self.id:
            raise ValueError("Vehicle id must be a non-empty string.")
        if self.fuel < 0 or self.fuel > 100:
            raise ValueError("Fuel percentage must be between 0 and 100.")
        # Plausibility checks for speed and temperature
        if self.speed < 0 or self.speed > 300:
            raise ValueError("Speed must be between 0 and 300 km/h.")
        if self.temperature < -50 or self.temperature > 200:
            raise ValueError("Temperature must be between -50 and 200 °C.")


