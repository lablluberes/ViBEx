import pandas as pd

from .LoadNodes import LoadNodes
from .MutualInformationCalculation import MutualInformationCalculation
from .MIBNIUpateRules import MIBNIUpateRules

class Mibni():

    def __init__(self, maxK, textContent, modelFile):

        self.MODEL_FILE = modelFile
        self.allNodes = LoadNodes(textContent)
        self.nodes = self.allNodes.getNodes()
        self.nodeSize = self.allNodes.getNodeSize()
        self.nodeLength = self.allNodes.getNodeLength()
        self.maxK = min(maxK, self.nodeSize)


        self.mifs = MutualInformationCalculation(self.nodes, self.nodeSize, self.nodeLength)
        self.mifs.initializeTabularMI()
        self.dynamics = MIBNIUpateRules(self.allNodes)

        self.allRegulators = []
        self.regulatoryRules = []

        self.curPermutation = []
        self.curLogicFunction = []

        self.nodeNumbers = []

        for i in range(1, self.nodeSize+1):
            self.nodeNumbers.append(i)

        labels = textContent.columns

        dict_labels = {}

        for i in self.nodeNumbers:
            dict_labels[i] = labels[i-1]

        self.nodeLabels = dict_labels

    def run(self):
        regulators = []

        for i in range(1, self.nodeSize+1):
            targetGene = self.nodeNumbers[i-1]

            if(self.mifs.entropyCheckingOfATargetgene(targetGene) == 0):

                self.regulatoryRules.append(self.getRegulatoryRule(targetGene, None, None, 0, self.nodeLabels))
                continue

            regulators = []
         
            for k in range(1, self.maxK+1):
                #print("===================== K is :", k, "=====================")
                self.mifs.prepare()
                #print("Calling MIFS")
                self.mifs.executeFeatureSelection(i, k)
                regulators = self.mifs.getResult()
                #print("Calling SWAP")
                ers = self.swap(i-1, regulators)
                #print("Error:", ers)

                if ers == 0:
                    break

                #if k == 2: break
                #break # for debug  
            
            rule = self.getRegulatoryRule(targetGene, regulators, self.curPermutation, self.curLogicFunction, self.nodeLabels)
            self.regulatoryRules.append(rule)
            arr = [int(x) for x in regulators]
            self.allRegulators.append(arr)

            #break  # for debug 

        return self.regulatoryRules

    def getRegulatoryRule(self, targetGene, regulators, permutation, logicFunction, labels):

        rule = labels[targetGene] + " = "

        if(regulators != None):
            for i in range(len(permutation)):
                ch = permutation[i]

                if ch == '0':
                    rule = rule + "(" + labels[regulators[i]] + ")"
                
                else:
                    rule = rule + "(not " + labels[regulators[i]] + ")"

                if(i < len(permutation)-1):
                    if logicFunction == 1:
                        rule = rule + ' and '
                    else:
                        rule = rule + ' or '
        
        else:

            rule = rule + "(" + labels[targetGene] +")"

        return rule
    
    def getUnselected(self, regulators):
        unselected = []

        for i in range(self.nodeSize):
            target = self.nodeNumbers[i]

            if target not in regulators:
                unselected.append(target)

        return unselected
    
    def getSolutions(self, regulators):
        
        sols = [[0] * (self.allNodes.getNodeLength()-1) for _ in range(len(regulators))]
        
        for k in range(self.allNodes.getNodeLength()-1):
            for l in range(len(regulators)):
                sols[l][k] = self.nodes[regulators[l]-1][k]
        
        return sols
    

    def swap(self, targetIndex, regulators):

        unselected = self.getUnselected(regulators)

        target = []

        #print("targetIndex:", targetIndex)
        #print("regulators:", regulators)

        for j in range(1, self.allNodes.getNodeLength()):
            target.append(self.nodes[targetIndex][j])
        
        sols = self.getSolutions(regulators)

        #print("target:", target)
        #print("Sols:", sols[0])

        ret = self.dynamics.test(target, sols)

        minError = self.dynamics.calculateError(ret, targetIndex)

        #print("BEFORE FOR LOOP \n")

        #print("ret:", ret)
        #print("minError:", minError)

        error = 0

        permutation = self.dynamics.getPermutation()
        boolFunction = self.dynamics.getLogicFunction()

        #print("permutation:", permutation)
        #print("boolFunction:", boolFunction)

        for i in range(1, len(unselected)+1):
            for j in range(1, len(regulators)+1):

                wi = unselected[i-1]
                si = regulators[j-1]
               
                regulators[j-1] = wi
                unselected[i-1] =  si
                
                #print("\n")
                #print("Regulators:",regulators)
                sols = self.getSolutions(regulators)
                #print("Sols:", sols[0])

                ret = self.dynamics.test(target, sols)
                #print("ret:", ret)

                error = self.dynamics.calculateError(ret, targetIndex)
                
                #print("error:", error, "minError:", minError)

                if error is not None and error < minError:
                    minError = error
                    permutation = self.dynamics.getPermutation()
                    boolFunction = self.dynamics.getLogicFunction()
                else:
                    regulators[j-1] = si
                    unselected[i-1] = wi
            
                #break # debug
            #break # debug

        self.curPermutation = permutation
        self.curLogicFunction = boolFunction

        return minError



'''if __name__ == "__main__":

    data = {'lexA': [0, 1, 0, 1], 
                'uvrD': [0, 0, 1, 1], 
                'recA': [0, 1, 0, 0], 
                'uvrA': [1, 1, 1, 1], 
                'polB': [1, 0, 0, 0], 
                'umuD': [0, 0, 0, 0]}
    
    data = {'lexA': [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
            'uvrD': [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
            'recA': [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
            'uvrA': [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
            'polB': [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
            'umuD': [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}


    df = pd.DataFrame(data)

    

    a = Mibni(10, df, "dynamics.tsv")
    rules = a.run()

    print(rules)'''


