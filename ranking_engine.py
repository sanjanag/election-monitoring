class RankingEngine:
    def __init__(self, k):
        self.list_k = k
        pass

    def rank(self, batch):
        for tweet in batch:
            tweet.setrankscore(tweet.getrscore() - tweet.getirscore())
        rankedBatch = sorted(batch, key = itemgetter(rankscore))
        #assume they are ranked
        self.act_labels = act_labels
        self.ranked_labels = []  # todo
        rankings = []
        return rankings

    def eval(self):
        total_relevant, total_irrelevant = self.count_labels(self.act_labels)
        return self.calc_sensitivity(total_relevant), self.calc_specificity(
            total_irrelevant)

    def count_labels(self, labels):
        num_relevant = 0
        num_irrlevant = 0
        for label in labels:
            if label == 1:
                num_relevant += 1
            else:
                num_irrlevant += 1
        return num_relevant, num_irrlevant

    def calc_sensitivity(self, total_relevant):
        metrics = []
        for k in self.list_k:
            num_relevant, num_irrlevant = self.count_labels(
                self.ranked_labels[:k])
            metrics.append(num_relevant / total_relevant)
        return metrics

    def calc_specificity(self, total_irrelevant):
        metrics = []
        for k in self.list_k:
            num_relevant, num_irrlevant = self.count_labels(
                self.ranked_labels[:k])
            metrics.append(num_irrlevant / total_irrelevant)
        return metrics
