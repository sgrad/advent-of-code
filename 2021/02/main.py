import logging
import sys

LOG_LEVEL = logging.INFO

log = logging.getLogger()
log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel(LOG_LEVEL)


class Sub:
    def __init__(self):
        self._x = 0
        self._y = 0

    def _move_down(self, units: int) -> None:
        log.debug(f"Moving down {units} units")
        self._y += units

    def _move_up(self, units: int) -> None:
        log.debug(f"Moving up {units} units")
        self._y -= units

    def _move_forward(self, units: int) -> None:
        log.debug(f"Moving forward {units} units")
        self._x += units

    def move(self, direction: str, raw_units: str) -> None:
        log.debug(f"Moving sub direction: {direction}, raw units: {raw_units}")
        getattr(self, f"_move_{direction}")(int(raw_units))

    @property
    def position(self) -> int:
        log.debug(f"Current position forward: {self._x}, depth: {self._y}")
        return self._x * self._y


class FancySub(Sub):
    def __init__(self):
        super().__init__()
        self._aim = 0

    def _move_down(self, units: int) -> None:
        log.debug(f"Aiming down {units} units")
        self._aim += units

    def _move_up(self, units: int) -> None:
        log.debug(f"Aiming up {units} units")
        self._aim -= units

    def _move_forward(self, units: int) -> None:
        _y_increment = self._aim * units
        log.debug(f"Moving forward {units} units, down: {_y_increment}, current aim: {self._aim}")
        self._x += units
        self._y += _y_increment


def main():
    with open("input.txt") as input_file:
        sub = Sub()
        for line in input_file:
            direction, raw_units = line.split()
            sub.move(direction, raw_units)
        log.info(f"Done moving, first sub is at: {sub.position}")

        input_file.seek(0)
        fancy_sub = FancySub()
        for line in input_file:
            direction, raw_units = line.split()
            fancy_sub.move(direction, raw_units)
        log.info(f"Done moving, second sub is at: {fancy_sub.position}")


if __name__ == "__main__":
    main()
