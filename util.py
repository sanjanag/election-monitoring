import re
from collections import OrderedDict

import networkx as nx
from nltk.corpus import stopwords

punctuations = "!\"(),-./:;<=>?[\\]^_`{|}~'"
refinedPunctuations = ",|\.|;"
stopWords = set(stopwords.words('english'))


class Util:
    @staticmethod
    def score_tweet(outputFile, edges, G):
        score = 0
        for edge in edges:
            if edge in G.edges():
                outputFile.write(','.join(edge) + " : " + str(
                    G[edge[0]][edge[1]]['weight']) + '\n')
                score += G[edge[0]][edge[1]]['weight']
        return score

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
        tokens = [x.lower() for x in tokens if Util.is_valid(x)]  # remove
        # URLs,
        # @ mentions etc.
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
    def compare_graph(Girrelevant, Grelevant, k):
        with open('comparison-' + str(k) + '.txt', 'w') as outputFile:
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
            outputFile.write("fraction common nodes: " + str(
                nodeCount / len(Grelevant.nodes())) + '\n')
            outputFile.write("fraction common edges: " + str(
                edgeCount / len(Grelevant.edges())) + '\n')



    @staticmethod
    def write_output(Grelevant, Girrelevant, k):
        Util.compare_graph(Girrelevant, Grelevant, k)
        nx.write_edgelist(Grelevant, 'relevant-edges-' + str(k) + '.txt')
        nx.write_edgelist(Girrelevant, 'irrelevant-edges-' + str(k) + '.txt')
