from itertools import combinations

import networkx as nx

from util import Util


class Graph:
    def __init__(self):
        self.graph = nx.Graph()

    def add_tweet(self, tweet, k):
        new_edges = Graph.get_edges(tweet)
        self.add_edges(new_edges, k)

    def add_edges(self, edges, k):
        for edge in edges:
            if edge not in self.graph.edges():
                self.graph.add_edge(edge[0], edge[1])
                self.graph[edge[0]][edge[1]]['weight'] = 0
            self.update_weight(self.graph[edge[0]][edge[1]])
            self.graph[edge[0]][edge[1]]['time_interval'] = k

    @staticmethod
    def get_edges(tweet):
        tokens = Util.tokenize(tweet.text)
        edges = list(combinations(tokens, 2))
        return edges

    def update_weight(self, edge):
        edge['weight'] += 1

    def prune_edges(self, curr_age):
        with open("logs/pruning-" + str(curr_age) + '.txt', 'w') as outputFile:
            allEdges = list(self.graph.edges())
            for edge in allEdges:
                if self.graph[edge[0]][edge[1]]['weight'] == 1 and self.graph[
                    edge[0]][
                    edge[1]][
                    'time_interval'] < curr_age:
                    outputFile.write("pruning edge: " + ','.join(edge) + '\n')
                    self.graph.remove_edge(*edge)
            self.graph.remove_nodes_from(list(nx.isolates(self.graph)))

    def score(self, tweet):
        edges = Graph.get_edges(tweet)
        score = 0
        for edge in edges:
            if edge in self.graph.edges():
                # outputFile.write(','.join(edge) + " : " + str(
                #     self.graph[edge[0]][edge[1]]['weight']) + '\n')
                score += self.graph[edge[0]][edge[1]]['weight']
        return score

    def number_of_nodes(self):
        return self.graph.number_of_nodes()