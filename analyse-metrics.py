import csv

from util import Util

# inputFolders = ['complete-b1-5000/', 'complete-b1-10000/',
# 'complete-b1-20000/']
inputFolders = ['logs/']

for folder in inputFolders:
    with open(folder + 'ranking-metrics.txt', 'r') as inputFile, open(
            folder + 'plot-metrics.csv', 'w') as outputFile:
        outputWriter = csv.writer(outputFile)
        outputWriter.writerow(['Age', 'K', 'Recall', 'Relevant Count'])
        print(folder)
        relevantcount = '0'
        for line in inputFile:
            if 'contains' in line:
                line = line.split()
                relevantcount = line[line.index('contains') + 1]
                print(relevantcount)
                try:
                    int(relevantcount)
                except Exception as e:
                    relevantcount = '0'
            elif int(relevantcount) > 0 and ':' in line:
                line = line.split()
                line = [x.strip(':') for x in line]
                if int(line[3]) % 1000 == 0:
                    outputWriter.writerow(
                        [line[1], line[3], line[5], relevantcount])

Util.plot_recall("./logs/plot-metrics.csv", 10000, [1000, 2000, 3000, 5000],
                 "recall.png")
