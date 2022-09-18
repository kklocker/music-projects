import sys
from itertools import pairwise

from notes import Notes

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
