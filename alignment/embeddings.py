import json
import networkx as nx
from karateclub import Graph2Vec
import ast
import numpy as np
import matplotlib.pyplot as plt
import os
import tensorflow_hub as hub


def embeddings(path):
    train_graph = False
    if train_graph:
        train_graph2vec(path)
    calculate_text = True
    if calculate_text:
        embeddings_usem(path)

    print('Embeddings created, use Vecmap to align them.')



def train_graph2vec(path):
    model = Graph2Vec(dimensions=516, attributed=True)
    graphs = []
    for file in os.listdir(path + r'\graphs'):
        with open(r'{p}\graphs\{f}'.format(p=path, f=file), 'r') as js_file_graph:
            graphs.append(nx.from_dict_of_dicts(ast.literal_eval(json.load(js_file_graph))))

    for count, file in enumerate(os.listdir(path + r'\graph_attributes')):
        with open(r'{p}\graph_attributes\{f}'.format(p=path, f=file), 'r') as js_file_attr:
            print(file)
            attrs = ast.literal_eval(json.load(js_file_attr))
            attributes_dict = {}
            for entry in attrs:
                attributes_dict[entry[0]] = entry[1]
            nx.set_node_attributes(graphs[count], attributes_dict)

    # for i in range(1):
        # print(graphs[i].nodes.data())
        # print(graphs[i].edges)
        # print(graphs[i].adj)
        # print(nx.get_node_attributes(graphs[i], 'feature'))
        # nx.draw(graphs[i], pos=nx.spring_layout(graphs[i]), node_size=30)
        # plt.show()

    model.fit(graphs)
    np.save(path + r'\graph_embeddings', model.get_embedding())


def embeddings_usem(path):
    model = hub.load('https://tfhub.dev/google/universal-sentence-encoder-multilingual-large/3')
    text = []
    for segment in os.listdir(path + r'\subtitle_segments'):
        print(segment)
        with open(r'{p}\subtitle_segments\{s}'.format(p=path, s=segment), 'r') as subtitle:
            text.append(model(subtitle.read()))

    np.save(path + r'\text_embeddings', text)



