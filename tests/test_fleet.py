import unittest

from fleet_manager import FleetManager, MAX_TEMP, MIN_FUEL
from vehicle import Vehicle


class TestVehicleAlerts(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_overheating_triggers_above_threshold(self):
        v = Vehicle(id="V1", speed=50, temperature=MAX_TEMP + 10, fuel=50)
        fm = FleetManager([v])
        alerts = fm.generate_alerts()
        self.assertIn("V1: Critical Overheating", alerts)

    def test_low_fuel_triggers_below_threshold(self):
        v = Vehicle(id="V2", speed=50, temperature=80, fuel=MIN_FUEL - 5)
        fm = FleetManager([v])
        alerts = fm.generate_alerts()
        self.assertIn("V2: Low Fuel Warning", alerts)

    def test_temperature_at_threshold_does_not_trigger(self):
        v = Vehicle(id="V3", speed=50, temperature=MAX_TEMP, fuel=50)
        fm = FleetManager([v])
        alerts = fm.generate_alerts()
        self.assertNotIn("V3: Critical Overheating", alerts)

    def test_fuel_at_threshold_does_not_trigger(self):
        v = Vehicle(id="V4", speed=50, temperature=80, fuel=MIN_FUEL)
        fm = FleetManager([v])
        alerts = fm.generate_alerts()
        self.assertNotIn("V4: Low Fuel Warning", alerts)


class TestFleetAveragesAndErrors(unittest.TestCase):
    def test_average_speed(self):
        v1 = Vehicle(id="A", speed=80, temperature=80, fuel=50)
        v2 = Vehicle(id="B", speed=90, temperature=80, fuel=50)
        v3 = Vehicle(id="C", speed=100, temperature=80, fuel=50)
        fm = FleetManager([v1, v2, v3])
        self.assertAlmostEqual(fm.average_speed(), 90.0, places=2)

    def test_empty_fleet_raises(self):
        with self.assertRaises(ValueError):
            FleetManager([])


if __name__ == "__main__":
    unittest.main()


