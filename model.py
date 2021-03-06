import json
import os
import shutil
import sys

from classifier import Classifier
from graph import Graph
from ranking_engine import RankingEngine
from simulator import Simulator
from util import Util


# usage python3 model.py <batchsize> <baseline> <decayflag>
class Model():
    def __init__(self, stream_file='test.csv', init_size=200,
                 batch_size=200, \
                 prune_interval=200, approach='RANK', baseline='b1',
                 decayflag=False):
        self.gr = Graph()
        self.gir = Graph()
        self.init_size = init_size
        self.batch_size = batch_size
        self.prune_interval = prune_interval
        self.age = 0
        self.simulator = Simulator(stream_file)
        self.approach = approach
        self.classifier = Classifier()
        self.results = []
        self.baseline = baseline
        self.decayflag = decayflag

    def add_batch(self, batch):
        self.age += 1
        for i, tweet in enumerate(batch):
            if isinstance(tweet.status, str):
                self.gr.add_tweet(tweet, self.age)
            else:
                self.gir.add_tweet(tweet, self.age)
        self.prune_graph()
        # self.decay_edges()            # commented this out since current
        # logic doesnt require iterative decay updates

    def prune_graph(self):
        if self.age > 1:
            print("Pruning edges")  #######log statement
            self.gir.prune_edges(self.age)

    def initialize(self):
        init_batch = self.simulator.get_next_batch(self.init_size)
        print("Adding initial batch to the graph")  #######log statement
        self.add_batch(init_batch)

    def score_tweet(self, tweet):
        # with open('scoring-' + str(self.age) + '.txt','a') as outputFile:
        # outputFile.write(tweet.text + '\n') #######log statement
        tweet.set_edges()
        edges = tweet.edges
        if len(edges) == 0:
            # outputFile.write("Tweet with no edges, will be ignored for
            # scoring\n") #######log statement
            return
        edgerscore = 0
        edgeirscore = 0
        for edge in edges:
            rscore = 0
            irscore = 0
            if edge in self.gr.graph.edges():
                #     rscore = sum(self.gr.graph[edge[0]][edge[1]][
                #     'weight'].values())
                if not self.decayflag == 'True':
                    rscore = sum(
                        self.gr.graph[edge[0]][edge[1]]['weight'].values())
                else:
                    rscore = self.gr.get_decay_value(edge, self.age + 1)
                    # print('decay score ', rscore)
                    # print('at age ', curr_age)
            else:
                rscore = 0
            if edge in self.gir.graph.edges():
                if not self.decayflag == 'True':
                    irscore = sum(
                        self.gir.graph[edge[0]][edge[1]]['weight'].values())
                else:
                    irscore = self.gir.get_decay_value(edge, self.age + 1)
                    # print(edge)
                    # print('decay score ', irscore)
                    # print('at age ', self.age)
            else:
                irscore = 0
            tweet.edgedict[edge] = [rscore, irscore]
            if not rscore == 0 or not irscore == 0:
                edgerscore += rscore / (rscore + irscore)
                edgeirscore += irscore / (rscore + irscore)
            # outputFile.write("Edge: " + ','.join(edge) + " Rscore: " +
            # str(rscore) + " IRscore: " + str(irscore) + '\n') #######log
            # statement
        # outputFile.write("Rscore: " + str(edgerscore) + " IRscore: " +
        # str(edgeirscore) + "\n") #######log statement
        tweet.rscore = edgerscore / len(edges)
        tweet.irscore = edgeirscore / len(edges)

    def score_batch(self, batch):
        for tweet in batch:
            self.score_tweet(tweet)

    def get_classifier_metrics(self, batch):
        self.classifier.predict(batch)
        return self.classifier.eval()

    def get_ranking_metrics(self, batch, age):
        ranked_batch = RankingEngine.rank(batch, age, self.baseline)
        RankingEngine.compute_NDCG(ranked_batch, age)
        return RankingEngine.eval(ranked_batch, age)

    def run(self):
        j = 0
        while self.simulator.has_next_batch():
            j += 1
            # print(j)
            print("Current model age is: ", self.age)  #######log statement
            print("Received a new batch")  #######log statement
            batch = self.simulator.get_next_batch(self.batch_size)
            print("First step: scoring the batch")  #######log statement
            self.score_batch(batch)
            if self.approach == 'RANK':
                print("Getting ranking metrics")  #######log statement
                batch_results = self.get_ranking_metrics(batch, self.age)
            else:
                batch_results = self.get_classifier_metrics(batch)
            # print(batch_results)
            self.results.append(batch_results)
            # if j > 1:
            #     break
            print("Second step: adding the new batch")  #######log statement
            self.add_batch(batch)
            # if j >1:
            #     break


if __name__ == '__main__':
    if os.path.exists('logs/'):
        shutil.rmtree('logs/')
    os.makedirs('logs/')
    with open('logs/ranking-metrics.txt', 'w') as outputFile:
        outputFile.write('\n')

    batchsize = sys.argv[1]
    baseline = sys.argv[2]
    decayflag = sys.argv[3]
    outputDirectory = "complete-" + baseline + "-" + str(batchsize)

    model = Model(stream_file='tweets_processing/data/tweets.csv',
                  init_size=int(batchsize),
                  batch_size=int(batchsize),
                  baseline=baseline,
                  decayflag=decayflag)
    print("Initializing the model with params: " + json.dumps(model.__dict__,
                                                              default=str))  #######log statement
    model.initialize()
    model.run()
    Util.write_output(model.gr.graph, model.gir.graph, model.age)
