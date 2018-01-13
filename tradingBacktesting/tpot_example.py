from tpot import TPOTClassifier

from strategy import Strategy


class Tpot_example(Strategy):
    name = 'tpotExample'
    # We define out own parameters
    # machine learning classiffier
    tpotClassifier = TPOTClassifier(generations=5, population_size=20, cv=5,
                                    random_state=42, verbosity=2)
    treshold = 0.5
    currentPosition = 0

    ### **********************
    ### Override methods
    def init(self, dictionaryParameters, trainSet=None):
        if trainSet is None:
            raise Exception('Tpot algo requires a train set!')
        xTrain, yTrain = self.prepareDatasetForMachineLarning(trainSet)
        self.tpotClassifier.fit(xTrain, yTrain)
        trainingScore = self.tpotClassifier.score(xTrain, yTrain)
        print 'Finished tpotTraining with score %f' % trainingScore

    def onBar(self, bar):
        x, y = self.prepareDatasetForMachineLarning(bar)
        output = self.tpotClassifier.predict(x)

        # We buy only to exit a sell position (position<0 ) or in not position (position =0)
        if output > self.treshold and self.currentPosition <= 0:
            print 'Buy'
            self.currentPosition += 1

        # We sell only to exit a buy position (position>0 ) or in not position (position =0)
        elif output < self.treshold and self.currentPosition >= 0:
            print 'Sell'
            self.currentPosition -= 1
        else:
            print 'Nothing: current output %f' % self.currentPosition
        return Strategy.onBar(self, bar)

    ### **********************

    ### custom methods
    def prepareDatasetForMachineLarning(self, dataframeToPrepare):
        # input set
        input = dataframeToPrepare[['close', 'open', 'volume']]

        # target set
        output = dataframeToPrepare['close'].diff()

        return input, output
