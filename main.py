from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import List

from vehicle import Vehicle
from fleet_manager import FleetManager


class CsvError(Exception):
    pass


def read_vehicles_from_csv(csv_path: Path) -> List[Vehicle]:
    if not csv_path.exists() or not csv_path.is_file():
        raise CsvError(f"CSV file not found: {csv_path}")

    vehicles: List[Vehicle] = []
    try:
        with csv_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                raise CsvError("CSV has no headers.")
            expected = {"id", "speed", "temperature", "fuel"}
            missing = expected - set(name.strip().lower() for name in reader.fieldnames)
            if missing:
                raise CsvError(f"CSV missing required headers: {', '.join(sorted(missing))}")

            for row in reader:
                if not any(row.values()):
                    # Skip completely empty lines
                    continue
                try:
                    vehicle = Vehicle(
                        id=str(row["id"]).strip(),
                        speed=float(row["speed"]),
                        temperature=float(row["temperature"]),
                        fuel=float(row["fuel"]),
                    )
                    vehicles.append(vehicle)
                except (ValueError, TypeError, KeyError) as exc:
                    # Skip bad rows but continue processing others
                    print(f"Warning: Skipping invalid row: {row}. Reason: {exc}")
                    continue
    except csv.Error as exc:
        raise CsvError(f"CSV parsing error: {exc}") from exc

    if not vehicles:
        raise CsvError("CSV contains no valid data rows.")

    return vehicles


def main() -> int:
    # Determine CSV path: provided as first arg or default to 'vehicles.csv' in the same folder
    default_path = Path(__file__).with_name("vehicles.csv")
    csv_arg = Path(sys.argv[1]) if len(sys.argv) > 1 else default_path

    try:
        vehicles = read_vehicles_from_csv(csv_arg)
    except CsvError as exc:
        print(f"Error: {exc}")
        return 1

    manager = FleetManager.from_iterable(vehicles)
    print(manager.summary())

    alerts = manager.generate_alerts()
    if alerts:
        print("\nAlerts:")
        for alert in alerts:
            print(f"-> {alert}")
    else:
        print("\nNo alerts.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


