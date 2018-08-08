import os

_DIR = "/home/mersmann/gsoc/analysis/"
_SCRIPT = "/home/mersmann/gsoc/analysis/convert_idXML_to_json.py"


def main():
    filenames = [
        os.path.join(_DIR, f)
        for f in os.listdir(_DIR)
        if f.endswith(".idXML") and "IDPEP" in f
    ]

    for filename in filenames:
        out = filename.replace(".idXML", ".json")
        os.system(
            "python {} {} {}".format(_SCRIPT, fn, out)
        )


if __name__ == '__main__':
    main()
