# PARENT

Code for [Handling Divergent Reference Texts when Evaluating Table-to-Text Generation](https://arxiv.org/abs/1906.01081).

This largely follows [the code given by Clément Rebuffel](https://github.com/KaijuML/parent), all credit to him.

## Computing the PARENT score in command line:

You need to run `create_tablt.py` to create WebNLG table.

After that, simply use:

```python parent.py --predictions $PREDICTION_PATH --references $REFERENCES_PATH --tables $TABLES_PATH --avg_results```

You can modify the `test.sh` file for simiplicity.

With the example files provided in `data`, and using `--n_jobs 32`, this should take around 8 secondes and print:

```
PARENT-precision: - - - 0.797
PARENT-recall:  - - - - 0.45
PARENT-fscore:  - - - - 0.553
```

In comparison, running the original script takes around 1m40s and returns `Precision = 0.7975 Recall = 0.4503 F-score = 0.5529`

### File format

Note that predictions/references should be one sentence per line (whitespace is used to tokenize sentences).

Tables should be in a json-line file, with one table per line in json format (```json.loads(line)``` will be called).


## Computing the PARENT score in a notebook:

You can also use the code anywhere, simply follow this example:

```python
from parent import parent
import json


# open all files
path_to_tables = 'data/wb_test_tables.jl'
path_to_references = 'data/wb_test_output.txt'
path_to_predictions = 'data/wb_predictions.txt'

with open(path_to_tables, mode="r", encoding='utf8') as f:
    tables = [json.loads(line) for line in f if line.strip()]

with open(path_to_references, mode="r", encoding='utf8') as f:
    references = [line.strip().split() for line in f if line.strip()]

with open(path_to_predictions, mode="r", encoding='utf8') as f:
    predictions = [line.strip().split() for line in f if line.strip()]
        
precisions, recalls, f_scores = parent(
    predictions,
    references,
    tables,
    avg_results=True,
    n_jobs=32,
    use_tqdm='notebook'
)
```
