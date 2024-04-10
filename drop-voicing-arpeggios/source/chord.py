from source.arr import shift


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
            current += n_tones - 1

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
    scale_note = avg % (n_tones - 1)
    octave = avg // n_tones
    closest_scale_tone = min(scale, key=lambda x: abs(x - scale_note))
    adjusted_to_octave_scaletone = closest_scale_tone + (n_tones - 1) * octave
    return adjusted_to_octave_scaletone
