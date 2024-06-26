# Taken from https://stackoverflow.com/a/287944/10074443
import typing


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


def print_colored_and_reset(
    message: str,
    color: str,
):
    print(f"{color}{message}{bcolors.ENDC}")
