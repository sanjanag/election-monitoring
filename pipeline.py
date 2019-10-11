#author -- Shubham
#This file can act as a pipeline where we call different methods and do our analysis 
#Right now, this file has the method stubs for all the methods in the pipeline such as scoring, pruning etc.
#Actual methods will be developed in separate scripts and can be imported here. 
# keep only english language dictionary words? 
import networkx as nx
import csv
import update_graph as ug

def prune_edges(G,k):
	with open("pruning-" + str(k) + '.txt', 'w') as outputFile:
		allEdges = list(G.edges())
		for edge in allEdges:
			if G[edge[0]][edge[1]]['weight'] == 1 and G[edge[0]][edge[1]]['time_interval'] < k:
				outputFile.write("pruning edge: " + ','.join(edge) + '\n')
				G.remove_edge(*edge)
		G.remove_nodes_from(list(nx.isolates(G)))

def compare_graph(Girrelevant,Grelevant,k):
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
		outputFile.write("fraction common nodes: " + str(nodeCount/len(Grelevant.nodes())) + '\n')
		outputFile.write("fraction common edges: " + str(edgeCount/len(Grelevant.edges())) + '\n')

def score_tweet(outputFile, edges,G):
	score = 0
	for edge in edges:
		if edge in G.edges():
			outputFile.write(','.join(edge) + " : " + str(G[edge[0]][edge[1]]['weight']) + '\n')
			score += G[edge[0]][edge[1]]['weight']
	return score

def write_output(Grelevant,Girrelevant,k):
	compare_graph(Girrelevant,Grelevant,k)
	nx.write_edgelist(Grelevant,'relevant-edges-' + str(k) + '.txt')
	nx.write_edgelist(Girrelevant,'irrelevant-edges-' + str(k) + '.txt')

def get_batch(size,nextBatchAvailable):
	return None;

def update_graphs(batch, Grelevant, Girrelevant, k):
	for tweetDict in batch:
		tokens = ug.tokenize(tweetDict['text'])
		if tweetDict['status'] == 'NULL':
			ug.add_to_graph(tokens,Girrelevant,k)	
		else:
			ug.add_to_graph(tokens,Grelevant,k)

Grelevant = nx.Graph()
Girrelevant = nx.Graph()

# ########## This is the pipeline ##############
# nextBatchAvailable = True
# batchSize = 200
# k = 1 #denotes batch count
# maxBatches = 100
# while nextBatchAvailable and k <= maxBatches:
# 	batch = get_batch(batchSize,nextBatchAvailable)
# 	if k > 1:
# 		evaluate(batch,Grelevant,Girrelevant)
# 	update_graphs(batch,Grelevant,Girrelevant,k)
# 	if k > 1:
# 		prune_edges(Girrelevant,k)
# 	write_output(Grelevant,Girrelevant,k)

########### For testing ################
j = 0;
k = 1
tweets = []
with open('test.csv', 'r') as inputFile:
	csvReader = csv.reader(inputFile)
	headers = next(csvReader)
	for line in csvReader:
		tweet = line[0]
		# print("tweet: " + tweet)
		tokens = ug.tokenize(tweet)
		# print ("tokens: ")
		# print(tokens)
		if line[4] == 'NULL':
			ug.add_to_graph(tokens,Girrelevant,k)	
		else:
			ug.add_to_graph(tokens,Grelevant,k)
		j += 1
		print(j)
		if j % 200 == 0:
			if k > 1:
				prune_edges(Girrelevant,k)
			write_output(Grelevant,Girrelevant,k)
			k += 1
		if j == 500:
			break


############ For scoring ##############
with open('test-2.csv', 'r') as inputFile, open('scoring.txt', 'w') as outputFile:
	csvReader = csv.reader(inputFile)
	headers = next(csvReader)
	for line in csvReader:
		tweet = line[0]
		tokens = ug.tokenize(tweet)
		edges = ug.get_edges(tokens)
		outputFile.write(tweet + '\n')
		# print(*edges)
		relevantScore = score_tweet(outputFile, edges, Grelevant)
		irrelevantScore = score_tweet(outputFile, edges, Girrelevant)
		outputFile.write("Relevant Score: " + str(relevantScore) + " | Irrelevant Score: " + str(irrelevantScore) + '\n')

