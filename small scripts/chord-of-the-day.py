import random
import sys
from datetime import datetime

from notes import Notes

"""
❯ python .\chord-of-the-day.py 5
C#m7
D#mmaj7
G#maj7sus2b5
D#maj7#5
E7#5
"""

n = 1
cli_args = sys.argv
if len(cli_args) > 1:
    n = int(cli_args[1])

d0 = datetime(1996, 5, 2)  # Pick an arbitrary date in the past
d1 = datetime.now()
delta = d1 - d0
random.seed(delta.days)

for i in range(n):

    third_var = random.choice(range(4))
    fifth_var = random.choice(range(3))
    seventh_var = random.choice(range(2))
    root = Notes(random.choice(range(12)))

    third_str = ""
    match third_var:
        case 0:
            third_str = "sus2"
        case 1:
            third_str = "m"
        case 2:
            third_str = ""
        case 3:
            third_str = "sus4"

    fifth_str = ""
    match fifth_var:
        case 0:
            fifth_str = "b5"
        case 1:
            fifth_str = ""
        case 2:
            fifth_str = "#5"

    seventh_str = ""
    match seventh_var:
        case 0:
            seventh_str = "7"
        case 1:
            seventh_str = "maj7"
    chord = ""
    if third_var == 0 or third_var == 3:
        chord = f"{root}{seventh_str}{third_str}{fifth_str}"
    else:
        chord = f"{root}{third_str}{seventh_str}{fifth_str}"

    print(chord)
