import logging
import sys
from dataclasses import dataclass
from pprint import pformat
from typing import List, Optional

LOG_LEVEL = logging.INFO

log = logging.getLogger()
log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel(LOG_LEVEL)


@dataclass
class Number:
    value: int
    marked: bool = False

    @staticmethod
    def from_str(value: str) -> "Number":
        return Number(int(value))

    def __repr__(self) -> str:
        return str(self.value)


class Bingo(Exception):
    def __init__(self, score: int):
        self._score = score

    @property
    def score(self) -> int:
        return self._score


class BoardNotRectangular(Exception):
    pass


class Board:
    def __init__(self):
        self._rows: Optional[int] = 0
        self._columns: Optional[int] = None
        self._board: List[List[Number]] = []
        self._row_marks: List[int] = []
        self._column_marks: List[int] = []
        self._bingo: bool = False

    def append_row(self, row: str) -> None:
        new_row = [Number.from_str(n) for n in row.split()]
        if not self._columns:
            self._columns = len(new_row)
            self._column_marks = [0] * self._columns
        else:
            if self._columns != len(new_row):
                raise BoardNotRectangular
        self._board.append(new_row)
        self._row_marks.append(0)
        self._rows += 1

    def mark(self, value: int):
        if self._bingo:
            return
        for line, row in enumerate(self._board):
            for column, element in enumerate(row):
                if element.value == value:
                    self._row_marks[column] += 1
                    self._column_marks[line] += 1
                    element.marked = True
                    if self.bingo:
                        raise Bingo(self.unmarked_sum * value)

    @property
    def unmarked_sum(self) -> int:
        return sum([e.value
                    for row in self._board
                    for e in row
                    if not e.marked])

    @property
    def bingo(self) -> bool:
        self._bingo = self._rows in self._row_marks or self._columns in self._column_marks
        return self._bingo

    def __repr__(self) -> str:
        return pformat(self._board, compact=False, width=50)


def play(draws: List[int], boards: List[Board]):
    log.info("Time to bingo!\n"
             f"Draws: {draws}\n")
    if log.level == logging.DEBUG:
        board_reprs = "\n\n".join([str(b) for b in boards])
        log.debug(f"Boards:\n{board_reprs}")

    first_bingo: Optional[int] = None
    last_bingo: Optional[int] = None
    for draw in draws:
        for board in boards:
            try:
                board.mark(draw)
            except Bingo as e:
                if not first_bingo:
                    first_bingo = e.score
                last_bingo = e.score
    log.info(f"BINGO! \n"
             f"First board score: {first_bingo}\n"
             f"Last board score: {last_bingo}")


def main():
    with open("input.txt") as input_file:
        draws = [int(n) for n in input_file.readline().strip().split(",")]
        boards = []
        while current_line := input_file.readline():
            cleaned_line = current_line.strip()
            if not cleaned_line:
                boards.append(Board())
            else:
                boards[-1].append_row(cleaned_line)
        play(draws, boards)


if __name__ == "__main__":
    main()
