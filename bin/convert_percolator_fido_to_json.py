import sys
import json

from read import read_percolator_psms


def main():
    if len(sys.argv[1:]) != 2:
        error_msg = "python {} <in> <out>".format(
            sys.argv[0]
        )
        sys.exit(error_msg)

    in_file, out_file = sys.argv[1:]

    df = read_percolator_psms(in_file)

    data = [
        {
            "accession": row.ProteinId,
            "PEP": float(row.posterior_error_prob),
            "peptides": row.peptideIds,
            "protein_group_id": row.ProteinGroupId,
            "q_value": float(row["q-value"])
        } for _, row in df.iterrows()
    ]

    with open(out_file, "w") as out:
        json.dump(data, out, indent=4)


if __name__ == '__main__':
    main()
