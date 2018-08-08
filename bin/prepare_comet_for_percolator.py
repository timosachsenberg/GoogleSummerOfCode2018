import sys
import pandas as pd


def main():
    if len(sys.argv[1:]) != 3:
        error_msg = "usage: python {} <target.pin> <decoy.pin> <out>"
        sys.exit(error_msg.format(sys.argv[0]))

    target = pd.read_csv(sys.argv[1], sep="\t")
    decoy = pd.read_csv(sys.argv[2], sep="\t")
    decoy["label"] = -1

    pd.concat(
        [target, decoy],
        ignore_index=True
    ).to_csv(
        sys.argv[3],
        sep="\t",
        index=False
    )


if __name__ == '__main__':
    main()
