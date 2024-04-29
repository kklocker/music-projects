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

from midiutil.MidiFile import MIDIFile

n_tones = 12  #  Assuming western 12-tone notes

# TODO: Take as input
scale = [
    0,
    2,
    3,
    5,
    7,
    9,
    11,
]

assert max(scale) < n_tones and min(scale) >= 0

# TODO: Take as  input
root = 1  # 1-12, 1 == C

scale_length = len(scale)

# Generate chords from each note in the scale by stacking "thirds"
chord_stacking_increment = 2  # thirds

inversion = 0  # 0..3; Four different ways to play the chord


def write_midi(title: str, sequence: list[int]):
    mf = MIDIFile(1)
    track = 0
    time = 0
    mf.addTrackName(track, time, title)
    mf.addTempo(track, time, 120)

    channel = 0
    volume = 100

    base_pitch = 60 + root - 1  # C4  + root diff
    time = 0
    duration = 0.25  # Quarter note

    for note in sequence:
        mf.addNote(track, channel, base_pitch + note, time, duration, volume)
        time += duration

    # write it to disk
    with open(f"output/{title}.mid", "wb") as outf:
        mf.writeFile(outf)


if __name__ == "__main__":
    print(f"Root: {Notes(root).name}")
    print(f"Scale notes (relative to root): {scale}")
    print(f"Variant (inversion): {inversion}")

    print_colored_and_reset("Exercise sequence: ", color=bcolors.HEADER)

    for idx, root_note in enumerate(scale):
        scale_chord_for_root = []
        next_scale_chord_for_root = []

        increment = 0
        for i in range(4):
            scale_chord_for_root.append(scale[(idx + increment) % scale_length])
            next_scale_chord_for_root.append(
                scale[(idx + 1 + increment) % scale_length]
            )
            increment += chord_stacking_increment

        adjusted_scalechord = adjustOctaveForAscendingChord(
            scale_chord_for_root, n_tones
        )
        inversion_note = scale_chord_for_root[inversion]

        next_inversion_note = next_scale_chord_for_root[inversion]
        next_adjusted = shiftForInversion(
            next_scale_chord_for_root, next_inversion_note
        )

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

        lastFillerNotes = [next_adjusted[2], next_adjusted[3]]

        print_colored_chord(adjusted_drop_2, bcolors.OKBLUE)
        print_filler_note(firstFillerNote)
        print_colored_chord(adjusted_drop_3, bcolors.OKGREEN)
        print_filler_note(secondFillerNote)
        print_colored_chord(adjusted_scalechord[::-1], bcolors.OKCYAN)
        print_filler_note(lastFillerNotes[0])
        print_filler_note(lastFillerNotes[1])

        print()

        start_octave = 4

        total_list = (
            adjusted_drop_2
            + [firstFillerNote]
            + adjusted_drop_3
            + [secondFillerNote]
            + adjusted_scalechord[::-1]
            + lastFillerNotes
        )

        write_midi(
            f"r{root}-inv{inversion}-inc{chord_stacking_increment}-ix{idx}",
            total_list,
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
