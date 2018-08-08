import sys

_SCAN_NR_INDEX = 2


def main():
    if len(sys.argv[1:]) != 2:
        error_msg = "python {} <in> <out>".format(
            sys.argv[0]
        )
        sys.exit(error_msg)

    in_file, out_file = sys.argv[1:]

    with open(in_file) as f, open(out_file, "w") as o:
        line_number = 0
        for line in f:
            new_line = line

            if not line.startswith("SpecId"):
                line_number += 1
                split = line.split()
                split[_SCAN_NR_INDEX] = str(line_number)
                new_line = "\t".join(split) + "\n"

            o.write(new_line)


if __name__ == '__main__':
    main()
