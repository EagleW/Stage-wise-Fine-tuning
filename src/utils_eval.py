import re
import os
from sacrebleu import corpus_bleu

def eval_bleu(folder_data, pred_file, dataset):

    dir_path = os.path.dirname(os.path.realpath(__file__))

    print(folder_data, dataset)

    cmd_string = "perl " + dir_path + "/multi-bleu.perl -lc " + folder_data + "/" + dataset + ".target_eval " \
                  + folder_data + "/" + dataset + ".target2_eval " + folder_data + "/" + dataset + ".target3_eval < " \
                  + pred_file + " > " + pred_file.replace("txt", "bleu")

    os.system(cmd_string)

    try:
        bleu_info = open(pred_file.replace("txt", "bleu"), 'r').readlines()[0].strip()
    except:
        bleu_info = -1

    return bleu_info

def calculate_sacrebleu(output_lns, refs_lns, **kwargs) -> dict:
    """Uses sacrebleu's corpus_bleu implementation."""
    return {"sacrebleu": round(corpus_bleu(output_lns, [refs_lns], **kwargs).score, 4)}