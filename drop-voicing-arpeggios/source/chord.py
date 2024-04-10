from source.arr import shift
from source.colors import bcolors


def getDrop2(chord: list[int]) -> list[int]:
    assert len(chord) == 4
    return [chord[2], chord[0], chord[1], chord[3]]


def getDrop3(chord: list[int]) -> list[int]:
    assert len(chord) == 4
    return [chord[1], chord[0], chord[2], chord[3]]


def shiftForInversion(chord: list[int], inversion_note: int) -> list[int]:
    index = chord.index(inversion_note)
    return shift(chord, index)


def adjustOctaveForAscendingChord(chord: list[int], n_tones: int) -> list[int]:
    prev = 0
    res = []
    for current in chord:
        while current < prev:
            current += n_tones

        prev = current
        res.append(current)

    return res


def getFillerNote(
    firstChord: list[int], secondChord: list[int], scale: list[int], n_tones: int
) -> int:
    """Gets the scale tone that lies closest to in the middle of the two adjecent"""
    lastNoteInFirstChord = firstChord[-1]
    firstNoteInSecondChord = secondChord[0]
    avg = (lastNoteInFirstChord + firstNoteInSecondChord) // 2
    (note, octave) = get_note_and_octave(avg, n_tones)
    closest_scale_tone = min(scale, key=lambda x: abs(x - note))
    adjusted_to_octave_scaletone = closest_scale_tone + n_tones * octave
    return adjusted_to_octave_scaletone


def get_octave(note: int, n_tones: int):
    return note // n_tones


def get_note_and_octave(note: int, n_tones: int) -> tuple[int, int]:
    normalized_note = note % n_tones
    octave = get_octave(note, n_tones)
    return (normalized_note, octave)


def print_colored_chord(chord, color: str):
    for note in chord:
        print(color, end="")
        print(f"{note:02d}", end="")
        print(bcolors.ENDC, end="   ")


def print_filler_note(fillerNote):
    print(f"{bcolors.WARNING}{fillerNote:2d}{bcolors.ENDC}", end="   ")
