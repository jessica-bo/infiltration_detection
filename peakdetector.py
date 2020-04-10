import numpy as np

class PeakDetector:
    def __init__(self, array, lag, threshold, influence):
        self.y = list(array)
        self.length = len(self.y)
        self.lag = lag
        self.threshold = threshold
        self.influence = influence
        self.signals = [0] * len(self.y)
        self.filteredY = np.array(self.y).tolist()
        self.avgFilter = [0] * len(self.y)
        self.stdFilter = [0] * len(self.y)
        self.avgFilter[self.lag - 1] = np.mean(self.y[0:self.lag]).tolist()
        self.stdFilter[self.lag - 1] = np.std(self.y[0:self.lag]).tolist()

    def thresholding_algo(self):
        signals = np.zeros(len(self.y))
        filteredY = np.array(self.y)
        avgFilter = [0]*len(self.y)
        stdFilter = [0]*len(self.y)
        avgFilter[self.lag - 1] = np.mean(self.y[0:self.lag])
        stdFilter[self.lag - 1] = np.std(self.y[0:self.lag])
        for i in range(self.lag, len(self.y) - 1):
            #checks if current point deviates from average by threshold amount
            if abs(self.y[i] - avgFilter[i-1]) > self.threshold * stdFilter [i-1]:
                if self.y[i] > avgFilter[i-1]:
                    signals[i] = 1
                else:
                    signals[i] = -1
                #updates average by influence of current point
                filteredY[i] = self.influence * self.y[i] + (1 - self.influence) * filteredY[i-1]
                avgFilter[i] = np.mean(filteredY[(i-self.lag):i])
                stdFilter[i] = np.std(filteredY[(i-self.lag):i])
            else:
                signals[i] = 0
                filteredY[i] = self.y[i]
                avgFilter[i] = np.mean(filteredY[(i-self.lag):i])
                stdFilter[i] = np.std(filteredY[(i-self.lag):i])
    
        return dict(signals = np.asarray(signals),
                    avgFilter = np.asarray(avgFilter),
                    stdFilter = np.asarray(stdFilter))
    
    
    def realtime_thresholding_algo(self, new_value):
        self.y.append(new_value)
        i = len(self.y) - 1
        self.length = len(self.y)
        if i < self.lag:
            return 0
        elif i == self.lag:
            self.signals = [0] * len(self.y)
            self.filteredY = np.array(self.y).tolist()
            self.avgFilter = [0] * len(self.y)
            self.stdFilter = [0] * len(self.y)
            self.avgFilter[self.lag - 1] = np.mean(self.y[0:self.lag]).tolist()
            self.stdFilter[self.lag - 1] = np.std(self.y[0:self.lag]).tolist()
            return 0
        
        self.signals += [0]
        self.filteredY += [0]
        self.avgFilter += [0]
        self.stdFilter += [0]

        if abs(self.y[i] - self.avgFilter[i - 1]) > self.threshold * self.stdFilter[i - 1]:
            if self.y[i] > self.avgFilter[i - 1]:
                self.signals[i] = 1
            else:
                self.signals[i] = -1

            self.filteredY[i] = self.influence * self.y[i] + (1 - self.influence) * self.filteredY[i - 1]
            self.avgFilter[i] = np.mean(self.filteredY[(i - self.lag):i])
            self.stdFilter[i] = np.std(self.filteredY[(i - self.lag):i])
        else:
            self.signals[i] = 0
            self.filteredY[i] = self.y[i]
            self.avgFilter[i] = np.mean(self.filteredY[(i - self.lag):i])
            self.stdFilter[i] = np.std(self.filteredY[(i - self.lag):i])

        return self.signals[i]
    
    def extractpeaktime(signals):
        for i in range(len(signals)-1):
            #looks for positive increases in signal
            if signals[i] < signals[i+1]:
                return i+0.5
            