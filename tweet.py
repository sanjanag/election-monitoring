from util import Util

class Tweet:
    def __init__(self, args):
        self.text = args['report']
        self.timestamp = args['authored_at']
        self.status = 'Y' if isinstance(args['relevant'], str) else None
        self.label = 1 if self.status == 'Y' else 0
        self.predictedlabel = 0
        self.rank_score = 0
        self.rscore = 0
        self.irscore = 0
        self.edges = []
        self.edgedict = {}
        # can use more args if required

    def __repr__(self):
        return 'Tweet(timestamp=' + str(self.timestamp) + ', text=' + self.text

    def __str__(self):
        return ', '.join([str(self.timestamp), self.text])

    def setrscore(self, rscore):
        self.rscore = rscore

    def setirscore(self, irscore):
        self.irscore = irscore

    def setrankscore(self, rankscore):
        self.rank_score = rankscore

    def setpredictedlabel(label):
        self.predictedlabel = label

    def getpredictedlabel(label):
        return self.predictedlabel

    def set_edges(self):
        try:
           tokens = Util.tokenize(self.text)
        except TypeError as e:
            print("Found typeerror, tweet will be ignored")
            return []

        window_size = 2
        edges = Util.get_windowed_edges(tokens, window_size)
        self.edges = edges

