class Classifier:

    def __init__(self):
        pass

    def train(self):
        pass

    def predict(self, rscore, irscore, act_labels):
        # todo
        self.act_label = act_labels
        self.pred_label = []
        return self.pred_label, self.act_label

    def eval(self):
        return self.calc_sensitivity(), self.calc_specificity()

    def calc_sensitivity(self):
        tp = 0
        fn = 0
        for i in range(len(self.pred_label)):
            if self.pred_label == 1 and self.act_label == 1:
                tp += 1
            elif self.act_label == 1 and self.pred_label == 0:
                fn += 1
        return tp / (tp + fn)

    def calc_specificity(self):
        tn = 0
        fp = 0
        for i in range(len(self.pred_label)):
            if self.pred_label == 0 and self.act_label == 0:
                tn += 1
            elif self.act_label == 0 and self.pred_label == 1:
                fp += 1
        return tn / (tn + fp)
