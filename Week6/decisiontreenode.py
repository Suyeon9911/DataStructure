import csv
import math
from voterecord import *

class Node:

    def __init__(self,records):
        self.blnSplit = False
        self.children = {}
        self.records = records
        self.decisionAttribute = -1
        self.stat = {}
        for type in Record.types:
            self.stat[type] = 0
            for record in records:
                if record.party == type:
                    self.stat[type] = self.stat[type] + 1

    def __str__(self):
        if self.blnSplit == True:
            ret = 'Feature '+str(self.decisionAttribute)+ '('+str(self.stat)+')' + '\n'
            for key in self.children.keys():
                ret = ret + '---- key : '+str(key)+ ' ' +str(self.children[key])
        else:
            ret = str(self.stat) + '\n'
        return ret
    # 4
    def splitNode(self):
        self.blnSplit = True
        gains = self.calculateInformationGainPerFeatures()
        idxMaxGainFeature = -1
        maxGain = -999999999999999999.0
        # max 값
        for itr in range(len(gains)):
            if gains[itr] > maxGain :
                maxGain = gains[itr]
                idxMaxGainFeature = itr

        for value in Record.values:
            childRecords = []
            for record in self.records:
                if record.feature[idxMaxGainFeature] == value:
                    childRecords.append(record)
            self.children[value] = Node(childRecords)
        self.decisionAttribute = idxMaxGainFeature
        return self.children
    # 3
    def calculateInformationGainPerFeatures(self):
        gains = []
        entropyClass = self.calculateClassEntropy()
        for itr in range(Record.numValues):
            entropyConditional = self.calculateConditionalEntropy(itr)
            gains.append( entropyClass - entropyConditional )
        return gains

    # 1
    def calculateClassEntropy(self):
        entropy = 0.0
        for type in Record.types:
            cnt = 0.0
            for record in self.records:
                if record.party == type:
                    cnt = cnt + 1.0
            size = float(len(self.records))
            prob = float( cnt / size )  # 확률
            entropy = entropy - prob * math.log(prob,2)
        return entropy

    # 2
    def calculateConditionalEntropy(self,idxFeature):
        entropy = 0.0
        for value in Record.values:
            for type in Record.types:
                cntFeature = 0.0
                cntFeatureAndClass = 0.0
                for record in self.records:
                    if record.feature[idxFeature] == value:
                        cntFeature = cntFeature + 1
                        if record.party == type:
                            cntFeatureAndClass = cntFeatureAndClass + 1.0
                size = float(len(self.records))
                probFeature = cntFeature / size + 0.000001
                probFeatureAndClass = cntFeatureAndClass / size + 0.000001
                entropy = entropy + probFeatureAndClass * math.log(probFeature/probFeatureAndClass,2)
        return entropy

if __name__ == "__main__":
    csvfile = open('house-votes-84.csv','rt')
    reader = csv.reader(csvfile,delimiter=',')
    records = []

    for row in reader:
        record = Record(row)
        print (record)
        records.append(record)

    node = Node(records)
    print(node)
    node.splitNode()
    print(node)