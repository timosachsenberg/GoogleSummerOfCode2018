from collections import defaultdict
import numpy as np

_DEFAULT_PEP_THRESH_LIST = [
    0,
    0.000001, 0.000005,
    0.00001, 0.00005,
    0.0001, 0.0005,
    0.001, 0.005,
    0.01, 0.05,
    0.1
]

_DEFAULT_PEP_THRESH_LIST_EXT = (
    _DEFAULT_PEP_THRESH_LIST +
    list(np.arange(0.15, 1.05, 0.05))
)

_TRANSLATE_CONFUSION = {
    (True, True): "TP",
    (True, False): "FP",
    (False, False): "TN",
    (False, True): "FN"
}


def n_psms(data):
    return len(data)


def unique_peptides(data, protein_key="peptide"):
    return list(set(list(
        map(lambda item: item[protein_key], data)
    )))


def n_unique_peptides(data, protein_key="peptide"):
    return len(unique_peptides(data, protein_key=protein_key))


def correct_psms(data, thresh=None):
    psms = []
    for psm in data:
        criterion = psm["correct"]
        if thresh is not None:
            criterion = criterion and psm["PEP"] < thresh
        if criterion:
            psms.append(psm)
    return psms


def incorrect_psms(data):
    return [
        psm for psm in data
        if not psm["correct"]
    ]


def n_correct_identifications(data, thresh_list=_DEFAULT_PEP_THRESH_LIST):
    return thresh_list, [
        len(correct_psms(data, thresh))
        for thresh in thresh_list
    ]


def n_unique_correct_identifications(data, protein_key="peptide",
                                     thresh_list=_DEFAULT_PEP_THRESH_LIST):
    return thresh_list, [
        len(unique_peptides(correct_psms(data, thresh), protein_key=protein_key))
        for thresh in thresh_list
    ]


def reduce_to_list(data, name="PEP"):
    return list(
        map(lambda item: item[name], data)
    )


def confusion_matrix(data, thresh):
    matrix = defaultdict(int)
    for psm in data:
        matrix[
            _TRANSLATE_CONFUSION[
                (psm["PEP"] < thresh, psm["correct"])
            ]
        ] += 1
    return matrix


def precision(matrix):
    return (matrix["TP"] + 1e-60) / (matrix["TP"] + matrix["FP"] + 1e-60)


def recall(matrix):
    return (matrix["TP"] + 1e-60) / (matrix["TP"] + matrix["FN"] + 1e-60)


def specificity(matrix):
    return (matrix["TN"] + 1e-60) / (matrix["TN"] + matrix["FP"] + 1e-60)


def fpr(matrix):
    return 1 - specificity(matrix)


def roc_curve(data, thresh_list=_DEFAULT_PEP_THRESH_LIST_EXT):
    tp_rates, fp_rates = [], []
    for thresh in thresh_list:
        matrix = confusion_matrix(data, thresh)
        tp_rates.append(recall(matrix))
        fp_rates.append(fpr(matrix))
    return thresh_list, tp_rates, fp_rates


def precision_recall_curve(data, thresh_list=_DEFAULT_PEP_THRESH_LIST_EXT):
    prec_vals, recall_vals = [], []
    for thresh in thresh_list:
        matrix = confusion_matrix(data, thresh)
        prec_vals.append(precision(matrix))
        recall_vals.append(recall(matrix))
    return thresh_list, prec_vals, recall_vals


def actual_vs_computed_pep(data, window_size=100):
    sorted_data = sorted(
        data, key=lambda item: item["PEP"]
    )

    peps = reduce_to_list(sorted_data)
    is_correct = reduce_to_list(sorted_data, name="correct")
    is_incorrect = [not x for x in is_correct]

    actual, computed = [], []
    for i in range(len(peps)):
        end = i + window_size
        if end <= len(peps):
            actual.append(sum(is_incorrect[i: end]) / window_size)
            computed.append(sum(peps[i: end]) / window_size)

    return actual, computed
