import math

class SentiAnalyzer:

    # Make the method signature to accept "sentidata" and "word"
    def __init__(self):
        print('This is a senti analyzer')
    # 단어가 긍정일 확률, 부정일 확률 계산
    # 리뷰, 단어 파일과 단어의 인덱스를 입력하면 그 입력받은 인덱스의 단어를 pointedWord에 저장
    # 리뷰 변수에 리뷰들 저장,occurence 변수에 입력받은 단어인덱스의 행을 저장. ??
    def probWordPositiveAndNegative(self, sentidata, word, idxWord):
        pointedWord = word[idxWord]
        reviews = [int(float(row[-1])) for row in sentidata]
        occurrence = [int(float(row[idxWord])) for row in sentidata]

        # Calculate the number of positive review occurrence with the pointed word, and assign the calculated value to 'positive'
        # pointedWord 가 있는 리뷰에서 긍정인 경우 - 둘다 1인경우 : positive 로 저장.
        positive = 0
        for i in range(len(occurrence)):
            positive = positive + occurrence[i] * reviews[i]

        # Calculate the number of positive reviews from the entire review set
        # 전체 리뷰에서 긍정적인 리뷰의 개수 계산 - 1이니까 그냥 더하면 됨 !
        numPositiveReviews = sum(reviews)

        # Calculate the number of negative review occurrence with the pointed word, and assign the calculated value to 'negative'
        # negative 일 경우, 0이므로 1에서 뺴서 값 저장
        negative = 0
        for i in range(len(occurrence)):
            negative = negative + occurrence[i] * (1 - reviews[i])


        rowCount = len(sentidata)
        positiveProb = float(positive) / float(numPositiveReviews)
        negativeProb = float(negative) / float(rowCount - numPositiveReviews)

        if positiveProb == 0:
            positiveProb = 0.00001
        if negativeProb == 0:
            negativeProb = 0.00001
        # 단어랑, 긍정일 확률, 부정일 확률 리턴
        return pointedWord, positiveProb, negativeProb

    # 리뷰만 넣었을 때

    def probPositiveAndNegative(self, sentidata):
        positive = sum([int(float(row[-1])) for row in sentidata])
        numReviews = len(sentidata)
        negative = numReviews - positive
        positiveProb = float(positive) / float(numReviews)
        negativeProb = float(negative) / float(numReviews)
        return positiveProb, negativeProb

    # 단어 찾기
    def findUsedWords(self, sentidata, word, idx):
        # Return the index of the used words in 'idx'th review
        # idx번째 리뷰에 쓰인 단어들의 인덱스
        temp = [int(float(x)) for x in sentidata[idx][:-1]]
        idxUsedWords = [index for index, value in enumerate(temp) if value == 1]
        # Return the actual words in 'idx'th review
        # 실제 idx번째 리뷰의 단어들
        usedWords = [word[idx] for idx in idxUsedWords]
        return idxUsedWords, usedWords

    #분석 - 어떤 리뷰를 분석할건지 입력 - 단어들의 리스트 - 단어들마다 인덱스를 모으기
    # 어레이로 모여져 있고, 단어 하나하나에 대한 확률 계산하기

    def runAnalysis(self, sentidata, word, idxReview):
        probLogPositive = 0
        probLogNegative = 0
        idxUsedWords, usedWords = self.findUsedWords(sentidata, word, idxReview)

        # Make a for-loop to run from the first word to the last word
        # 첫 단어부터 끝 단어까지 forloop로 계산.
        for i in range(len(idxUsedWords)):
            # get the first word from the used word set
            idxWord = idxUsedWords[i]
            # calculate the word's probability to be positive or negative
            pointedWord, positive, negative = self.probWordPositiveAndNegative( sentidata ,word, idxWord )
            # 왜 log demension? adding multiplication..? 0.000000 .. 30번.. - 컴퓨터가 0으로 인식 - 로그로 변환 - 숫자로 인식
            probLogPositive += math.log(positive)
            probLogNegative += math.log(negative)

        # 이건 무슨 확률이지,,
        positiveProb1, negativeProb1 = self.probPositiveAndNegative(sentidata)
        probLogPositive += math.log(positiveProb1)
        probLogNegative += math.log(negativeProb1)

        if probLogPositive > probLogNegative:
            sentiment = 'Positive'
            print('Positive')
        else:
            sentiment = 'Negative'
            print('Negative')

        return probLogPositive, probLogNegative, sentiment

