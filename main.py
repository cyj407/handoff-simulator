import tkinter as tk
import time
import datetime
import math
import random
import car
import policy
import numpy as np
import matplotlib.pyplot as plt

# delta = 10
p_lambda = 1/30 #1/30 # every 30 secs per cars
poisson_1sec = p_lambda * math.exp(-1*p_lambda) # 0.03224053668273353
E = 5 # dBm
T = -110 # dBm
multiplier = 0.9 # parameter for my policy
base = 1
p0 = -50 #dBm
p1 = p0 - 10
Pmin = -125 #dBm

grid_num = 4
grid_dis = 750
velocity = 10
p_init = p1 - 20 * math.log(grid_dis/base, 10)     #  -103.52182518111363 

bestPolicy_handoff = 0
thresPolicy_handoff = 0
entropyPolicy_handoff = 0
myPolicy_handoff = 0

base_station = [ 
                [grid_dis, grid_dis],   # top_left
                [grid_dis*3, grid_dis],  # top_right
                [grid_dis, grid_dis*3],  # bot_left
                [grid_dis*3, grid_dis*3]  # bot_right
        ]

entrance = {
                'left_top':  [ 0, grid_dis*1],
                'left_mid':  [ 0, grid_dis*2],
                'left_bot':  [ 0, grid_dis*3],
                'top_left':  [grid_dis*1, 0],
                'top_mid':   [grid_dis*2, 0],
                'top_right': [grid_dis*3, 0],
                'right_top': [grid_dis*grid_num, grid_dis*1],
                'right_mid': [grid_dis*grid_num, grid_dis*2],
                'right_bot': [grid_dis*grid_num, grid_dis*3],
                'bot_left':  [grid_dis*1, grid_dis*grid_num],
                'bot_mid':   [grid_dis*2, grid_dis*grid_num],
                'bot_right': [grid_dis*3, grid_dis*grid_num]
        }

entrance_point = [ 
                [ 0, grid_dis*1],
                [ 0, grid_dis*2],
                [ 0, grid_dis*3],
                [grid_dis*1, 0],
                [grid_dis*2, 0],
                [grid_dis*3, 0],
                [grid_dis*grid_num, grid_dis*1],
                [grid_dis*grid_num, grid_dis*2],
                [grid_dis*grid_num, grid_dis*3],
                [grid_dis*1, grid_dis*grid_num],
                [grid_dis*2, grid_dis*grid_num],
                [grid_dis*3, grid_dis*grid_num]
        ]

corner_point = [ 
                 [0, 0],            # left_top
                 [grid_dis*grid_num, 0],           # right_top
                 [0, grid_dis*grid_num],           # left_bottom
                 [grid_dis*grid_num, grid_dis*grid_num]           # right_bottom
        ]

intersect_point = [ 
                    [grid_dis*1, grid_dis*1],         # top_left
                    [grid_dis*2, grid_dis*1],        # top_middle
                    [grid_dis*3, grid_dis*1],        # top_right
                    [grid_dis*1, grid_dis*2],        # middle_left
                    [grid_dis*2, grid_dis*2],       # middle_middle
                    [grid_dis*3, grid_dis*2],       # middle_right
                    [grid_dis*1, grid_dis*3],        # bottom_left
                    [grid_dis*2, grid_dis*3],       # bottom_middle
                    [grid_dis*3, grid_dis*3]        # bottom_right
        ]

dir_possibility = [ 'straight', 'straight', 'straight', 'right', 'right', 'left']

# record the car on the board
mobility_list = []
deleteIndex = []

