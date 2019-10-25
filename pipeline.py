from graph import Graph
from simulator import Simulator
from util import Util


def process_batch(batch, gr, gir, curr_age, prune_thresh):
    for i, tweet in enumerate(batch):
        if isinstance(tweet.status, str):
            gr.add_tweet(tweet, curr_age)
        else:
            gir.add_tweet(tweet, curr_age)
        if i % prune_thresh == 0:
            gir.prune_edges(curr_age)
            curr_age += 1
            if gr.number_of_nodes() > 0:
                Util.write_output(gir, gr, curr_age)
    return curr_age


curr_age = 1
prune_thresh = 200
size = 100
gr = Graph()
gir = Graph()
batch_num = 1

# processing
train_sim = Simulator('test.csv')
while train_sim.has_next_batch():
    print("Processing batch: " + str(batch_num))
    batch = train_sim.get_next_batch(size)
    curr_age = process_batch(batch, gr, gir, curr_age, prune_thresh)
    batch_num += 1

# evaluating
outputFile = open('scoring.txt', 'w')

test_sim = Simulator('test-2.csv')
tweets = test_sim.get_all()
for tweet in tweets:
    rscore = gr.score(tweet)
    irscore = gir.score(tweet)
    outputFile.write(
        "Relevant Score: " + str(rscore) + " | Irrelevant Score: " + str(
            irscore) + " " + tweet.text + '\n')
