import logging
import sys
from typing import TextIO, List, Iterator

LOG_LEVEL = logging.DEBUG

log = logging.getLogger()
log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel(LOG_LEVEL)


def _window(input_file: TextIO, window_size) -> Iterator[int]:
    _read_values: List[int] = []
    for _ in range(window_size - 1):
        _read_values.append(int(input_file.readline()))
    for line in input_file:
        _read_values.append(int(line))
        s = sum(_read_values)
        log.debug(f"Window: {_read_values}, sum: {s}")
        yield sum(_read_values)
        _read_values.pop(0)


def count_increases(input_file: TextIO, window_size: int):
    n_increased: int = 0
    iterator = _window(input_file, window_size)
    current_value = next(iterator)
    for value in iterator:
        msg = f"{value}: "
        if value > current_value:
            msg = f"{msg}increased"
            n_increased += 1
        log.debug(msg)
        current_value = value
    log.info(f"Done, counted {n_increased} increases")


def main():
    with open("input.txt") as input_file:
        log.info("Counting with sliding window size 1")
        count_increases(input_file, 1)

        input_file.seek(0)
        log.info("Counting with sliding window size 3")
        count_increases(input_file, 3)


if __name__ == "__main__":
    main()
