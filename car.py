import math

class Car():
    
    def setPrevIntersect(self, prevIntersect):
        self.prevIntersect = prevIntersect

    def setMovVectorFromCorner(self, newVector):
        self.movVector = newVector

    def setMovVector(self, dir):
        if(dir == 'left'):
            if(self.movVector == (1, 0)):
                self.movVector = (0, -1 )

            elif(self.movVector == ( -1, 0)):
                self.movVector = (0, 1)
            
            elif(self.movVector == ( 0, 1)):
                self.movVector = (1, 0)
            
            else:       # self.movVector = ( 0, -1 * velocity)
                self.movVector = (-1, 0)
        
        elif(dir == 'right'):
            if(self.movVector == (1, 0)):
                self.movVector = (0, 1)

            elif(self.movVector == ( -1 , 0)):
                self.movVector = (0, -1)
            
            elif(self.movVector == ( 0, 1)):
                self.movVector = ( -1 , 0)
            
            else:       # self.movVector = ( 0, -1 * velocity)
                self.movVector = ( 1, 0)

        
    def setInitMovVector(self):
        if(self.newCar == True):
            if("left_" in self.entrance):
                self.movVector = ( 1, 0)
            elif("right_" in self.entrance):
                self.movVector = ( -1, 0)
            elif("top_" in self.entrance):
                self.movVector = ( 0, 1)
            elif("bot_" in self.entrance):
                self.movVector = (0, -1)


    def setAttributes(self, prevIntersectPos):
        self.setPrevIntersect(prevIntersectPos)
        self.setInitMovVector()

    def setOldCar(self):
        self.newCar = False
    
    def setBestPower(self, power):
        self.bestPower = power
    
    def setBestBaseID(self, id):
        self.bestBaseID = id

    def setThresPower(self, power):
        self.thresPower = power
    
    def setThresBaseID(self, id):
        self.thresBaseID = id

    def setEntropyPower(self, power):
        self.entropyPower = power
    
    def setEntropyBaseID(self, id):
        self.entropyBaseID = id

    def setMyPower(self, power):
        self.myPower = power
    
    def setMyBaseID(self, id):
        self.myBaseID = id

    def setBaseID(self, policy, id):
        if(policy == 'best'):
            return self.setBestBaseID(id)
        if(policy == 'thres'):
            return self.setThresBaseID(id)
        if(policy == 'entropy'):
            return self.setEntropyBaseID(id)
        if(policy == 'my'):
            return self.setMyBaseID(id)

    def setPower(self, policy, power):
        if(policy == 'best'):
            return self.setBestPower(power)
        if(policy == 'thres'):
            return self.setThresPower(power)
        if(policy == 'entropy'):
            return self.setEntropyPower(power)
        if(policy == 'my'):
            return self.setMyPower(power)

    def setPos(self, pos):
        self.pos = pos

    def __init__(self, entranceName, power, baseID, pos=None):
        super().__init__()
        # self.obj = obj
        self.pos = pos
        self.newCar = True
        self.entrance = entranceName
        self.movVector = None
        self.prevIntersect = None
        self.bestBaseID = baseID
        self.thresBaseID = baseID
        self.entropyBaseID = baseID
        self.myBaseID = baseID
        self.bestPower = power
        self.thresPower = power
        self.entropyPower = power        
        self.myPower = power
        self.setAttributes(pos)

    def getPos(self):
        if(self.pos != None):
            return self.pos

    # def getObj(self):
    #     return self.obj

    def getPrevIntersect(self):
        return self.prevIntersect
    
    def getMovVector(self):
        return self.movVector

    def getBestPower(self):
        return self.bestPower
    
    def getBestBaseID(self):
        return self.bestBaseID

    def getThresPower(self):
        return self.thresPower
    
    def getThresBaseID(self):
        return self.thresBaseID

    def getEntropyPower(self):
        return self.entropyPower
    
    def getEntropyBaseID(self):
        return self.entropyBaseID

    def getMyPower(self):
        return self.myPower
    
    def getMyBaseID(self):
        return self.myBaseID

    def getPower(self, policy):
        if(policy == 'best'):
            return self.getBestPower()
        if(policy == 'thres'):
            return self.getThresPower()
        if(policy == 'entropy'):
            return self.getEntropyPower()
        if(policy == 'my'):
            return self.getMyPower()

    def getBaseID(self, policy):
        if(policy == 'best'):
            return self.getBestBaseID()
        if(policy == 'thres'):
            return self.getThresBaseID()
        if(policy == 'entropy'):
            return self.getEntropyBaseID()
        if(policy == 'my'):
            return self.getMyBaseID()