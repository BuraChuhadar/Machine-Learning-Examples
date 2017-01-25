import numpy as np

from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.metrics import classification_report
from sklearn import svm
from sklearn.model_selection import cross_val_score
from learning_curve import plot_learning_curve
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

class support_vector_machines:
    def __init__(self, X, Y, KFolds, kernelFunction):
        self.KFolds = KFolds
        self.X = X
        self.Y = Y
        self.split(X, Y)
        self.kernelFunction = kernelFunction
        return


    def split(self, X, Y):
        split = StratifiedShuffleSplit(Y, n_iter=100, test_size=0.3)
        train_index, test_index = list(split)[0]
        self.trainX, self.trainY = X[train_index], Y[train_index]
        self.testX, self.testY = X[test_index], Y[test_index]


    def train(self):
        self.clf = svm.SVC(kernel= self.kernelFunction)
        self.clf.fit(self.trainX, self.trainY)

        self.y_pred = self.clf.predict(self.testX)



    def report(self):
        # print(classification_report(self.testY, self.y_pred))
        CV_Score1, CV_Score2, Accuracy_Score = cross_val_score(self.clf, self.testX, self.testY,
                                                               cv=self.KFolds).mean(), cross_val_score(self.clf,
                                                                                                       self.testX,
                                                                                                       self.testY,
                                                                                                       cv=self.KFolds * 2).mean(), accuracy_score(
            self.testY, self.y_pred)

        return CV_Score1, CV_Score2, Accuracy_Score

    def plot_learning_curve(self):
        plot_learning_curve(self.clf, 'Learning Curves for SVC', self.X, self.Y, ylim=(0.1, 1.01), cv=5, n_jobs=4)
        plt.show()