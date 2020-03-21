def checkBestPolicy(pnew, pold):
    if(pnew > pold):
        return True
    return False


threshold = -110 # dBm
def checkThresPolicy(pnew, pold):
    if(pnew > pold and pold < threshold):
        return True
    return False


entropy = 5 # dBm
def checkEntropyPolicy(pnew, pold):
    if(pnew > pold + entropy):
        return True
    return False


multiplier = 0.9 # parameter for my policy
pmin = -125
def checkMyPolicy(pnew, pold):
    if(pnew > pold * multiplier and pnew > pmin):
        return True
    return False

def checkPolicy(policy, pnew, pold):
    if(policy == 'best'):
        return checkBestPolicy(pnew, pold)
    elif(policy == 'thres'):
        return checkThresPolicy(pnew, pold)
    elif(policy == 'entropy'):
        return checkEntropyPolicy(pnew, pold)
    elif(policy == 'my'):
        return checkMyPolicy(pnew, pold)
