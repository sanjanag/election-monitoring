import operator


class RankingEngine:
    def __init__(self, k):
        self.list_k = k
        pass

    @staticmethod
    def rank(batch):
        for tweet in batch:
            tweet.rank_score = tweet.rscore - tweet.irscore
        ranked_batch = sorted(batch, key=operator.attrgetter('rank_score'),
                              reverse=True)
        return ranked_batch

    @staticmethod
    def eval(ranked_batch):
        total_relevant, total_irrelevant = RankingEngine.count_labels(
            ranked_batch)
        metrics = {}
        for k in range(10, len(ranked_batch), 10):
            num_relevant, num_irrelevant = RankingEngine.count_labels(
                ranked_batch[:k])
            metrics[k] = [
                RankingEngine.sensitivity(num_relevant, total_relevant),
                RankingEngine.specificity(num_irrelevant, total_irrelevant)]
        return metrics

    @staticmethod
    def count_labels(tweets):
        num_relevant = 0
        num_irrelevant = 0
        for tweet in tweets:
            if tweet.label == 1:
                num_relevant += 1
            else:
                num_irrelevant += 1
        return num_relevant, num_irrelevant

    @staticmethod
    def sensitivity(num_relevant, total_relevant):
        return num_relevant / total_relevant

    @staticmethod
    def specificity(num_irrelevant, total_irrelevant):
        return num_irrelevant / total_irrelevant
