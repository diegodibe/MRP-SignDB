import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import os
import json
from util import get_path


def split_in_units(array, chunks):
    return np.array_split(array, chunks)


def round_mean_values(array):
    mean_array = np.mean(array, 0)
    xy_round_mean_array = np.round(mean_array[:, 0:2]).astype(int)
    return xy_round_mean_array


def get_body_edges(start):
    return [(start, start + 15), (start, start + 16), (start, start + 1), (start + 1, start + 2),
            (start + 1, start + 5), (start + 1, start + 8), (start + 2, start + 3), (start + 3, start + 4),
            (start + 5, start + 6), (start + 6, start + 7), (start + 8, start + 9), (start + 8, start + 12),
            (start + 9, start + 10), (start + 10, start + 11), (start + 11, start + 22), (start + 11, start + 24),
            (start + 12, start + 13), (start + 13, start + 14), (start + 14, start + 19), (start + 14, start + 21),
            (start + 15, start + 17), (start + 16, start + 18), (start + 19, start + 20), (start + 19, start + 21),
            (start + 22, start + 23)]


def get_hand_edges(start):
    edges = []
    index = start
    for i in range(start + 1, start + 21):
        edges.append((index, i))
        if i % 4 == 0:
            index = start
        else:
            index = i
    return edges


def graph_processing(path):
    last_file = ''
    for segment in os.listdir(path + r'\coordinates_segments'):
        print(segment)
        if not last_file or segment.split('_')[1] != last_file[1]:
            last_file = segment.split('_')
            print(last_file)
            # segmentation values
            units = 10
            graphs_per_unit = 1

            # load data

            keypoints_dict = {'pose': split_in_units(
                                  np.load(path + r'\coordinates_segments\{v}_{s}_pose.npy'.format(v=last_file[0], s=last_file[1])), units),
                              'left_hand': split_in_units(
                                  np.load(path + r'\coordinates_segments\{v}_{s}_left_hand.npy'.format(v=last_file[0], s=last_file[1])), units),
                              'right_hand': split_in_units(
                                  np.load(path + r'\coordinates_segments\{v}_{s}_right_hand.npy'.format(v=last_file[0], s=last_file[1])), units)}


            pose = []
            right = []
            left = []
            for unit in range(units):
                right_units = split_in_units(keypoints_dict['pose'][unit], graphs_per_unit)
                left_units = split_in_units(keypoints_dict['right_hand'][unit], graphs_per_unit)
                pose_units = split_in_units(keypoints_dict['left_hand'][unit], graphs_per_unit)
                for chunk in range(graphs_per_unit):
                    pose.append(round_mean_values(pose_units[chunk]))
                    right.append(round_mean_values(right_units[chunk]))
                    left.append(round_mean_values(left_units[chunk]))

            coordinates = []
            for unit in range(units * graphs_per_unit):
                # stack all matrixes together
                coordinates.append(np.vstack((pose[unit], left[unit], right[unit])))

            #add feature to store the order
            multiplier = 0
            graph = nx.Graph()
            for entry in coordinates:
                n_nodes = multiplier * len(coordinates[0])
                graph.add_nodes_from((c + n_nodes, {'feature': {'x': val[0], 'y': val[1]}}) for c, val in enumerate(entry))
                #print('iter ', multiplier, '\n', graph.nodes)
                graph.add_edges_from(get_body_edges(n_nodes))
                graph.add_edges_from(get_hand_edges(25 + n_nodes))
                graph.add_edges_from(get_hand_edges(46 + n_nodes))
                graph.add_edge(4 + n_nodes, 25 + n_nodes)
                graph.add_edge(7 + n_nodes, 46 + n_nodes)
                if multiplier > 0:
                    graph.add_edge(n_nodes - len(coordinates[0]),  n_nodes)
                multiplier += 1
                #print(nx.is_connected(graph))

            # print(graph.nodes.data())
            # print(graph.edges)
            # print(graph.adj)
            # print(nx.get_node_attributes(graph, "feature"))
            # nx.draw(graph, pos=nx.spring_layout(graph), node_size=30)
            # plt.show()

            video_ns = [s for s in last_file[0] if s.isdigit()]
            video_n = ''
            for value in video_ns:
                video_n += value
            out = '_{s}.json'.format(s=last_file[1])
            with open(get_path(video_n, r'\{p}\graphs'.format(p=path), 'graph{}' + out), 'w') as f:
                json.dump(str(nx.to_dict_of_dicts(graph)), f)
            out = '_{s}_attributes.json'.format(s=last_file[1])
            with open(get_path(video_n, r'\{p}\graph_attributes'.format(p=path), 'graph{}' + out), 'w') as f:
                json.dump(str(graph.nodes.data()), f)
