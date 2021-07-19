from PlanNode import PlanNode

import matplotlib.pyplot as plt
import numpy as np
class ProductionList():
    def __init__(self, Filename):

        self.nodeHead = PlanNode(-1, '', '', '', '', '', '', '')
        self.nodeTail = PlanNode(-1, '', '', '', '', '', '', '')

        # Problem 2. setup the node relations between the nodeTail and nodeHead in
        # 헤드노드와 테일 노드의 노드 관계 설정
        # the properties. Use setNextNode and setPrevNode method of
        # the nodes
        # 원형으로 연결된 구조이기 때문에 -> 헤드와 테일 연결

        self.nodeHead.setNextNode(self.nodeTail)
        self.nodeTail.setPrevNode(self.nodeHead)

        f = open(Filename)
        temp = f.readlines()
        f.close()

        dataset = []
        for row in temp:
            dataset.append(row[:-1].split(','))
        Dataset = np.asarray(dataset[1:]).T

        numNos = Dataset[0].astype('int')
        strSerialNumbers = Dataset[1].astype('str')
        strModels = Dataset[2].astype('str')
        numModelNumbers = Dataset[3].astype('int')
        dateStart = Dataset[4].astype('str')
        numAssemblyOrders = Dataset[5].astype('int')
        dateEnd = Dataset[6].astype('str')
        strOrderOrigins = Dataset[7].astype('str')

        for i in range(len(numNos)):
            node = PlanNode(numNos[i], strSerialNumbers[i], strModels[i], numModelNumbers[i], dateStart[i],
                            numAssemblyOrders[i], dateEnd[i], strOrderOrigins[i])
            node.printOut()
            self.addLast(node)

        self.showPlanChart()

    def addLast(self, node):
        # Problem 3. complete the method to add the node in the parameter to the
        # last of the linked list. The tail should be always at the
        # last, so the node in the parameter should be the previous
        # node of the tail

        # 링크드 리스트의 마지막에 파라미터로 받은 노드를 추가 . 테일노드는 항상 마지막
        # 파라미터로 받은 노드는 항상 테일노드의 이전 노드임을 설정
        nodeLast = self.nodeTail.getPrevNode()
        nodeLast.setNextNode(node)
        node.setNextNode(self.nodeTail)
        node.setPrevNode(nodeLast)
        self.nodeTail.setPrevNode(node)
        # 노드라스트 변수에 테일 노드의 이전노드 저장.
        # 노드라스트의 넥스트 노드는 추가한 노드
        # 추가한 노드의 넥스트 노드는 테일노드
        # 추가한 노드의 이전 모드는 라스트노드
        # 테일 노드의 이전 노드는 추가한 노드


    def showPlanChart(self):

        allStartDate = []
        allModel = []
        node = self.nodeHead

        # Problem 4. iterate from nodeHead to nodeTail to retrieve the
        # start data and the model of all plan nodes.
        # 헤드 노드와 테일 노드로 반복하여 시작데이터와 모든 플랜노드들의 모델을 검색?
        # 테일노드까지 와일문으로 반복 -> 넥스트 노드로 옮겨가면서
        while node.getNextNode() != self.nodeTail:
            node = node.getNextNode()
            allStartDate.append(node.dateStart)
            allModel.append(node.strModel)

        plt.figure(1)
        plt.subplot(211)
        Uniq_allModel = list(set(allModel))
        Counting_allModel = [allModel.count(a) for a in Uniq_allModel]
        xlabel = [i for i in range(len(Uniq_allModel))]
        plt.bar(xlabel[0:10], Counting_allModel[0:10], align='center')
        plt.xticks(xlabel[0:10], Uniq_allModel[0:10])
        plt.xlabel('Model')
        plt.ylabel('Number of Orders')

        plt.subplot(212)
        Uniq_allStartDate = list(set(allStartDate))
        Counting_dateStart = [allStartDate.count(a) for a in Uniq_allStartDate]
        xlabel = [i for i in range(len(Uniq_allStartDate))]
        plt.bar(xlabel[0:10], Counting_dateStart[0:10], align='center')
        plt.xticks(xlabel[0:10], Uniq_allStartDate[0:10])
        plt.xlabel('Date')
        plt.ylabel('Number of Orders')
        plt.show()