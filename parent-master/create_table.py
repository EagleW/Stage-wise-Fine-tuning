""" table: List of either (attribute, value) pairs or (head, relation, tail)
      triples. Each member of the pair / triple is assumed to already be
      tokenized into a list of strings.
tables: An iterator over the tables. Each table is a list of tuples, with
            tuples being either (attribute, value) or (head, relation, tail).
            The members of the tuples are assumed to be themselves tokenized
            lists of strings. E.g.
                `[(["name"], ["michael", "dahlquist"]),
                  (["birth", "date"], ["december", "22", "1965"])]`
"""
import json
from tqdm import tqdm
wf = open('webnlg.jl', 'w')

with open('pos/test.source', 'r') as f:
    for line in tqdm(f):
        data = json.loads(line)
        tmp = []
        for triples in data:
            tt = []
            for e in triples[:-1]:
                tt.append(e[3:].split())
            tmp.append(tt)
        wf.write(json.dumps(tmp)+'\n')

wf.close()