import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python_modules'))

from garage_gate import GarageGate, MAX_CARS


class TestGarageGate:
    def setup_method(self):
        self.gate = GarageGate()

    def test_max_cars_constant(self):
        assert MAX_CARS == 15

    def test_initial_state(self):
        assert self.gate.count == 0
        assert self.gate.green is True
        assert self.gate.red is False

    def test_increment(self):
        event, ok = self.gate.car_enters()
        assert ok is True
        assert event == "CAR IN"
        assert self.gate.count == 1

    def test_decrement(self):
        self.gate.car_enters()
        event, ok = self.gate.car_exits()
        assert ok is True
        assert event == "CAR OUT"
        assert self.gate.count == 0

    def test_full_at_15(self):
        for _ in range(15):
            self.gate.car_enters()
        assert self.gate.count == 15
        assert self.gate.red is True
        assert self.gate.green is False

    def test_cannot_exceed_max(self):
        for _ in range(20):
            self.gate.car_enters()
        assert self.gate.count == 15
        event, ok = self.gate.car_enters()
        assert ok is False
        assert event == "GARAGE FULL"

    def test_cannot_go_below_zero(self):
        for _ in range(5):
            self.gate.car_exits()
        assert self.gate.count == 0
        event, ok = self.gate.car_exits()
        assert ok is False
        assert event == "EMPTY"

    def test_green_off_when_full(self):
        self.gate.car_enters()  # count 1
        assert self.gate.green is True
        for _ in range(14):
            self.gate.car_enters()  # count 15
        assert self.gate.green is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])