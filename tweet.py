class Tweet:
    def __init__(self, args):
        self.text = args['report']
        self.timestamp = args['authored_at']
        self.status = 'Y' if isinstance(args['status'], str) else None
        self.label = 1 if self.status == 'Y' else 0
        self.predictedlabel = 0
        self.rankscore = 0
        self.rscore = 0
        self.irscore = 0
        # can use more args if required

    def __repr__(self):
        return 'Tweet(timestamp=' + str(self.timestamp) + ', text=' + self.text

    def __str__(self):
        return ', '.join([str(self.timestamp), self.text])

    def setrscore(rscore):
        self.rscore = rscore

    def getrscore(rscore):
        return rscore

    def setirscore(irscore):
        self.irscore = irscore
   
    def getirscore(irscore):
        return self.irscore
   
    def setrankscore(rankscore):
        self.rankScore = rankscore
    
    def getrankscore(rankscore):
        return self.rankscore

    def setpredictedlabel(label):
        self.predictedlabel = label

    def getpredictedlabel(label):
        return self.predictedlabel

