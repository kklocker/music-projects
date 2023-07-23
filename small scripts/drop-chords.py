import random
import sys

from modes import IONIAN
from notes import Notes

# random.seed(420)

DROP_MODE: int = 0
MAX_FINGER_SPLIT_CONST = 2  # up or down
TUNING = "EADGBe"
START_FRET = MAX_FINGER_SPLIT_CONST


MODE = IONIAN

if len(sys.argv) > 1:
    inputmode = int(sys.argv[1])
    DROP_MODE = inputmode


startNote = Notes(random.randint(0, 11))
print(f"Root note: {startNote}")


def generate_chord(startNote: Notes, count=4, mode=IONIAN) -> list[Notes]:
    notes = [Notes((v + startNote) % 12) for v in mode]
    availableNotes = set(notes)
    # print(availableNotes)
    availableNotes.remove(startNote)
    chord = [startNote]

    for _ in range(count - 1):
        sample_to_pop = random.sample(tuple(availableNotes), 1)[0]
        # print(sample_to_pop)

        availableNotes.remove(sample_to_pop)
        chord.append(sample_to_pop)

    return chord


chord = generate_chord(startNote)
print(f"Generated chord: {chord}")


def find_finger_placement(chord: list[Notes]) -> list[(int, int, Notes)]:
    """
    returns:  (string(int), fret, Note)
    """
    returnlist = []

    # bass on the two lowest strings -- take the one furthest up on the fretboard
    start = chord[0]
    firstString = Notes[TUNING[0].upper()]
    secondString = Notes[TUNING[1].upper()]

    fretFirst = (start - firstString) % 12
    fretSecond = (start - secondString) % 12

    if fretFirst <= fretSecond:
        # we use the first string
        returnlist.append((6, fretFirst, start))
    else:
        returnlist.append((5, fretSecond, start))

    for note in chord[1:]:
        base_fret_pos = returnlist[0][1]
        found = False
        for idx, tun in enumerate(TUNING[2:]):
            tun_note = Notes[tun.upper()]
            fret = (note - tun_note) % 12
            frets = [fret, fret + 12]
            filtered = [
                x
                for x in filter(
                    lambda f: abs(f - base_fret_pos) <= MAX_FINGER_SPLIT_CONST, frets
                )
            ]
            if len(filtered) == 0:
                continue

            selected_fret = filtered[0]
            returnlist.append((4 - idx, selected_fret, note))
            found = True
        if not found:
            return RuntimeError("SDASDKAKHSDPGØLHSØGL1")

    return returnlist


fingers = find_finger_placement(chord)
print("String, Fret, Note:")
for finger in fingers:
    print(finger)
