from source.chord import (
    adjustOctaveForAscendingChord,
    getDrop2,
    getDrop3,
    getFillerNote,
    shiftForInversion,
)
from source.colors import bcolors, print_colored_and_reset


n_tones = 12  #  Assuming western 12-tone notes

# TODO: Take as input
scale = [
    1,
    3,
    5,
    6,
    8,
    10,
    11,
]  # Major scale Notes are 1-indexed to easier conform with interval names root = 1. For instance 1=C, 3 = D, 5 = E, 6 = F etc..

assert max(scale) < n_tones and min(scale) > 0

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

        # print(f"Scale chord: {scale_chord_for_root}")
        adjusted_scalechord = adjustOctaveForAscendingChord(
            scale_chord_for_root, n_tones
        )
        # print(f"Adjusted: {adjusted_scalechord}")
        # print()
        inversion_note = scale_chord_for_root[inversion]

        drop_2 = getDrop2(scale_chord_for_root)
        drop_2 = shiftForInversion(drop_2, inversion_note)
        # print(f"Drop 2: {drop_2}")
        adjusted_drop_2 = adjustOctaveForAscendingChord(drop_2, n_tones)
        # print(f"Adjusted: {adjusted_drop_2}")
        # print()
        drop_3 = getDrop3(scale_chord_for_root)
        drop_3 = shiftForInversion(drop_3, inversion_note)
        adjusted_drop_3 = adjustOctaveForAscendingChord(drop_3, n_tones)

        # print(f"Drop 3: {drop_3}")
        # print(f"Adjusted: {adjusted_drop_3}")
        # print()

        # sequence: drop 2 asc + filler note + drop 3 asc + filler note(s) + closed form desc

        firstFillerNote = getFillerNote(
            adjusted_drop_2, adjusted_drop_3, scale, n_tones
        )

        # print(f"Filler note: {firstFillerNote}")

        secondFillerNote = getFillerNote(
            adjusted_drop_3, adjusted_scalechord[::-1], scale, n_tones
        )

        # print(f"Second filler note: {secondFillerNote}")

        print_colored_and_reset("Total sequence: ", color=bcolors.HEADER)

        def print_colored_chord(chord, color: str):
            for note in chord:
                print(color, end="")
                print(f"{note:02d}", end="")
                print(bcolors.ENDC, end="  ")

        def print_filler_note(fillerNote):
            print(f"{bcolors.WARNING}{fillerNote:2d}{bcolors.ENDC}", end="  ")

        print_colored_chord(adjusted_drop_2, bcolors.OKBLUE)
        print_filler_note(firstFillerNote)
        print_colored_chord(adjusted_drop_3, bcolors.OKGREEN)
        print_filler_note(secondFillerNote)
        print_colored_chord(adjusted_scalechord[::-1], bcolors.OKCYAN)

        print()
        print()
