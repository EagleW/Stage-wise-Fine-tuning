import glob
import json
import unidecode
import re
from tqdm import tqdm
from pathlib import Path
import networkx as nx

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


# https://github.com/commonsense/metanl/blob/master/metanl/token_utils.py
def untokenize(words):
    """
    Untokenizing a text undoes the tokenizing operation, restoring
    punctuation and spaces to the places that people expect them to be.
    Ideally, `untokenize(tokenize(text))` should be identical to `text`,
    except for line breaks.
    """
    text = ' '.join(words)
    step1 = text.replace("`` ", '"').replace(" ''", '"').replace('. . .',  '...')
    step2 = step1.replace(" ( ", " (").replace(" ) ", ") ")
    step3 = re.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", step2)
    step4 = re.sub(r' ([.,:;?!%]+)$', r"\1", step3)
    step5 = step4.replace(" '", "'").replace(" n't", "n't").replace(
         "can not", "cannot")
    step6 = step5.replace(" ` ", " '")
    return step6.strip()

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

Path('wiki_pos').mkdir(exist_ok=True)
pair_src = 'wiki_pos/train.source'
pair_tgt = 'wiki_pos/train.target'
wf_src = open(pair_src, 'w')
wf_tgt = open(pair_tgt, 'w')
for filename in sorted(glob.glob('total/data/*.json')):
    print(filename)
    with open(filename, 'r') as f:
        for line in tqdm(f):
            info = json.loads(line)
            triples = info['triples']
            covered = info['covered']
            total = info['total']
            type_ = info['type']
            sents = info['txt']

            covered_triples = []
            covered_entities = []
            covered_entities_dict = {}
            new_sent = []
            new_save = []

            src = ''
            cur_triples = []
            for h,r,t,f in triples:
                if f == True:
                    covered_triples.append((h,r,t,f))
                    covered_entities.append(t)
                    covered_entities_dict[t] = 0
                    h = get_point(h)
                    r = camel_case_split(get_relation(r))
                    t = get_point(t)
                    h = ' '.join(h)
                    r = ' '.join(r)
                    t = ' '.join(t)
                    cur_triples.append((h,r,t))
            new_sent.extend(sents[0])
            new_save.append(sents[0])
            for w in sents[0]:
                if w in covered_entities_dict:
                    covered_entities_dict[w] += 1
            for sent in sents[1:]:
                flag = False
                for w in sent:
                    if w in covered_entities_dict:
                        if covered_entities_dict[w] == 0:
                            flag = True
                        covered_entities_dict[w] += 1
                if flag:
                    new_sent.extend(sent)
                    new_save.append(sent)
            tgt = untokenize(new_sent)
            src = process_src(cur_triples)
            wf_src.write(json.dumps(src) + '\n')
            wf_tgt.write(tgt + '\n')
            wf_src.flush()
            wf_tgt.flush()
                        
wf_tgt.close()
wf_src.close()
