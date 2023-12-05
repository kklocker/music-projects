import getopt
import random
import sys

intervals = [1, 2, 3, 4, 5, 6, 7]
primes = [2, 3, 5, 7, 11, 13, 17]
limbs = set(["LH", "RH", "LF", "RF"])
number_of_limbs = 4
(options, args) = getopt.getopt(
    sys.argv[1:], "pl:x:", ["prime-only", "number-of-limbs =", "pattern = "]
)

primes_only = False
CONSOLE_LENGTH = 50

custom_pattern = ""
use_custom_pattern = False

for name, arg_value in options:
    if name in ("-p", "prime-only"):
        primes_only = True
    if name in ("-l", "number-of-limbs"):
        number_of_limbs = int(arg_value)
        if number_of_limbs > 4:
            raise Exception("Invalid input")
    if name in ("-x", "pattern"):
        # -x xx-x--x--
        custom_pattern = arg_value
        use_custom_pattern = True

if primes_only:
    interval_set = set(primes)
else:
    interval_set = set(intervals)


def print_limb(representation: str, value):
    if value == custom_pattern:
        print(bcolors.OKBLUE + f"{representation}: XX  |" + bcolors.ENDC, end="")
        n_repeat_times = CONSOLE_LENGTH // len(custom_pattern)
        extra = CONSOLE_LENGTH % len(custom_pattern)
        pattern = custom_pattern.replace("-", " ")
        padded_pattern = str.join("", [f" {x} " for x in pattern])
        extra_pattern = str.join("", [f" {x} " for x in pattern[:extra]])
        string_to_print = padded_pattern * n_repeat_times + extra_pattern
        print(bcolors.WARNING + string_to_print + bcolors.ENDC)

    else:
        print(
            bcolors.OKBLUE + f"{representation}: {value:2d}  |" + bcolors.OKBLUE, end=""
        )
        for x in range(CONSOLE_LENGTH):
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
    SPACE_CHAR = " . "
    print(bcolors.OKBLUE + ("---" * (CONSOLE_LENGTH + 3)) + bcolors.ENDC)
    print()
    print(bcolors.OKBLUE + ("Limb    |" + SPACE_CHAR * CONSOLE_LENGTH) + bcolors.ENDC)

    if "RH" in limb_dict:
        print_limb("RH", limb_dict["RH"])
    if "LH" in limb_dict:
        print_limb("LH", limb_dict["LH"])
    if "RF" in limb_dict:
        print_limb("RF", limb_dict["RF"])
    if "LF" in limb_dict:
        print_limb("LF", limb_dict["LF"])
    print()
    print("---" * (CONSOLE_LENGTH + 3))
