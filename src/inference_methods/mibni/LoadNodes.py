##############################################
# This code was converted from Java to Python based on Pusnik paper Java code: Pušnik, Ž., Mraz, M., Zimic, N., & Moškon, M. (2022). Review and assessment of Boolean approaches for inference of gene regulatory networks. Heliyon, 8(8).
#
# Barman and Kwon, the creaters of MIBNI, provided the Java code to Pusnik
# This is the paper of Barman about MIBNI: Barman, S., & Kwon, Y. K. (2017). A novel mutual information-based Boolean network inference method from time-series gene expression data. PloS one, 12(2), e0171097.
#
#
##############################################

# Following comment was in the Java code that we obtained from Pusnik
'''/**
 * @author Shohag Barman
 * Combined Master's and PhD student
 * Complex Systems Computing Lab, Ulsan university, South Korea.
 *
 */'''


import pandas as pd

class LoadNodes():
    
    #tabularMI = None 
    #nodes = []  
    #atributos = []
    #atributosInteger = []    
    #nodeLength = 0    
    #data = []         
    #nodeSize = 0

    def getAtributosInteger(self):
        return self.atributosInteger
    
    def setNodeSize(self, nodeSize):
        self.nodeLength = nodeSize

    def getNodes(self):
        return self.nodes
    
    def getNodeSize(self):
        if self.nodes != []:
            return len(self.nodes)
        else: return -1

    def getNodeLength(self):
        return self.nodeLength
    
    def setNodeLength(self, nodeLength):
        self.nodeLength = nodeLength

    def __init__(self, textContent):
        self.tabularMI = []
        self.nodes = []
        self.nodeLength = 0
        self.data = []


        self.atributos = []
        self.atributosInteger = []

        nodes = []

        self.addNodes(textContent)
        self.nodeSize = self.getNodeSize()

    
    def addNodes(self, textContent):
        
        data = list(textContent.values)

        line = None
   

        self.nodeLength = len(data)

        noOfNodes = len(data[0])

        for i in range(noOfNodes):
            nodevals = []
            self.nodes.append(nodevals)

        for i in range(self.nodeLength):
           
            for j in range(noOfNodes):
                self.nodes[j].append(data[i][j])

        #print(self.nodes)




'''if __name__ == "__main__":

    data = {'lexA': [0, 1, 0, 1], 
                'uvrD': [0, 0, 1, 1], 
                'recA': [0, 1, 0, 0], 
                'uvrA': [1, 1, 1, 1], 
                'polB': [1, 0, 0, 0], 
                'umuD': [0, 0, 0, 0]}

    df = pd.DataFrame(data)

    print(df)

    a = list(df.values)

    print(a[0])'''