def checkEntrance(car, pos):
    for i in range(len(entrance_point)):
        if(entrance_point[i] == pos):
            next_dir = random.choice(dir_possibility)
            if(next_dir == 'straight'):
                if(car.getMovVector() == ( -1, 0) and i < 3):              # left entrances
                    deleteIndex.append(mobility_list.index(car))
                elif(car.getMovVector() == ( 0, -1) and i < 6 and i >= 3):    # top entrances
                    deleteIndex.append(mobility_list.index(car))
                elif(car.getMovVector() == ( 1, 0) and i < 9 and i >= 6):         # right entrances
                    deleteIndex.append(mobility_list.index(car))
                elif(car.getMovVector() == ( 0, 1) and i >= 9):                  # bottom entrances
                    deleteIndex.append(mobility_list.index(car))
                else:
                    car.setPrevIntersect(entrance_point[i])
                    new_x = car.getPos()[0] + car.movVector[0] * velocity
                    new_y = car.getPos()[1] + car.movVector[1] * velocity
                    car.setPos([new_x, new_y])

            elif(next_dir == 'left'):
                if(car.getMovVector() == ( 0, -1) and i < 3):              # left entrances
                    deleteIndex.append(mobility_list.index(car))
                elif(car.getMovVector() == ( 1, 0) and i < 6 and i >= 3):    # top entrances
                    deleteIndex.append(mobility_list.index(car))
                elif(car.getMovVector() == ( 0, 1) and i < 9 and i >= 6):         # right entrances
                    deleteIndex.append(mobility_list.index(car))
                elif(car.getMovVector() == ( -1, 0) and i >= 9):                  # bottom entrances
                    deleteIndex.append(mobility_list.index(car))
                else:
                    car.setMovVector(next_dir)
                    car.setPrevIntersect(entrance_point[i])
                    new_x = car.getPos()[0] + car.movVector[0] * velocity
                    new_y = car.getPos()[1] + car.movVector[1] * velocity
                    car.setPos([new_x, new_y])
         
            elif(next_dir == 'right'):
                if(car.getMovVector() == ( 0, 1) and i < 3):              # left entrances
                    deleteIndex.append(mobility_list.index(car))
                elif(car.getMovVector() == ( -1, 0) and i < 6 and i >= 3):    # top entrances
                    deleteIndex.append(mobility_list.index(car))
                elif(car.getMovVector() == ( 0, -1) and i < 9 and i >= 6):         # right entrances
                    deleteIndex.append(mobility_list.index(car))
                elif(car.getMovVector() == ( 1, 0) and i >= 9):                  # bottom entrances
                    deleteIndex.append(mobility_list.index(car))
                else:
                    car.setMovVector(next_dir)
                    car.setPrevIntersect(entrance_point[i])
                    new_x = car.getPos()[0] + car.movVector[0] * velocity
                    new_y = car.getPos()[1] + car.movVector[1] * velocity
                    car.setPos([new_x, new_y])
            return True
    return False

def checkCorner(car, pos):
    if(pos == corner_point[0]):
        if(car.getMovVector() == ( 0, -1)):
            car.setMovVectorFromCorner((1, 0))
        else:
            car.setMovVectorFromCorner((0, 1))
    elif(pos == corner_point[1]):
        if(car.getMovVector() == ( 0, -1)):
            car.setMovVectorFromCorner((-1, 0))
        else:
            car.setMovVectorFromCorner((0, 1))
    elif(pos == corner_point[2]):
        if(car.getMovVector() == ( 0, 1)):
            car.setMovVectorFromCorner((1, 0))
        else:
            car.setMovVectorFromCorner((0, -1))
    elif(pos == corner_point[3]):
        if(car.getMovVector() == ( 0, 1)):
            car.setMovVectorFromCorner((-1, 0))
        else:
            car.setMovVectorFromCorner((0, -1))
    else:
        return False
    return True

def checkIntersect(car, pos):
    for i in range(0, len(intersect_point)):
        if(pos == intersect_point[i]):
            next_dir = random.choice(dir_possibility)
            if(next_dir == 'straight'):
                car.setPrevIntersect(intersect_point[i])
            else:           # next_dir = right or left
                car.setMovVector(next_dir)        
                car.setPrevIntersect(intersect_point[i]) 
            new_x = car.getPos()[0] + car.movVector[0] * velocity
            new_y = car.getPos()[1] + car.movVector[1] * velocity
            car.setPos([new_x, new_y])       
            return True
    return False    

def moveCar():
    for car in mobility_list:
        pos = car.getPos()

        if(car.newCar == True):
            new_x = car.getPos()[0] + car.movVector[0] * velocity
            new_y = car.getPos()[1] + car.movVector[1] * velocity
            car.setPos([new_x, new_y])
            car.setOldCar()
            continue
        
        if(checkEntrance(car, pos)):
            continue
        elif(checkIntersect(car, pos)):
            continue
        elif(checkCorner(car, pos)): 
            new_x = car.getPos()[0] + car.movVector[0] * velocity
            new_y = car.getPos()[1] + car.movVector[1] * velocity
            car.setPos([new_x, new_y])        
            continue
        else:
            new_x = car.getPos()[0] + car.movVector[0] * velocity
            new_y = car.getPos()[1] + car.movVector[1] * velocity
            car.setPos([new_x, new_y])    

fill_color = [ "red", "yellow", "green", "pink", "orange", "blue", "purple", "brown"]

def setInitBase(loc):
    if(loc == "top_left" or loc == "left_top" or loc == "left_mid"):
        return 0
    elif(loc == "top_mid" or loc == "top_right" or loc == "right_top"):
        return 1
    elif(loc == "left_bot" or loc == "bot_left" or loc == "bot_mid"):
        return 2
    elif(loc == "bot_right" or loc == "right_mid" or loc == "right_bot"):
        return 3

def plotCar():
    for key, value in entrance.items():
        n = random.randint(1, 101)
        if(n < poisson_1sec * 100):
            # set initial base station
            base_id = setInitBase(key)
            new_car = car.Car( key, None, p_init, base_id, value)
            mobility_list.append(new_car)

