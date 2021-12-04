import logging
import sys
from collections import defaultdict
from typing import List

LOG_LEVEL = logging.INFO

log = logging.getLogger()
log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel(LOG_LEVEL)


def _flip_bits(bits: str) -> str:
    return bits.replace("1", "_").replace("0", "1").replace("_", "0")


def _most_common_bits(numbers: List[str]) -> str:
    bit_counter = defaultdict(lambda: defaultdict(int))
    n_bits = len(numbers[0])
    for num in numbers:
        for index, bit in enumerate(num):
            bit_counter[bit][index] += 1
    most_bits = [
        "1" if bit_counter["1"][index] >= bit_counter["0"][index] else "0"
        for index in range(n_bits)
    ]

    return "".join(most_bits)


def _filter_numbers(numbers: List[str], least_common: bool = False) -> str:
    bit_index = 0
    while len(numbers) > 1:
        common_bits = _most_common_bits(numbers)
        numbers = [n for n in numbers if least_common ^ (n[bit_index] == common_bits[bit_index])]
        bit_index += 1
    return numbers[0]


def main():
    with open("input.txt") as input_file:
        numbers = [line.strip() for line in input_file]

    common_bits = _most_common_bits(numbers)
    gamma_rate = int(common_bits, 2)
    epsilon_rate = int(_flip_bits(common_bits), 2)
    log.info(f"Common bits: {common_bits}, "
             f"Gamma: {gamma_rate}, "
             f"Epsilon: {epsilon_rate}, "
             f"Result: {gamma_rate * epsilon_rate}")

    oxy_bits = _filter_numbers(numbers)
    co2_bits = _filter_numbers(numbers, least_common=True)
    oxy_rate = int(oxy_bits, 2)
    co2_rate = int(co2_bits, 2)
    log.info(f"Oxygen bits: {oxy_bits}, "
             f"rate: {oxy_rate}, "
             f"CO2 bits: {co2_bits}, "
             f"rate: {co2_rate}, "
             f"Result: {oxy_rate * co2_rate}")


if __name__ == "__main__":
    main()
