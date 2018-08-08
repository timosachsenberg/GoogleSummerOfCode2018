

def annotate_correctness(data, protein_key="proteins"):
    for psm in data:
        psms = psm[protein_key]
        if not isinstance(psms, list):
            psms = [psms]

        # if any ID is a know protein, consider as correct
        # questionable
        psm["correct"] = any(
            "[INFLUENZA]" not in protein and
            "random" not in protein
            for protein in psms
        )
    return data


