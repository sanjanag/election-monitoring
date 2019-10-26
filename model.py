from classifier import Classifier
from graph import Graph
from ranking_engine import RankingEngine
from simulator import Simulator


class Model():
    def __init__(self, stream_file='test.csv', init_size=2000, test_size=100, \
                 prune_interval=200, approach='RANK', k=[10, 100, 500]):
        self.gr = Graph()
        self.gir = Graph()
        self.init_size = init_size
        self.test_size = test_size
        self.prune_interval = prune_interval
        self.age = 1
        self.simulator = Simulator(stream_file)
        self.approach = approach
        self.classifier = Classifier()
        self.ranking_engine = RankingEngine(k)
        self.results = []
        self.k = k

    def add_batch(self, batch):
        for i, tweet in enumerate(batch):
            if isinstance(tweet.status, str):
                self.gr.add_tweet(tweet, self.age)
            else:
                self.gir.add_tweet(tweet, self.age)
            if i % self.prune_interval == 0:
                self.gir.prune_edges(self.age)
                self.age += 1
                # if self.gr.number_of_nodes() > 0:
                #     Util.write_output(gir, gr, curr_age)

    def initialize(self):
        init_batch = self.simulator.get_next_batch(2000)
        self.add_batch(init_batch)

    def score_batch(self, batch):
        rscore = []
        irscore = []
        for tweet in batch:
            rscore.append(self.gr.score(tweet))
            irscore.append(self.gir.score(tweet))
        return rscore, irscore

    def get_classifier_metrics(self, rscore, irscore, act_labels):
        self.classifier.predict(rscore, irscore, act_labels)
        return self.classifier.eval()

    def get_ranking_metrics(self, rscore, irscore, act_labels):
        self.ranking_engine.rank(rscore, irscore, act_labels)
        return self.ranking_engine.eval()

    def run(self):
        while self.simulator.has_next_batch():
            batch = self.simulator.get_next_batch(self.test_size)
            rscore, irscore = self.score_batch(batch)
            act_labels = [tweet.label for tweet in batch]
            if self.approach == 'RANK':
                batch_results = self.get_ranking_metrics(rscore,
                                                         irscore, act_labels)
            else:
                batch_results = self.get_classifier_metrics(rscore,
                                                            irscore,
                                                            act_labels)
            self.results.append(batch_results)
            self.add_batch(batch)
