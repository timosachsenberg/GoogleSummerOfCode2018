from __future__ import print_function

import sys
import json
from xml.dom import minidom

_MAP_NAME = {
    "MS:1001491": "q-value",
    "MS:1001492": "SVM score",
    "MS:1001493": "PEP"
}


def main():
    if len(sys.argv[1:]) != 2:
        error_msg = "python {} <in> <out>".format(
            sys.argv[0]
        )
        sys.exit(error_msg)

    in_file, out_file = sys.argv[1:]

    # print("Parsing file...", end=" ", file=sys.stderr, flush=True)
    doc = minidom.parse(in_file)
    # print("done", file=sys.stderr, flush=True)

    protein_hits = doc.getElementsByTagName("ProteinHit")

    protein_id_to_acc = {
        hit.attributes["id"].value:
            hit.attributes["accession"].value
        for hit in protein_hits
    }

    peptide_ids = doc.getElementsByTagName("PeptideIdentification")
    peptide_hits = doc.getElementsByTagName("PeptideHit")

    data = []
    for pep_id, hit in zip(peptide_ids, peptide_hits):
        protein_refs = hit.attributes["protein_refs"].value.split()
        protein_accs = list(map(
            lambda ref: str(protein_id_to_acc[ref]),
            protein_refs
        ))

        params = hit.getElementsByTagName("UserParam")
        params_dict = {
            _MAP_NAME[p.attributes["name"].value]:
                float(p.attributes["value"].value)
            for p in params
            if p.attributes["name"].value in _MAP_NAME.keys()
        }

        params_dict["peptide"] = hit.attributes["sequence"].value
        params_dict["proteins"] = protein_accs

        data.append(params_dict)

    with open(out_file, "w") as out:
        json.dump(data, out, indent=4)


if __name__ == '__main__':
    main()
