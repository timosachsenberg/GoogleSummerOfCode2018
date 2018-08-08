import sys

_ANNOTATION = '<UserParam type="string" name="target_decoy" value="{}"/>\n'


def main():
    if len(sys.argv[1:]) != 2:
        error_msg = "usage: python {} <in.idXML> <out.idXML>"
        sys.exit(error_msg.format(sys.argv[0]))

    in_file, out_file = sys.argv[1:]

    with open(in_file) as f, open(out_file, "w") as o:
        for line in f:
            # if "<ProteinHit" in line:
            #     o.write(line)
            #     target_decoy = "decoy" if "random_" in line else "target"
            #     line = _ANNOTATION.format(target_decoy)

            if "<ProteinHit" in line:
                o.write(line)
                line = '<UserParam type="string" name="isDecoy" value="true"/>\n'

            if '<UserParam type="string" name="target_decoy" value="target"/>' in line:
                line = line.replace('value="target"', 'value="decoy"')

            if '<UserParam type="string" name="isDecoy" value="false"/>' in line:
                line = line.replace('value="false"', 'value="true"')

            o.write(line)


if __name__ == '__main__':
    main()
