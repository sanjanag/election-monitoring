import networkx as nx
import math
# from util import Util


class Graph:
    def __init__(self):
        self.graph = nx.Graph()

    def add_tweet(self, tweet, k):
        if len(tweet.edges) == 0:
            tweet.set_edges()
        new_edges = tweet.edges
        self.add_edges(new_edges, k)

    def add_edges(self, edges, k):
        for edge in edges:
            if edge not in self.graph.edges():
                self.graph.add_edge(edge[0], edge[1])
                self.graph[edge[0]][edge[1]]['weight'] = {}
            self.update_weight(self.graph[edge[0]][edge[1]],k)
            self.graph[edge[0]][edge[1]]['time_interval'] = k

    def update_weight(self, edge, k):
        if not k in edge['weight'].keys():
            edge['weight'][k] = 0
        edge['weight'][k] += 1

    def prune_edges(self, curr_age):
        with open("logs/pruning-" + str(curr_age) + '.txt', 'w') as outputFile:
            allEdges = list(self.graph.edges())
            for edge in allEdges:
                # self.get_decay_value(edge, curr_age) # compute decay for each edge
                if sum(self.graph[edge[0]][edge[1]]['weight'].values()) == 1 and self.graph[
                    edge[0]][
                    edge[1]][
                    'time_interval'] == curr_age - 1:
                    outputFile.write("pruning edge: " + ','.join(edge) + '\n')
                    self.graph.remove_edge(*edge)
            self.graph.remove_nodes_from(list(nx.isolates(self.graph)))


    def get_decay_value(self, edge, curr_age):
        curr_edge = self.graph[edge[0]][edge[1]]
        decay_value = [self.compute_individual_decay_value(key, value, curr_age) for key, value in curr_edge['weight'].items()]
        return sum(decay_value)

    def compute_individual_decay_value(self, key, value, curr_age):
        lambd = 0.1
        return value * math.exp(-1 * lambd * (curr_age - key))

    # def score(self, tweet):
    #     edges = Graph.get_edges(tweet)
    #     score = 0
    #     for edge in edges:
    #         if edge in self.graph.edges():
    #             # outputFile.write(','.join(edge) + " : " + str(
    #             #     self.graph[edge[0]][edge[1]]['weight']) + '\n')
    #             score += self.graph[edge[0]][edge[1]]['weight']
    #     return score

    def number_of_nodes(self):
        return self.graph.number_of_nodes()