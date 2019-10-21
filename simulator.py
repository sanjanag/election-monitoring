import pandas as pd

from tweet import Tweet


class Simulator:

    def __init__(self, tweet_csv="./test.csv", start_id=0):
        self.tweets_df = pd.read_csv(tweet_csv, parse_dates=['authored_at'])
        self.tweets_df = self.tweets_df.sort_values(by=['authored_at'])
        self.tweets_df[self.tweets_df['source'] == 'Twitter']
        self.tweets_df = self.tweets_df.drop(columns=['source'])

        self.next_id = start_id
        self.last_id = self.tweets_df.shape[0]

    def has_next_batch(self):
        if self.next_id == self.last_id:
            return False
        return True

    def get_next_batch(self, size):
        if not self.has_next_batch():
            raise Exception("Next batch does not exist.")
        start = self.next_id
        end = min(start + size, self.last_id)
        self.next_id = end
        batch_df = self.tweets_df.iloc[start:end]
        records = batch_df.to_dict('r')
        tweets = [Tweet(record) for record in records]
        return tweets
