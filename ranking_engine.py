import operator
import json

class RankingEngine:
    def __init__(self, k):
        self.list_k = k
        pass

    @staticmethod
    def get_score(tweet):
        return tweet.rscore - tweet.irscore

    @staticmethod
    def rank(batch, age):
        with open('logs/ranked-list-' + str(age) + '.txt', 'w') as outputFile:
            for tweet in batch:
                tweet.rank_score = RankingEngine.get_score(tweet)
            ranked_batch = sorted(batch, key=operator.attrgetter('rank_score'),
                                  reverse=True)
            for tweet in ranked_batch:
                outputFile.write(json.dumps(tweet.__dict__, default=str))
                outputFile.write('\n')
            return ranked_batch

    @staticmethod
    def eval(ranked_batch, age):
        with open('logs/ranking-metrics.txt','a') as outputFile:
            total_relevant, total_irrelevant = RankingEngine.count_labels(
                ranked_batch)
            outputFile.write("New batch, age is: " + str(age) + " Batch contains " + str(total_relevant) + " relevant tweets\n")
            if (total_relevant == 0):
                outputFile.write("Batch contains no relevant tweets, skipping metric analysis")
                return []
            metrics = {}
            for k in range(10, len(ranked_batch), 10):
                num_relevant, num_irrelevant = RankingEngine.count_labels(
                    ranked_batch[:k])
                metrics[k] = [
                    RankingEngine.recall(num_relevant, total_relevant, k),
                    RankingEngine.specificity(num_irrelevant, total_irrelevant)]
                outputFile.write("Age: " + str(age) + " K: " + str(k) + " Recall: " + str(metrics[k][0]) + '\n')
                if metrics[k][0] == 1.0:
                    break
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
    def recall(num_relevant,total_relevant,k):
        return num_relevant / min(total_relevant,k)
   
    @staticmethod
    def sensitivity(num_relevant, total_relevant):
        return num_relevant / total_relevant

    @staticmethod
    def specificity(num_irrelevant, total_irrelevant):
        return num_irrelevant / total_irrelevant
