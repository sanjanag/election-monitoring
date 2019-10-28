class Tweet:
    def __init__(self, args):
        self.text = args['report']
        self.timestamp = args['authored_at']
        self.status = 'Y' if isinstance(args['status'], str) else None
        self.label = 1 if self.status == 'Y' else 0
        # can use more args if required

    def __repr__(self):
        return 'Tweet(timestamp=' + str(self.timestamp) + ', text=' + self.text

    def __str__(self):
        return ', '.join([str(self.timestamp), self.text])

