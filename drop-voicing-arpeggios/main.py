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
root = 1 # 1-12, 1 == C

scale_length = len(scale)


# Generate chords from each note in the scale by stacking "thirds"
chord_stacking_increment = 2 # thirds
for (idx, root_note) in enumerate(scale):
    scale_chord_for_root = []

    increment = 0
    for i in range(4):
        scale_chord_for_root.append(scale[(idx + increment)% scale_length])
        increment += chord_stacking_increment
    
    print(scale_chord_for_root)

    drop_2 = [scale_chord_for_root[2], scale_chord_for_root[0], scale_chord_for_root[1], scale_chord_for_root[3]]
    drop_3 = [scale_chord_for_root[1], scale_chord_for_root[0], scale_chord_for_root[2], scale_chord_for_root[3]]
    print(f"Drop 2: {drop_2}")
    print(f"Drop 3: {drop_3}")


