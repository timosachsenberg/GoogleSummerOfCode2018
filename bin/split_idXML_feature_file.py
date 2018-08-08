import os

_DIR = "/Users/sophiamersmann/Dropbox/student/imperial_college_london/GSoC/datasets/iPRG2016/search_engine_results"

_FIRST = [
    'name="REP:siblingSearchesTop"',
    'name="REP:siblingModificationsTop"',
    'name="REP:siblingIonsTop"'
]

_SECOND = [
    'name="REP:siblingSearches"',
    'name="REP:siblingModifications"',
    'name="REP:siblingIons"'
]


def main():
    filenames = [
        os.path.join(_DIR, fn)
        for fn in os.listdir(_DIR)
        if "features.idXML" in fn
    ]

    for fn in filenames:
        out_v1 = fn.replace(".idXML", "_v1.idXML")
        out_v2 = fn.replace(".idXML", "_v2.idXML")
        with open(fn) as f, open(out_v1, "w") as o1, open(out_v2, "w") as o2:
            for line in f:
                if 'name="extra_features"' in line:
                    line1 = line
                    line1 = line1.replace(",REP:siblingSearchesTop", "")
                    line1 = line1.replace(",REP:siblingModificationsTop", "")
                    line1 = line1.replace(",REP:siblingIonsTop", "")
                    o1.write(line1)

                    line2 = line
                    line2 = line2.replace("REP:siblingSearches,", "")
                    line2 = line2.replace("REP:siblingModifications,", "")
                    line2 = line2.replace("REP:siblingIons,", "")
                    o2.write(line2)
                else:
                    if not any([item in line for item in _FIRST]):
                        o1.write(line)
                    if not any([item in line for item in _SECOND]):
                        o2.write(line)


if __name__ == '__main__':
    main()
