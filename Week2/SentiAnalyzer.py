import numpy as np
import matplotlib.pyplot as plt
import itertools

class SentiAnalyzer:

    # Make the method signature to accept "sentidata" and "word"
    def __init__(self, sentidata, word):
        self.sentidata = sentidata       # Original Dataset
        self.numTraining = 150           # number of Training
        self.wordLimit = 1500            # number of words of interests
        self.dataWord = word             # list of words
        print('This is a senti analyzer')

    def runAnalysis(self, idxReview):
        probLogPositive = 0
        probLogNegative = 0
        idxUsedWords, usedWords = self.findUsedWords(idxReview)

        for i in range(len(idxUsedWords)):
            idxWord = idxUsedWords[i]
            positive, negative = self.calculateProbWord(idxWord)
            probLogPositive = probLogPositive + np.log(positive)
            probLogNegative = probLogNegative + np.log(negative)

        positiveProb1, negativeProb1 = self.calculateProbReview()
        probLogPositive = probLogPositive + np.log(positiveProb1)
        probLogNegative = probLogNegative + np.log(negativeProb1)

        # return correct as 1 if the review is positive and the analysis is positive and if the review is negative and the analysis is negative
        # 리뷰가 긍정이고 분석결과도 긍정, 리뷰가 부정이고 분석결과도 부정이면 1로 반환
        # return correct as 0 otherwise
        # 분석결과가 틀리면 0을 반환.

        # self.dataReviewTesting stores the correct review result by specifying 1 as a positive review
        # 만약 제대로 분류 했다면 1 .
        if self.dataReviewTesting[idxReview] == 1:
            if probLogPositive > probLogNegative:
                correct = 1
            else:
                correct = 0
        else:
            if probLogPositive > probLogNegative:
                correct = 0
            else:
                correct = 1
        return probLogPositive, probLogNegative, correct

    # 여러번 시도 - 바르게 분류한 경우들만 카운트. 카운트 저장, training 데이터셋 사이즈 다양하게 ?
    # 30 번 반복 . j 사이즈의  training data set 을 만들어라.
    def runWholeAnalysis(self):
        cnt = 0
        numCorrect = np.zeros((int(self.numTraining/30) + 1, 1))

        # for loop with 0, 30, 60, 90, 120, 150
        # make
        # numCorrect(0) = (sum of correct cases for 0 case) / (size of testing which is 1 in the current iteration)
        # numCorrect(1) = (sum of correct cases for 30 case) / (size of testing which is 30 in the current iteration)
        # and so on...
        # 재사용할 수 있는 코드 작성 하기
        # numcorrect는 매트릭스
        for j in range(0,self.numTraining+1, 30) :
            self.dataSentimentTraining = self.sentidata[self.shuffle[0:j+1], 0:self.wordLimit]
            self.dataReviewTraining = self.sentidata[self.shuffle[0:j+1], -1]
            numCorrect[cnt] = 0
            for i in range(np.shape(self.dataSentimentTesting)[0]):
                p, n, c = self.runAnalysis(i)
                if c == 1:
                    numCorrect[cnt] += 1
            numCorrect[cnt] = numCorrect[cnt] / np.shape(self.dataSentimentTesting)[0]
            cnt += 1
        return numCorrect

    # 평균 성능 계산 ,confidence interval ?  표준편차?
    # 넘파이 매트릭스. - 0으로 된 행렬 만들기 ! 그 안에 값을 넣어주기 .
    def runExperiments(self, numReplicate):
        average = np.zeros((int(self.numTraining/30 + 1), 1))
        averageSq = np.zeros((int(self.numTraining/30 + 1), 1))

        # iterate by the numReplicate
        for i in range(numReplicate):
            self.shuffle = np.arange(np.shape(self.sentidata)[0])
            np.random.shuffle(self.shuffle)

            self.dataSentimentTesting = self.sentidata[self.shuffle[self.numTraining+1:198], 0:self.wordLimit]
            self.dataReviewTesting = self.sentidata[self.shuffle[self.numTraining + 1:198], -1]

            # receive the correct information from runWholeAnalysis()
            correct = self.runWholeAnalysis()
            # calculate the average by the training case sizes
            average =  average + correct
            # calculate the squared average by the training case sizes
            averageSq += correct * correct

        # finish the calculation of average
        average = average / numReplicate
        # finish the calculation of average squared
        averageSq = averageSq / numReplicate
        # finish the calculation of standard deviation
        std = np.sqrt(averageSq - average*average)

        average = list(itertools.chain(*average))
        std = list(itertools.chain(*std))
        plt.errorbar(np.arange(0, self.numTraining+1, 30), average, std)
        plt.title('Product Review Classification')
        plt.xlabel('Number of Cases')
        plt.ylabel('Percentage of Correct Classification')
        plt.show()

    def calculateProbWord(self, idxWord):
        occurrence = [[row[idxWord]] for row in self.dataSentimentTraining]
        positive = np.matmul(np.transpose(occurrence), self.dataReviewTraining)
        dataNegReviewTraining = [[1-row] for row in self.dataReviewTraining]
        negative = np.matmul(np.transpose(occurrence), dataNegReviewTraining)
        positiveProb = int(positive+1) / float(positive+negative+1)
        negativeProb = int(negative+1) / float(positive+negative+1)
        return positiveProb, negativeProb

    def calculateProbReview(self):
        numReviews = max(np.shape(self.dataReviewTraining))
        positive = np.sum(self.dataReviewTraining)
        negative = numReviews - positive
        positiveProb = int(positive + 1) / float(numReviews + 1)
        negativeProb = int(negative + 1) / float(numReviews + 1)
        return positiveProb, negativeProb

    def findUsedWords(self, idx):
        idxUsedWords = np.where(self.dataSentimentTesting[idx] == 1)[0]
        usedWords = self.dataWord[idxUsedWords]
        return idxUsedWords, usedWords

