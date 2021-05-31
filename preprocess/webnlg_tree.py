from benchmark_reader import Benchmark, select_files
import os, json, re, unidecode
from collections import Counter
from tqdm import tqdm
from operator import itemgetter
import networkx as nx
from transformers import BartTokenizer


def camel_case_split(identifier):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    d = [m.group(0) for m in matches]
    new_d = []
    for token in d:
        token = token.replace('(', '')
        token_split = token.split('_')
        for t in token_split:
            new_d.append(t)
    return new_d

def get_point(n):
    n = n.strip()
    n = n.replace('(', '')
    n = n.replace('\"', '')
    n = n.replace(')', '')
    n = n.replace(',', ' ')
    n = n.replace('_', ' ')
    n = unidecode.unidecode(n)

    return n.split()

def get_relation(n):
    n = n.replace('(', '')
    n = n.replace(')', '')
    n = n.strip()
    n = n.split()
    n = "_".join(n)
    return n



def get_tree(triples):
    G = nx.DiGraph()
    triple_dict = {}
    for h, _, t in triples:
        G.add_edge(h,t)
    min_d = 100000
    sub_graph = G
    root = ''
    for n, d in sub_graph.in_degree():
        if min_d > d:
            min_d = d
            root = n
    head = root
    level = 0
    for h, t in nx.bfs_edges(sub_graph, root):
        if head == h:
            triple_dict[h+t] = level
        else:
            level += 1
            head = h
            triple_dict[h+t] = level
    for n, level in nx.single_source_shortest_path_length(sub_graph, root).items():
        triple_dict[n+n] = level
    flag = True
    while(flag):
        flag = False
        G1 = nx.DiGraph()
        for h, _, t in triples:
            if h+t not in triple_dict:
                flag = True
                G1.add_edge(h,t)
        if not flag:
            break
        min_d = 100000
        sub_graph = G1
        root = ''
        for n, d in sub_graph.in_degree():
            if min_d > d:
                min_d = d
                root = n
        head = root
        level = 0
        for h, t in nx.bfs_edges(sub_graph, root):
            if head == h:
                triple_dict[h+t] = level
            else:
                level += 1
                head = h
                triple_dict[h+t] = level
        for n, level in nx.single_source_shortest_path_length(sub_graph, root).items():
            triple_dict[n+n] = level
    return triple_dict


def process_src(triples):
    filtered_triples = []
    triple_dict = get_tree(triples)
    for h, r, t in triples[:-1]:
        token = h + t
        filtered_triples.append(('S| ' + h + ' ', ' P| ' + r + ' ', 'O| ' + t + ' ', triple_dict[token] + 3))
    h, r, t = triples[-1]
    token = h + t
    filtered_triples.append(('S| ' + h + ' ', ' P| ' + r + ' ', 'O| ' + t, triple_dict[token] + 3))
    return filtered_triples

def process_tgt_test(tgts):
    texts = []
    for text in tgts:
        new_txt = text.lex.strip()
        texts.append(new_txt)
    return  texts

def convert_dataset(pair_src, pair_tgt, b):
    wf_src = open(pair_src, 'w')
    wf_tgt = open(pair_tgt, 'w')
    max_role = 4
    max_tree = 1
    for entry in tqdm(b.entries):

        triples = entry.list_triples()
        if len(triples) == 0:
            continue
        cur_triples = []
        for triple in triples:
            h, r, t = triple.split(' | ')
            h = get_point(h)
            r = camel_case_split(get_relation(r))
            t = get_point(t)
            h = ' '.join(h)
            r = ' '.join(r)
            t = ' '.join(t)
            cur_triples.append((h,r,t))
        tgt = process_tgt_test(entry.lexs)
        src = process_src(cur_triples)
        if len(tgt) == 0:
            continue
        for tg in tgt:
            wf_src.write(json.dumps(src) + '\n')
            wf_tgt.write(tg + '\n')
    wf_tgt.close()
    wf_src.close()

def convert_dataset_test(pair_src, pair_tgt, b):
    wf_src = open(pair_src, 'w')
    wf_tgt = open(pair_tgt, 'w')
    wf_tgt1 = open(pair_tgt + '_eval', 'w')
    wf_tgt2 = open(pair_tgt + '2_eval', 'w')
    wf_tgt3 = open(pair_tgt + '3_eval', 'w')
    max_role = 4
    max_segment = 1
    max_order = 1
    max_tree = 1
    for entry in tqdm(b.entries):

        triples = entry.list_triples()
        if len(triples) == 0:
            continue
        cur_triples = []
        for triple in triples:
            h, r, t = triple.split(' | ')
            h = get_point(h)
            r = camel_case_split(get_relation(r))
            t = get_point(t)
            h = ' '.join(h)
            r = ' '.join(r)
            t = ' '.join(t)
            cur_triples.append((h,r,t))
        src = process_src(cur_triples)
        tgt = process_tgt_test(entry.lexs)
        if len(tgt) == 0:
            continue
        src = process_src(cur_triples)
        wf_src.write(json.dumps(src) + '\n')
        wf_tgt.write(tgt[0] + '\n')
        
        wf_tgt1.write(tgt[0] + '\n')
        if len(tgt) > 1:
            wf_tgt2.write(tgt[1] + '\n')
            if len(tgt) > 2:
                wf_tgt3.write(tgt[2] + '\n')
            else:
                wf_tgt3.write('\n')
        else:
            wf_tgt2.write('\n')
            wf_tgt3.write('\n')
    wf_tgt.close()
    wf_src.close()
    wf_tgt1.close()
    wf_tgt2.close()
    wf_tgt3.close()



outdir = 'data/pos'
b = Benchmark()
files = select_files('webnlg_challenge_2017/train')
b.fill_benchmark(files)

pair_train_src = os.path.join(outdir, "train.source")
pair_train_tgt = os.path.join(outdir, "train.target")
convert_dataset(pair_train_src, pair_train_tgt, b)

b = Benchmark()
files = select_files('webnlg_challenge_2017/dev')
b.fill_benchmark(files)

pair_valid_src = os.path.join(outdir, "val.source")
pair_valid_tgt = os.path.join(outdir, "val.target")
convert_dataset_test(pair_valid_src, pair_valid_tgt, b)


b = Benchmark()
files = [('webnlg_challenge_2017/test', 'testdata_with_lex.xml')]
b.fill_benchmark(files)

pair_valid_src = os.path.join(outdir, "test.source")
pair_valid_tgt = os.path.join(outdir, "test.target")
convert_dataset_test(pair_valid_src, pair_valid_tgt, b)