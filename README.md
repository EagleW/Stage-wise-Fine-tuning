# Stage-wise-Fine-tuning-for-Graph-to-Text-Generation

[![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/stage-wise-fine-tuning-for-graph-to-text/data-to-text-generation-on-webnlg-full-1)](https://paperswithcode.com/sota/data-to-text-generation-on-webnlg-full-1?p=stage-wise-fine-tuning-for-graph-to-text)

[Stage-wise Fine-tuning for Graph-to-Text Generation](https://aclanthology.org/2021.acl-srw.2.pdf)

Accepted by the Joint Conference of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing 2021 Student Research Workshop (ACL-IJCNLP 2021 SRW)

Table of Contents
=================
  * [Overview](#overview)
  * [Requirements](#requirements)
  * [Quickstart](#quickstart)
  * [Evaluation](#evaluation)
  * [Citation](#citation)

## Overview
<p align="center">
  <img src="https://eaglew.github.io/images/stage.png?raw=true" alt="Photo" style="width: 100%;"/>
</p>

This project is based on the framework [HuggingFace Transformers](https://huggingface.co/transformers/). 

## Requirements

### Environment:

- Python 3.8.5
- Ubuntu 18.04/20.04 **CAUTION!! The model might not run properly on windows because [windows uses backslashes on the path while Linux/OS X uses forward slashes](https://www.howtogeek.com/181774/why-windows-uses-backslashes-and-everything-else-uses-forward-slashes/)**

### Setup:
```
# Create python environment (optional)
conda create -n stage_fine python=3.8.5

# Install pytorch with cuda (optional)
conda install pytorch==1.7.1  cudatoolkit=11.0 -c pytorch

# Install python dependencies
pip install -r requirements.txt

```

### Data
#### [WebNLG 2017](https://gitlab.com/shimorina/webnlg-dataset/-/tree/master/webnlg_challenge_2017)

For this paper, we test our model on the original version of [English WebNLG 2017](https://gitlab.com/shimorina/webnlg-dataset/-/tree/master/webnlg_challenge_2017). The preprocessed WebNLG data with position information for this model can be downloaded [here](https://drive.google.com/file/d/1PKXKuh9Q2b2bEOPX2r4vlC9gnrlo_Hfk/view?usp=sharing). 

#### [Wikipedia Pre-train Pairs](https://drive.google.com/file/d/18N8xgAftgoV7D03G643EDp1BfQXzPOTH/view?usp=sharing)

This repository contains data used for the Wikipedia fine-tuning stage for paper Stage-wise Fine-tuning for Graph-to-Text Generation. The documentation for this dataset is [here](https://github.com/EagleW/Stage-wise-Fine-tuning/blob/main/Wikipedia%20Pre-train%20Pairs/README.md). The preprocessed Wikipedia Pre-train Pairs with position information for this model can be downloaded [here](https://drive.google.com/file/d/1qA6A2YoW9bgC5WD3YpWEiPagsjclkxVA/view?usp=sharing).

## Quickstart

### Preprocessing:

#### Download Preprocessed Data
You can download preprocessed [WebNLG with Position](https://drive.google.com/file/d/1PKXKuh9Q2b2bEOPX2r4vlC9gnrlo_Hfk/view?usp=sharing) and [Wikipedia Pre-train Pairs with Position](https://drive.google.com/file/d/18N8xgAftgoV7D03G643EDp1BfQXzPOTH/view?usp=sharing). Unzip them in the `src` folder.

#### Preprocess by Yourself
If you prefer to preprocess by yourself, download [WebNLG 2017](https://gitlab.com/shimorina/webnlg-dataset/-/tree/master/webnlg_challenge_2017) and [Wikipedia Pre-train Pairs](https://drive.google.com/file/d/18N8xgAftgoV7D03G643EDp1BfQXzPOTH/view?usp=sharing). Put them under the `preprocess` folder. Unzip `total.zip` which contains [Wikipedia Pre-train Pairs](https://drive.google.com/file/d/18N8xgAftgoV7D03G643EDp1BfQXzPOTH/view?usp=sharing).

To get [WebNLG with Position](https://drive.google.com/file/d/1PKXKuh9Q2b2bEOPX2r4vlC9gnrlo_Hfk/view?usp=sharing). Run `webnlg_tree.py` under this folder:
```
python webnlg_tree.py
```

This will create `pos`. 
To get [Wikipedia Pre-train Pairs with Position](https://drive.google.com/file/d/18N8xgAftgoV7D03G643EDp1BfQXzPOTH/view?usp=sharing). Run `webnlg_tree.py` under this folder:
```
python get_new_pretrained_pos.py
```
Copy `val.*` and `test.*` from `pos` folder to `wiki_pos` folder. Move `pos` folder and  `wiki_pos` folder under the `src` folder.

### Finetuning

#### Finetuning with 2-stage pre-training
You can finetune your model by running `finetune_*_all.sh` in the `src` folder. For example, if you want to test t5_large, you can run
```
./finetune_t5_large_all.sh 
```

#### Finetuning without Wikipedia pre-training
Similarly, you can finetune your own model by running `finetune_*_alone.sh` in the `src` folder. For example, if you want to test t5_large, you can run
```
./finetune_t5_large_alone.sh 
```

You can modify hyperparameters such as batch size in those bash files. The result will be under `*_results/test_generations.txt`. 

### Decoding with Our Model
Our model can be downloaded [here](http://159.89.180.81/demo/stage/final_model_results.tar.xz). After you extract the file under the `src` folder, you can run 
```
./test_t5.sh 
```
to get the result.

The result will be under `t5_large_pos_test_results/test_generations.txt`.


## Evaluation
### Official Evaluation

The official evaluation script is based on [WebNLG official transcript](https://gitlab.com/webnlg/webnlg-automatic-evaluation) and [DART](https://github.com/Yale-LILY/dart/tree/master/evaluation).

#### Usage: 
Change `OUTPUT_FILE` in `run_eval_on_webnlg.sh` and run the following:
```
./run_eval_on_webnlg.sh
```

### PARENT-SCORE
For details about PARENT score, please check [PARENT folder](https://github.com/EagleW/Stage-wise-Fine-tuning/tree/main/parent-master).



### BERT-SCORE

Install [Bert-Score](https://github.com/Tiiiger/bert_score) from pip by
```
pip install bert-score

```

Test your file
```
bert-score -r evaluation/references/reference0 evaluation/references/reference1 evaluation/references/reference2 -c evaluation/example/pos+wiki.txt --lang en 
```

If you have some questions about BERT-Score, please check this [issue](https://github.com/Tiiiger/bert_score/issues/85).

#### Trained Model and Result

Result from T5-large + Wiki + Position is [here](https://raw.githubusercontent.com/EagleW/Stage-wise-Fine-tuning/main/evaluation/example/pos%2Bwiki.txt).

<table style='font-size:80%'>
  <tr>
    <th>Model</th>
    <th>BLEU ALL</th>
    <th>METEOR ALL</th>
    <th>TER ALL</th>
    <th>BERTScore P</th>
    <th>BERTScore R</th>
    <th>BERTScore F1</th>
  </tr>
  <tr>
    <td> <a href="http://159.89.180.81/demo/stage/final_model_results.tar.xz">T5-large + Wiki + Position   </a></td>
    <td><b>60.56</b></td>
    <td><b>0.44</b></td>
    <td><b>0.36</b></td>
    <td><b>96.36</b></td>
    <td><b>96.13</b></td>
    <td><b>96.21</b></td>
  </tr>
</table>

## Citation
```
@inproceedings{wang-etal-2021-stage,
    title = "Stage-wise Fine-tuning for Graph-to-Text Generation",
    author = "Wang, Qingyun  and
      Yavuz, Semih  and
      Lin, Xi Victoria  and
      Ji, Heng  and
      Rajani, Nazneen",
    booktitle = "Proceedings of the ACL-IJCNLP 2021 Student Research Workshop",
    month = aug,
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.acl-srw.2",
    pages = "16--22"
}
```
