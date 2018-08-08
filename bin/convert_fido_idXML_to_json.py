import sys
from xml.dom.minidom import parseString
import json


def main():
    if len(sys.argv[1:]) != 2:
        error_msg = "usage: python {} <in.idXML> <out.idXML>"
        sys.exit(error_msg.format(sys.argv[0]))

    in_file, out_file = sys.argv[1:]

    data = []
    with open(in_file) as f:
        for line in f:
            if "<ProteinHit id=" in line:
                doc = parseString(line + "</ProteinHit>")
                protein_hit = doc.getElementsByTagName("ProteinHit")[0]
                data.append(
                    {
                        "id": protein_hit.attributes["id"].value,
                        "accession": protein_hit.attributes["accession"].value,
                        "posterior_probability": float(protein_hit.attributes["score"].value),
                        "PEP": 1 - float(protein_hit.attributes["score"].value)
                    }
                )

    with open(out_file, "w") as out:
        json.dump(data, out, indent=4)


if __name__ == '__main__':
    main()
