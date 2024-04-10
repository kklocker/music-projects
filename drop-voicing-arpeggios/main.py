from source.chord import (
    adjustOctaveForAscendingChord,
    get_note_and_octave,
    getDrop2,
    getDrop3,
    getFillerNote,
    print_colored_chord,
    print_filler_note,
    shiftForInversion,
)
from source.colors import bcolors, print_colored_and_reset
from source.notes import Notes


n_tones = 12  #  Assuming western 12-tone notes

# TODO: Take as input
scale = [
    0,
    2,
    4,
    5,
    7,
    9,
    11,
]  # Major scale Notes are 1-indexed to easier conform with interval names root = 1. For instance 1=C, 3 = D, 5 = E, 6 = F etc..

assert max(scale) < n_tones and min(scale) >= 0

# TODO: Take as  input
root = 1  # 1-12, 1 == C

scale_length = len(scale)

# Generate chords from each note in the scale by stacking "thirds"
chord_stacking_increment = 2  # thirds

inversion = 0  # 0..3; Four different ways to play the chord

if __name__ == "__main__":
    for idx, root_note in enumerate(scale):
        scale_chord_for_root = []

        increment = 0
        for i in range(4):
            scale_chord_for_root.append(scale[(idx + increment) % scale_length])
            increment += chord_stacking_increment

        adjusted_scalechord = adjustOctaveForAscendingChord(
            scale_chord_for_root, n_tones
        )
        inversion_note = scale_chord_for_root[inversion]

        drop_2 = getDrop2(scale_chord_for_root)
        drop_2 = shiftForInversion(drop_2, inversion_note)
        adjusted_drop_2 = adjustOctaveForAscendingChord(drop_2, n_tones)

        drop_3 = getDrop3(scale_chord_for_root)
        drop_3 = shiftForInversion(drop_3, inversion_note)
        adjusted_drop_3 = adjustOctaveForAscendingChord(drop_3, n_tones)

        firstFillerNote = getFillerNote(
            adjusted_drop_2, adjusted_drop_3, scale, n_tones
        )

        secondFillerNote = getFillerNote(
            adjusted_drop_3, adjusted_scalechord[::-1], scale, n_tones
        )
        print_colored_and_reset("Total sequence: ", color=bcolors.HEADER)

        print_colored_chord(adjusted_drop_2, bcolors.OKBLUE)
        print_filler_note(firstFillerNote)
        print_colored_chord(adjusted_drop_3, bcolors.OKGREEN)
        print_filler_note(secondFillerNote)
        print_colored_chord(adjusted_scalechord[::-1], bcolors.OKCYAN)

        print()

        start_octave = 4

        total_list = (
            adjusted_drop_2
            + [firstFillerNote]
            + adjusted_drop_3
            + [secondFillerNote]
            + adjusted_scalechord[::-1]
        )

        for scale_note in total_list:
            (note, scale_octave) = get_note_and_octave(scale_note, n_tones)
            octave_for_note = scale_octave + start_octave
            actual_note = (root + note) % n_tones
            if actual_note == 0:
                actual_note = n_tones

            s_rep = f"{Notes(actual_note).name}{octave_for_note}"
            print(f"{s_rep:4s}", end=" ")

        print()
        print()
