import csv
import math
import operator


class RankingEngine:
    def __init__(self, k):
        self.list_k = k
        pass

    @staticmethod
    def get_score(tweet, baseline):
        if baseline == "b1":
            return tweet.rscore - tweet.irscore  ######## B1
        elif baseline == 'b2':
            return tweet.rscore  ######### B2
        elif baseline == 'b3':
            if tweet.rscore == 0:
                return 0
            elif tweet.irscore == 0:
                print("What the fuck!!!!!")
                return 0
            return math.log(tweet.rscore / tweet.irscore)
        elif baseline == 'b4':
            return 0

    @staticmethod
    def get_edges_list(edgedict):
        outputlist = []
        for key in edgedict.keys():
            if edgedict[key][0] > 0 or edgedict[key][1] > 0:
                outputlist.append(key)
                outputlist.append(edgedict[key][0])
                outputlist.append(edgedict[key][1])
        return outputlist

    @staticmethod
    def rank(batch, age, baseline):
        age_str = str(age) if age >= 10 else "0"+str(age)
        with open('logs/ranked-list-' + age_str + '.csv', 'w') as outputFile:
            for tweet in batch:
                tweet.rank_score = RankingEngine.get_score(tweet, baseline)
            if baseline == 'b4':
                ranked_batch = sorted(batch, key=lambda tweet: (
                    -tweet.rscore, tweet.irscore))
            else:
                ranked_batch = sorted(batch,
                                      key=operator.attrgetter('rank_score'),
                                      reverse=True)
            outputWriter = csv.writer(outputFile)
            outputWriter.writerow(
                ["Text", "timestamp", "status", "label", "rank_score",
                 "incident_category", "rscore", "irscore",
                 'edge', 'rscore', 'irscore'])
            for tweet in ranked_batch:
                outputlist = RankingEngine.get_edges_list(tweet.edgedict)
                outputWriter.writerow(
                    [tweet.text, tweet.timestamp, tweet.status, tweet.label,
                     tweet.rank_score, tweet.category, tweet.rscore,
                     tweet.irscore, outputlist])
            return ranked_batch

    @staticmethod
    def eval(ranked_batch, age):
        with open('logs/ranking-metrics.txt', 'a') as outputFile:
            total_relevant, total_irrelevant = RankingEngine.count_labels(
                ranked_batch)
            outputFile.write(
                "New batch, age is: " + str(age) + " Batch contains " + str(
                    total_relevant) + " relevant tweets\n")
            if (total_relevant == 0):
                outputFile.write(
                    "Batch contains no relevant tweets, skipping metric "
                    "analysis\n")
                return []
            metrics = {}
            for k in range(1000, len(ranked_batch) + 1, 1000):
                num_relevant, num_irrelevant = RankingEngine.count_labels(
                    ranked_batch[:k])
                metrics[k] = [
                    RankingEngine.recall(num_relevant, total_relevant, k),
                    RankingEngine.specificity(num_irrelevant,
                                              total_irrelevant)]
                outputFile.write(
                    "Age: " + str(age) + " K: " + str(k) + " Recall: " + str(
                        metrics[k][0]) + '\n')
                if metrics[k][0] == 1.0 and k > total_relevant:
                    break
            return metrics

    @staticmethod
    def compute_NDCG(ranked_batch, age):
        with open('logs/ndcg.txt', 'a') as outputFile:
            total_relevant, total_irrelevant = RankingEngine.count_labels(
                ranked_batch)
            outputFile.write(
                "New batch, age is: " + str(age) + " Batch contains " + str(
                    total_relevant) + " relevant tweets\n")
            DCG = 0
            nf = 0
            scoreList = [tweet.label for tweet in ranked_batch]
            for j in range(len(scoreList)):
                DCG += float(scoreList[j]) / math.log(max(j, 2), 2)
            outputFile.write('#NDCG DCG is found to be: ' + str(DCG) + '\n')
            newlist = sorted(scoreList, reverse=True)
            if DCG > 0:
                for j in range(len(scoreList)):
                    nf += float(newlist[j]) / math.log(max(j, 2), 2)
                outputFile.write(
                    '#NDCG normalisation factor is: ' + str(nf) + '\n')
                outputFile.write(
                    'Age: ' + str(age) + " NDCG: " + str(DCG / nf) + '\n')
            else:
                return 0

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
    def recall(num_relevant, total_relevant, k):
        return num_relevant / min(total_relevant, k)

    @staticmethod
    def sensitivity(num_relevant, total_relevant):
        return num_relevant / total_relevant

    @staticmethod
    def specificity(num_irrelevant, total_irrelevant):
        return num_irrelevant / total_irrelevant
