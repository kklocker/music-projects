# Taken from https://stackoverflow.com/a/2150512/10074443
def shift(seq, n):
    n = n % len(seq)
    return seq[n:] + seq[:n]
