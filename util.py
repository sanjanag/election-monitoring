import re
from collections import OrderedDict

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from nltk.corpus import stopwords

punctuations = "!\"(),-./:;<=>?[\\]^_`{|}~'"
refinedPunctuations = ",|\.|;"
stopWords = set(stopwords.words('english'))


class Util:
    # @staticmethod
    # def score_tweet(outputFile, edges, G):
    #     score = 0
    #     for edge in edges:
    #         if edge in G.edges():
    #             outputFile.write(','.join(edge) + " : " + str(
    #                 G[edge[0]][edge[1]]['weight']) + '\n')
    #             score += sum(G[edge[0]][edge[1]]['weight'].values())
    #     return score

    @staticmethod
    def sanitize(tokens):
        newTokens = []
        for token in tokens:
            token = token.strip(punctuations)  # remove punctuations
            splitTokens = re.split(refinedPunctuations,
                                   token)  # because people dont put space
            # after some imp. punctuations like comma and fullstop
            for splitToken in splitTokens:
                if (Util.is_valid(splitToken)):  # need to check validity
                    # again
                    # after
                    # stripping and removing symbols
                    newTokens.append(splitToken)
        return newTokens

    @staticmethod
    def tokenize(tweet):
        tweet = re.sub(r'[^\x00-\x7f]', r'', tweet)  # remove non-ascii chars
        tokens = tweet.split()  # split about empty spaces
        tokens = [x.lower() for x in tokens if
                  Util.is_valid(x)]  # remove URLs, @ mentions etc.
        tokens = Util.sanitize(
            tokens)  # remove random characters and punctions, #hash should
        # not be removed
        tokens = [x for x in tokens if not x in stopWords]  # remove stop words
        tokens = list(OrderedDict.fromkeys(
            tokens))  # remove duplicates, while maintaining order
        # print(tweet)
        # print(tokens)
        return tokens

    @staticmethod
    def is_valid(token):
        if len(token) <= 1 or token.startswith('@') or token.startswith(
                'http'):  # remove urls and @ mentions
            return False
        return True

    @staticmethod
    def get_windows(tokens, window_size):
        windows = [tokens[(i - window_size): (i + window_size + 1)] for i in
                   range(window_size, len(tokens) - window_size)]
        return windows

    @staticmethod
    def compare_graph(Girrelevant, Grelevant, k):
        with open('logs/comparison-' + str(k) + '.txt', 'w') as outputFile:
            nodeCount = 0
            edgeCount = 0
            for node in Grelevant.nodes():
                if node in Girrelevant.nodes():
                    nodeCount += 1
                    outputFile.write("Common node: " + node + '\n')
            for edge in Grelevant.edges():
                if edge in Girrelevant.edges():
                    edgeCount += 1
                    outputFile.write("Common edge: " + ','.join(edge) + '\n')
            if len(Grelevant.nodes()) > 0:
                outputFile.write("fraction common nodes: " + str(
                    nodeCount / len(Grelevant.nodes())) + '\n')
            else:
                outputFile.write(
                    "fraction common nodes: 0, as relevant graph is empty\n")
            if len(Grelevant.edges()) > 0:
                outputFile.write("fraction common edges: " + str(
                    edgeCount / len(Grelevant.edges())) + '\n')
            else:
                outputFile.write(
                    "fraction common edges: 0, as relevant graph is empty\n")

    @staticmethod
    def write_output(Grelevant, Girrelevant, k):
        Util.compare_graph(Girrelevant, Grelevant, k)
        nx.write_edgelist(Grelevant, 'logs/relevant-edges-' + str(k) + '.txt')
        nx.write_edgelist(Girrelevant,
                          'logs/irrelevant-edges-' + str(k) + '.txt')

    @staticmethod
    def plot_recall(csv_file, batch_size, klist, save_file=None):
        df = pd.read_csv(csv_file)
        df = df[df['Relevant Count'] >= 10]
        fig, ax = plt.subplots(figsize=(7, 4))
        plt.ylim(0, 1)
        ax.yaxis.grid()
        plt.title(f"Batch-wise Recall value (batch size = {batch_size})")
        plt.xlabel('Batch Index')
        plt.ylabel('Recall')
        x = df['Age'].unique()
        plt.xticks(np.arange(1, x[-1] + 1))
        for k in klist:
            ax.plot(x, df[df['K'] == k]['Recall'], label=f'K = {k}',
                    marker='o')
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        if save_file is not None:
            plt.savefig(save_file)
        plt.show()