def deleteCar():
    # remove index in decreasing order
    global mobility_list
    global deleteIndex
    deleteIndex.sort(reverse=True)
    for delIdx in deleteIndex:
        delete = mobility_list.pop(delIdx)
        del delete        
    deleteIndex = []

def getDistance(p1x, p1y, p2x, p2y):
    return (math.sqrt(math.pow(p1x - p2x, 2) + math.pow(p1y - p2y, 2)))

def calPower(dis):
    return (p1 - 20 * math.log(dis/base, 10))

def calSumOfPower():
    global sum_of_best_power, sum_of_thres_power, sum_of_entropy_power, sum_of_my_power, total_car
    total_car = total_car + len(mobility_list)
    for car in mobility_list:
        sum_of_best_power = sum_of_best_power + car.getBestPower()
        sum_of_thres_power = sum_of_thres_power + car.getThresPower()
        sum_of_entropy_power = sum_of_entropy_power + car.getEntropyPower()
        sum_of_my_power = sum_of_my_power + car.getMyPower()

def updateHandoff(policy):
    global bestPolicy_handoff, thresPolicy_handoff, entropyPolicy_handoff, myPolicy_handoff
    if(policy == 'best'):
        bestPolicy_handoff = bestPolicy_handoff + 1
    elif(policy == 'thres'):
        thresPolicy_handoff = thresPolicy_handoff + 1
    elif(policy == 'entropy'):
        entropyPolicy_handoff = entropyPolicy_handoff + 1
    elif(policy == 'my'):
        myPolicy_handoff = myPolicy_handoff + 1

def updatePower(policyStr):
    for car in mobility_list:
        pos = car.getPos()
        
        old_id = car.getBaseID(policyStr)
        old_signal_dis = getDistance(pos[0], pos[1], base_station[old_id][0], base_station[old_id][1])
        
        old_signal_power = p0
        if(old_signal_dis != 0):
            old_signal_power = calPower(old_signal_dis)

        new_id = old_id
        new_signal_dis = old_signal_dis

        for i in range(len(base_station)):
            tmp_dis = getDistance(pos[0], pos[1], base_station[i][0], base_station[i][1])
            if(tmp_dis < new_signal_dis):
                new_signal_dis = tmp_dis
                new_id = i
        
        new_signal_power = p0
        if(new_signal_dis != 0):
            new_signal_power = calPower(new_signal_dis)

        if(new_id == old_id):
            car.setPower(policyStr, new_signal_power)
        else:
            if(policy.checkPolicy(policyStr, new_signal_power, old_signal_power)):
                updateHandoff(policyStr)
                car.setPower(policyStr, new_signal_power)
                car.setBaseID(policyStr, new_id)
            else:
                car.setPower(policyStr, old_signal_power)
                car.setBaseID(policyStr, old_id)
        # print( 'baseid: %d, old: %f, new: %f' % (car.getBaseID(policyStr), new_signal_power, old_signal_power))
            # print( 'policy: %s, baseid: %d' % (policyStr, car.getBaseID(policyStr)))

bestPolicy_List = []
thresPolicy_List = []
entropyPolicy_List = []
myPolicy_List = []
sum_of_best_power = 0
sum_of_thres_power = 0
sum_of_entropy_power = 0
sum_of_my_power = 0

total_car = 0
# run 86400 times
count = 86400
for i in range(count, 0, -1):

    calSumOfPower()

    # move the cars on the canvas and remove exiting cars
    moveCar()
    deleteCar()

    updatePower("best")
    updatePower("thres")
    updatePower("entropy")
    updatePower("my")
    
    bestPolicy_List.append(bestPolicy_handoff)
    thresPolicy_List.append(thresPolicy_handoff)
    entropyPolicy_List.append(entropyPolicy_handoff)
    myPolicy_List.append(myPolicy_handoff)

    # plot new cars
    plotCar()

print("Average power of Best Policy: %f" % (sum_of_best_power/total_car))
print("Average power of Threshold Policy: %f" % (sum_of_thres_power/total_car))
print("Average power of Entropy Policy: %f" % (sum_of_entropy_power/total_car))
print("Average power of My Policy: %f" % (sum_of_my_power/total_car))

# Plot the figure
plt.figure()

x = np.linspace(0, count, num=count)

plt.plot( x, bestPolicy_List, 's',label="Best Policy",color="green")
plt.plot( x, thresPolicy_List, '^',label="Threshold Policy", color="red")
plt.plot( x, entropyPolicy_List, '.',label="Entropy Policy", color="blue")
plt.plot( x, myPolicy_List, label="My Policy", color="brown")

plt.xlabel("Time(sec)")
plt.ylabel("Number")
plt.title("Handoff")
plt.xlim( 0, 86400)
plt.legend()
plt.show()