import networkx as nx
import re
from itertools import combinations
from nltk.corpus import stopwords
from collections import OrderedDict

punctuations = "!\"(),-./:;<=>?[\\]^_`{|}~'"
refinedPunctuations = ",|\.|;"
stopWords = set(stopwords.words('english'))

def is_valid(token):
	if len(token) <= 1 or token.startswith('@') or token.startswith('http'): #remove urls and @ mentions
		return False
	return True

def sanitize(tokens):
	newTokens = []
	for token in tokens:
		token = token.strip(punctuations) #remove punctuations
		splitTokens = re.split(refinedPunctuations,token) #because people dont put space after some imp. punctuations like comma and fullstop
		for splitToken in splitTokens:
			if (is_valid(splitToken)): #need to check validity again after stripping and removing symbols
				newTokens.append(splitToken)
	return newTokens

def tokenize(tweet):
	tweet = re.sub(r'[^\x00-\x7f]',r'', tweet) #remove non-ascii chars
	tokens = tweet.split() #split about empty spaces
	tokens = [x.lower() for x in tokens if is_valid(x)] #remove URLs, @ mentions etc. 
	tokens = sanitize(tokens) #remove random characters and punctions, #hash should not be removed
	tokens = [x for x in tokens if not x in stopWords] #remove stop words
	tokens = list(OrderedDict.fromkeys(tokens)) #remove duplicates, while maintaining order
	# print(tweet)
	# print(tokens)
	return tokens

def update_weight(edge):
	edge['weight'] += 1

def get_edges(tokens):
	edges = list(combinations(tokens,2))
	return edges

def add_to_graph(tokens,G,k):
	newEdges = get_edges(tokens)
	for edge in newEdges:
		if not edge in G.edges():
			G.add_edge(edge[0],edge[1])
			G[edge[0]][edge[1]]['weight'] = 0
		update_weight(G[edge[0]][edge[1]])
		G[edge[0]][edge[1]]['time_interval'] = k



# def sanitize(tokens):
# 	newTokens = []
# 	for token in tokens:
# 		# print("token is: " + token)
# 		for char in punctuations:
# 			# print ("token: " + token)
# 			# print("char: " + char)
# 			token = token.replace(char,'')
# 		newToken = token.strip("'")
# 		if (is_valid(token)): #need to check validity again after stripping and removing symbols
# 			# print("new token is: " + newToken)
# 			newTokens.append(newToken)
# 	return newTokens
