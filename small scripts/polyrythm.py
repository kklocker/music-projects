import getopt
import math
import random
import sys

from midiutil import MIDIFile

intervals = [1, 2, 3, 4, 5, 6, 7]
primes = [2, 3, 5, 7, 11, 13, 17]
limbs = set(["LH", "RH", "LF", "RF"])
number_of_limbs = 4
(options, args) = getopt.getopt(
    sys.argv[1:],
    "pml:x:",
    ["prime-only", "midifile", "number-of-limbs =", "pattern = "],
)

primes_only = False
TOTAL_LENGTH = None  # set to lcm later

custom_pattern = ""
use_custom_pattern = False
write_midi = False

for name, arg_value in options:
    if name in ("-p", "prime-only"):
        primes_only = True
    if name in ("-l", "number-of-limbs"):
        number_of_limbs = int(arg_value)
        if number_of_limbs > 4:
            raise Exception("Invalid input")
    if name in ("-m", "midifile"):
        write_midi = True
    if name in ("-x", "pattern"):
        # -x xx-x--x--
        custom_pattern = arg_value
        use_custom_pattern = True

if primes_only:
    interval_set = set(primes)
else:
    interval_set = set(intervals)


def write_midi_file(limb_dict):
    """
    Write a MIDI file with the given dictionary of pattern for individual limbs

    Midi map: https://musescore.org/sites/musescore.org/files/General%20MIDI%20Standard%20Percussion%20Set%20Key%20Map.pdf

    """
    mf = MIDIFile(1)
    track = 0
    time = 0
    title = f"Polyrhythm-{'_'.join([str(x) if x!= custom_pattern else 'custom' for x in limb_dict.values()])}"
    mf.addTrackName(track, time, title)
    mf.addTempo(track, time, 120)

    limb_dict.items()

    channel = 0
    volume = 100

    duration = 0.25  # Quarter note

    def writePattern(pattern, note):
        time = 0
        iteration = 0
        if pattern == custom_pattern:
            n_repeat_times = TOTAL_LENGTH // len(custom_pattern)
            for _ in range(n_repeat_times):
                for x in custom_pattern:
                    if x == "x":
                        mf.addNote(track, channel, note, time, duration, volume)
                    time += duration

        else:
            while iteration < TOTAL_LENGTH:
                time = duration * iteration
                if iteration % pattern == 0:
                    mf.addNote(track, channel, note, time, duration, volume)
                iteration += 1

    if "RH" in limb_dict:
        writePattern(limb_dict["RH"], 41)  # 41 = Low floor tom
    if "LH" in limb_dict:
        writePattern(limb_dict["LH"], 38)  # 38 = Acoustic snare
    if "RF" in limb_dict:
        writePattern(limb_dict["RF"], 36)  # 36 = Bass drum 1
    if "LF" in limb_dict:
        writePattern(limb_dict["LF"], 44)  # 44 = Pedal Hi-Hat

    filename = f"output/{title}.mid"
    print("Saving midi file to", filename)
    # write it to disk
    with open(filename, "wb") as outf:
        mf.writeFile(outf)


def print_limb(representation: str, value):
    if value == custom_pattern:
        print(bcolors.OKBLUE + f"{representation}: XX  |" + bcolors.ENDC, end="")
        n_repeat_times = TOTAL_LENGTH // len(custom_pattern)
        extra = TOTAL_LENGTH % len(custom_pattern)
        pattern = custom_pattern.replace("-", " ")
        padded_pattern = str.join("", [f" {x} " for x in pattern])
        extra_pattern = str.join("", [f" {x} " for x in pattern[:extra]])
        string_to_print = padded_pattern * n_repeat_times + extra_pattern
        print(bcolors.WARNING + string_to_print + bcolors.ENDC)

    else:
        print(
            bcolors.OKBLUE + f"{representation}: {value:2d}  |" + bcolors.OKBLUE, end=""
        )
        for x in range(TOTAL_LENGTH):
            if x % value == 0:
                print(bcolors.OKGREEN + " x " + bcolors.ENDC, end="")
            else:
                print("   ", end="")
        print()


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


if __name__ == "__main__":
    limb_dict = {}
    for limb_idx in range(number_of_limbs):
        limb = random.choice(sorted(limbs))
        limbs.remove(limb)
        if use_custom_pattern:
            use_custom_pattern = False
            limb_dict[limb] = custom_pattern
        else:
            interval_for_limb = random.choice(sorted(interval_set))
            limb_dict[limb] = interval_for_limb
            interval_set.remove(interval_for_limb)

    limb_dict = dict(sorted(limb_dict.items()))

    print(limb_dict)
    lcm = math.lcm(
        *[x if x != custom_pattern else len(custom_pattern) for x in limb_dict.values()]
    )

    TOTAL_LENGTH = lcm

    if write_midi:
        write_midi_file(limb_dict)

    else:
        SPACE_CHAR = " . "
        print(bcolors.OKBLUE + ("---" * (TOTAL_LENGTH + 3)) + bcolors.ENDC)
        print()
        print(bcolors.OKBLUE + ("Limb    |" + SPACE_CHAR * TOTAL_LENGTH) + bcolors.ENDC)

        if "RH" in limb_dict:
            print_limb("RH", limb_dict["RH"])
        if "LH" in limb_dict:
            print_limb("LH", limb_dict["LH"])
        if "RF" in limb_dict:
            print_limb("RF", limb_dict["RF"])
        if "LF" in limb_dict:
            print_limb("LF", limb_dict["LF"])
        print()
        print("---" * (TOTAL_LENGTH + 3))
