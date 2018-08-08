import os
import json
from xml.dom.minidom import parseString

_DIR = "/Users/sophiamersmann/Dropbox/student/imperial_college_london/GSoC/datasets/iPRG2016/search_engine_results"


def main():
    filenames = [
        os.path.join(_DIR, fn)
        for fn in os.listdir(_DIR)
        if "features.idXML" in fn
    ]

    for fn in filenames:
        data, item = [], {}
        with open(fn) as f:
            for line in f:
                if "UserParam" in line and 'name="REP' in line:
                    param = parseString(line).getElementsByTagName("UserParam")[0]
                    name = param.attributes["name"].value
                    value = float(param.attributes["value"].value)
                    item[name] = value
                if len(item) == 8:
                    data.append(item)
                    item = {}

        out = fn.replace(".idXML", ".json")
        with open(out, "w") as o:
            json.dump(data, o, indent=4)


if __name__ == '__main__':
    main()
