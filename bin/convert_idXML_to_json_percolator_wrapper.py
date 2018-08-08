import os

_DIR = "/home/mersmann/gsoc/analysis/"
_SCRIPT = "/home/mersmann/gsoc/analysis/convert_idXML_to_json_percolator.py"


def main():
    filenames = [
        os.path.join(_DIR, f)
        for f in os.listdir(_DIR)
        if f.endswith(".idXML") and "percolator" in f
    ]

    for filename in filenames:
        out = filename.replace(".idXML", ".json")
        os.system(
            "python {} {} {}".format(_SCRIPT, filename, out)
        )


if __name__ == '__main__':
    main()
