import operator
import json
import csv
class RankingEngine:
    def __init__(self, k):
        self.list_k = k
        pass

    @staticmethod
    def get_score(tweet,baseline):
        if baseline == "b1":
            return tweet.rscore - tweet.irscore ######## B1
        elif baseline == 'b2':
            return tweet.rscore ######### B2

    @staticmethod
    def rank(batch, age, baseline):
        with open('logs/ranked-list-' + str(age) + '.csv', 'w') as outputFile:
            for tweet in batch:
                tweet.rank_score = RankingEngine.get_score(tweet,baseline)
            ranked_batch = sorted(batch, key=operator.attrgetter('rank_score'),
                                  reverse=True)
            outputWriter = csv.writer(outputFile)
            outputWriter.writerow(["Text","timestamp","status","rank_score","rscore","irscore",'edges'])
            for tweet in ranked_batch:
                outputWriter.writerow([tweet.text,tweet.timestamp,tweet.status,tweet.rank_score,tweet.rscore,tweet.irscore,tweet.edges])
            return ranked_batch

    @staticmethod
    def eval(ranked_batch, age):
        with open('logs/ranking-metrics.txt','a') as outputFile:
            total_relevant, total_irrelevant = RankingEngine.count_labels(
                ranked_batch)
            outputFile.write("New batch, age is: " + str(age) + " Batch contains " + str(total_relevant) + " relevant tweets\n")
            if (total_relevant == 0):
                outputFile.write("Batch contains no relevant tweets, skipping metric analysis\n")
                return []
            metrics = {}
            for k in range(1000, len(ranked_batch)+1, 1000):
                num_relevant, num_irrelevant = RankingEngine.count_labels(
                    ranked_batch[:k])
                metrics[k] = [
                    RankingEngine.recall(num_relevant, total_relevant, k),
                    RankingEngine.specificity(num_irrelevant, total_irrelevant)]
                outputFile.write("Age: " + str(age) + " K: " + str(k) + " Recall: " + str(metrics[k][0]) + '\n')
                if metrics[k][0] == 1.0 and k > total_relevant:
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
