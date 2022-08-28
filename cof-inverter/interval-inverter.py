import sys
from enum import IntEnum
from itertools import pairwise


class Notes(IntEnum):
    C = 0
    Csh = 1
    Db = 1
    D = 2
    Dsh = 3
    Eb = 3
    E = 4
    F = 5
    Fsh = 6
    Gb = 6
    G = 7
    Gsh = 8
    Ab = 8
    A = 9
    Ash = 10
    Bb = 10
    B = 11

    def __repr__(self) -> str:
        if self._name_[-2:] == "sh":
            return f"{self._name_[0]+'#'}"
        return f"{self._name_}"


notes = sys.argv[1:]

notes_as_enum = [Notes[note] for note in notes]
current = notes_as_enum[0]
flipped = [current]
diffs = [b - a for (a, b) in pairwise(notes_as_enum)]

for diff in diffs:
    prev = flipped[-1]
    next_flip = Notes((prev.value - diff) % 12)
    flipped.append(next_flip)

[print(f"{repr(n)}") for n in flipped]
