##############################################
# This code was converted from Java to Python based on Pusnik paper Java code: Pušnik, Ž., Mraz, M., Zimic, N., & Moškon, M. (2022). Review and assessment of Boolean approaches for inference of gene regulatory networks. Heliyon, 8(8).
#
# Barman and Kwon, the creaters of MIBNI, provided the Java code to Pusnik
# This is the paper of Barman about MIBNI: Barman, S., & Kwon, Y. K. (2017). A novel mutual information-based Boolean network inference method from time-series gene expression data. PloS one, 12(2), e0171097.
#
#
##############################################


# Following comment was in the Java code that we obtained from Pusnik
'''/*********************************************************************************************
 * This program is based on the paper "A novel mutual information-based Boolean network      *
 * inference method from time-series gene expression data." PloS one 12.2 (2017): e0171097.  *
 * This program generates the 2^|s+1| conjunction and disjunction update rules and           *
 * calculates the gene-wise dynamics consistency which will be used in SWAP.                 *
 *                                                                                           *
 * N.B: Initial states are same for both observed variable, v(t) and predicted variable v'(t)*
 *                                                                                           *
 *                                                                                           *
 * @author Shohag Barman                                                                     *
 * 						                                                                     *
 * Combined Master's and PhD student                                                         *
 * Complex Systems Computing Lab, Ulsan university, South Korea.                             *
 *                                                                                           *
 ********************************************************************************************/'''

import math

class MutualInformationCalculation():

    def getfeaturesInteger(self):
        return self.featuresInteger
    
    def setNodeSize(self, nodeSize):
        self.nodeSize = nodeSize

    def getNodes(self):
        return self.nodes
    
    def getNodesLength(self):
        return self.nodeLength
    
    def setNodeLength(self, nodeLength):
        self.nodeLength = nodeLength

    def getData(self):
        return self.data

    def setData(self, data):
        self.data = data

    def getfeatures(self):
        return self.features

    def setfeatures(self, features):
        self.features = features

    def __init__(self, nodes, nodeSize, nodeLength):
        
        self.setfeatures([])
        self.featuresInteger = []

        self.nodes = nodes
        self.nodeLength = nodeLength
        self.nodeSize = nodeSize

        self.setF = []
        self.setS = []
        self.setAS = []

        self.data = []

        self.tabularMI = [[] for i in range(self.nodeSize)]
        self.tabularMI2 = [[] for i in range(self.nodeSize)]

        self.quantidadeDefeatures = 0


    def prepare(self):

        self.setF = []
        self.setS = []
        self.setAS = []

        self.initializeSetF()
        self.initializeTabularMI()

    def initializeSetF(self):

        self.quantidadeDefeatures = len(self.getfeaturesInteger())

        for i in range(self.nodeSize):
            self.setF.append(i)

    def initializeTabularMI(self):

        for i in range(self.nodeSize):
            for j in range(self.nodeSize):
                self.tabularMI[i].append(-1.00)
                self.tabularMI2[i].append(-1.00)

    def getResult(self):

        r = []

        for i in self.setS:
            r.append(i+1)

        return r
    
    def executeFeatureSelection(self, targetGene, k):

        entropyValue = 0

        #if len(self.setF) == 0:
            #print("Not prepared. Prepare first")
        
        for i in range(self.nodeSize):
            for j in range(self.nodeSize):
                if i != j:
                    self.tabularMI[i][j] = self.calculatePairwiseMutualInformation(i, j)
                    self.tabularMI2[i][j] = self.calculatePairwiseMutualInformation(i, j)

        
        #print("\n")

        if k == 0:
            return
        
        entropyValue = self.entropyCheckingOfATargetgene(targetGene)

        if entropyValue == 0:
            return
        
        featureMax = self.getMax_MI_features(targetGene - 1)
        self.setF.remove(featureMax)
        self.setS.append(featureMax)

        while(len(self.setS) < k):

            featureMax = self.getMax_MI_features1()
          
            self.setF.remove(featureMax)
            self.setS.append(featureMax)

        for i in range(1, k):
            featureMax = self.getNextMax(targetGene - 1)
            self.setAS.append(featureMax)

    
    def getMax_MI_features(self, index):
        iMax = -1
        valorMax = -1

        for i in range(self.nodeSize):
            if valorMax < self.tabularMI[index][i]:
                valorMax = self.tabularMI[index][i]
                iMax = i

        return iMax

    def getMax_MI_features1(self):
        iMax = -1
        valorMax = -1

        for index in self.setS:
            for i in self.setF:
                
                if valorMax < self.tabularMI2[index][i]:
                    valorMax = self.tabularMI2[index][i]
                    iMax = i

        

        return iMax
    
    def getNextMax(self, index):
        iMax = -1
        valorMax = -1

        for i in range(self.nodeSize):
            found = False

            for s in self.setS:
                if int(s) == i:
                    found = True
                    continue
            
            if found:
                continue

            for s in self.setAS:
                if int(s) == i:
                    found = True
                    continue
            
            if found:
                continue

            if valorMax < self.tabularMI[index][i]:
                valorMax = self.tabularMI[index][i]
                iMax = i
        
        return iMax

    def entropyCheckingOfATargetgene(self, x):
        entropy = 0

        m = x-1

        s = self.nodes[m]

        firstVector = []
        tmp = []

        for i in range(self.nodeLength-1):
            firstVector.append(s[i+1])
        
        tmp.append(firstVector)
        
        entropy = self.getEntropy(tmp)

        return entropy
    
    def calculatePairwiseMutualInformation(self, x, y):

        mutualInformation = 0
        s = self.nodes[x]
        q = self.nodes[y]

        firstVector = []
        secondVector = []

        tmp = []

        for i in range(self.nodeLength-1):

            firstVector.append(s[i+1])
            secondVector.append(q[i])

        tmp.append(firstVector)
        tmp.append(secondVector)

        mutualInformation = self.getMutualInformation(tmp)    

        return mutualInformation

    def getEntropy(self, value):
        perm = self.binaryPermutation(len(value))

        occurance = {}

        for s in perm:
            occurance[s] = 0

        data = []
        rvar = value[0]

        for v in rvar:
            data.append(""+str(v))

        for i in range(1, len(value)):
            rvar = value[i]

            for j in range(len(rvar)):
                t = data[j]
                data.pop(j)
              
                t += str(rvar[j])
                data.insert(j, t)
        
        for str_ in data:
            occurance[str_] = occurance[str_] + 1

        result = 0

        for s in perm:

            p = occurance[s]/len(data)

            result -= 0 if (occurance[s] == 0) else (p * math.log(p) / math.log(2))

        
        return result
    
    def getMutualInformation(self, value):
        mutualInformation = 0.0

        mutualInformation -= self.getEntropy(value)
        mutualInformation += self.getEntropy(value[0:1])
        mutualInformation += self.getEntropy(value[1:len(value)])

        return mutualInformation


    def binaryPermutation(self, dim):
        perms = []
        perms1 = []

        perms.append("0")
        perms.append("1")

        for i in range(1, dim):
            for str_ in perms:
                perms1.append(str_+"0")
                perms1.append(str_+"1")
            
            perms.clear()
            perms.extend(perms1)
            perms1.clear()

        
        return perms