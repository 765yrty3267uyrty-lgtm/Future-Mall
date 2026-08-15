#!/usr/bin/env python3
"""
Pure-Python mirror of the Smart Garage Gate MicroPython firmware logic
(deliverables/sources/task5/esp32_wokwi/src/main.py).

Used to verify the truth-table behaviour without ESP32 hardware.
"""

MAX_CARS = 15


class GarageGate:
    """Mirrors main.py: count cars, entry/exit flashes, free/full LEDs."""

    def __init__(self):
        self.count = 0
        self.green = True
        self.red = False

    def _update_status(self):
        self.green = self.count < MAX_CARS
        self.red = self.count == MAX_CARS

    def car_enters(self):
        """Return (event, accepted). Mirrors firmware car_enters()."""
        if self.count < MAX_CARS:
            self.count += 1
            self._update_status()
            return "CAR IN", True
        return "GARAGE FULL", False

    def car_exits(self):
        """Return (event, accepted). Mirrors firmware car_exits()."""
        if self.count > 0:
            self.count -= 1
            self._update_status()
            return "CAR OUT", True
        return "EMPTY", False


if __name__ == "__main__":
    gate = GarageGate()
    for _ in range(16):
        print(gate.car_enters())
    print("full?", gate.red, "free?", gate.green)
    for _ in range(17):
        print(gate.car_exits())