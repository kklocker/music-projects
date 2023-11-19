import random
import sys
import getopt

intervals = [1, 2, 3, 4, 5, 6, 7]
primes = [2, 3, 5, 7, 11, 13, 17]
limbs = set(["LH", "RH", "LF", "RF"])
number_of_limbs = 4
(options, args) = getopt.getopt(
    sys.argv[1:], "pl:", ["prime-only", "number-of-limbs ="]
)

primes_only = False


for name, value in options:
    if name in ("-p", "prime-only"):
        primes_only = True
    if name in ("-l", "number-of-limbs"):
        number_of_limbs = int(value)
        if number_of_limbs > 4:
            raise Exception("Invalid input")

if primes_only:
    interval_set = set(primes)
else:
    interval_set = set(intervals)

if __name__ == "__main__":
    limb_dict = {}

    print(options)
    for limb_idx in range(number_of_limbs):
        limb = random.choice(sorted(limbs))
        limbs.remove(limb)
        interval_for_limb = random.choice(sorted(interval_set))
        interval_set.remove(interval_for_limb)
        limb_dict[limb] = interval_for_limb

    limb_dict = dict(sorted(limb_dict.items()))
    CONSOLE_LENGTH = 50
    SPACE_CHAR = " . "
    print()
    print("--------|" + SPACE_CHAR * CONSOLE_LENGTH)
    for k, v in limb_dict.items():
        print(f"{k}: {v:2d}  |", end="")
        for x in range(CONSOLE_LENGTH):
            if x % v == 0:
                print(" x ", end="")
            else:
                print("   ", end="")
        print()
