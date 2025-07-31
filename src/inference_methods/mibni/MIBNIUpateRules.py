

class MIBNIUpateRules():

    def getNodeSize(self):
        return self.nodeSize
    
    def setNodeSize(self, nodeSize):
        self.nodeSize = nodeSize
    
    def getFraser(self):
        return self.allNodes
    
    def setFraser(self, allNodes):
        self.allNodes = allNodes

    def getPermutation(self):
        return self.permutation
    
    def getLogicFunction(self):
        return self.logicFunction

    def __init__(self, allNodes):
        self.allNodes = allNodes
        self.nodeSize = allNodes.getNodeSize()
        self.permutation = None
        self.logicFunction = None

    
    def calculateError(self, result, indx):
        
        #print("---CALCULATE ERROR---")
        ret = 0

        nodes = self.allNodes.getNodes()
        #print("nodes:",nodes)

        originalNode = nodes[indx]
        #print('originalNode:', originalNode)

        reconstructedNode = result
        #print('reconstructedNode:', reconstructedNode)

        if reconstructedNode == None:

            return None #len(reconstructedNode)
        
        for j in range(len(reconstructedNode)):
                if reconstructedNode[j] != int(originalNode[j+1]):
                    ret += 1
        
        
        return ret


    def getTotalError(self, errs):

        noOfErrorBits = 0

        for i in range(len(errs)):
            noOfErrorBits += errs[i]

        
        return noOfErrorBits
    
    def calculateErrors(self, result):

        nodes = self.allNodes.getNodes()

        ret = []

        for i in range(len(nodes)):

            originalNode = nodes[i]
            reconstructedNode = result[i]

            if reconstructedNode == None:
                continue

            for j in range(len(reconstructedNode)):
                if reconstructedNode[j] != int(originalNode[j+1]):
                    ret[i] += 1

        return ret
    
    def binaryPermutation(self, dim):

        perms = []
        perms1 = []

        if dim == 0:
            return perms

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

    def test(self, target, solution):

        #print("\n--TEST FUNCTION DYNAMICS--\n")

        #print("solution length:",len(solution))

        perms = self.binaryPermutation(len(solution))

        #print("perms:", perms)

        ands = [[0] * len(target) for _ in range(len(perms))]
        ors = [[0] * len(target) for _ in range(len(perms))]

        cAnds = [0 for _ in range(len(perms))]
        cOrs = [0 for _ in range(len(perms))]

        for i in range(len(target)):
            for j in range(len(perms)):

                str_ = perms[j]

                for k in range(len(str_)):
                    if k == 0:
                        if str_[k] == "0":
                            ands[j][i] = solution[k][i]
                            ors[j][i] = solution[k][i]
                        
                        else:
                            ands[j][i] = solution[k][i]^1
                            ors[j][i] = solution[k][i]^1

                    else:
                        if str_[k] == "0":
                            ands[j][i] &= solution[k][i]
                            ors[j][i] |= solution[k][i]
                        
                        else:
                            ands[j][i] &= solution[k][i]^1
                            ors[j][i] |= solution[k][i]^1
                
                if target[i] == ands[j][i]:
                     cAnds[j] += 1
                
                if target[i] == ors[j][i]:
                    cOrs[j] += 1
        
        ret = None
        max = 0
        perm = ""
        logicFunction = 0

        for i in range(len(cAnds)):
            if cAnds[i] > max:
                max = cAnds[i]
                ret = ands[i]
                perm = perms[i]
                logicFunction = 1
        
        for i in range(len(cOrs)):
            if cOrs[i] > max:
                max = cOrs[i]
                ret = ors[i]
                perm = perms[i]
                logicFunction = 0
        
        self.permutation = perm
        self.logicFunction = logicFunction

        return ret

                