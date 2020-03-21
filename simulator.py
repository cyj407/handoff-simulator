import tkinter as tk
import time
import datetime
import math
import random
import car
import policy

# default time = 1 day
countdown_time = 86400

delta = 10
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
car_size = 3

real_grid_dis = 750
grid_dis = 150
real_velocity = 10  # 250 for test
velocity = grid_dis/real_grid_dis * real_velocity

p_init = p1 - 20 * math.log(grid_dis/base, 10)     #  -103.52182518111363 

bestPolicy_handoff = 0
thresPolicy_handoff = 0
entropyPolicy_handoff = 0
myPolicy_handoff = 0

base_station = [ 
                [grid_dis+delta, grid_dis+delta],   # top_left
                [grid_dis*(grid_num-1)+delta, grid_dis+delta],  # top_right
                [grid_dis+delta, grid_dis*(grid_num-1)+delta],  # bot_left
                [grid_dis*(grid_num-1)+delta, grid_dis*(grid_num-1)+delta]  # bot_right
        ]

entrance = {
                'left_top':  [-car_size+delta, grid_dis*1-car_size+delta, car_size+delta, grid_dis*1+car_size+delta],
                'left_mid':  [-car_size+delta, grid_dis*2-car_size+delta, car_size+delta, grid_dis*2+car_size+delta],
                'left_bot':  [-car_size+delta, grid_dis*3-car_size+delta, car_size+delta, grid_dis*3+car_size+delta],
                'top_left':  [grid_dis*1-car_size+delta, -car_size+delta, grid_dis*1+car_size+delta, car_size+delta],
                'top_mid':   [grid_dis*2-car_size+delta, -car_size+delta, grid_dis*2+car_size+delta, car_size+delta],
                'top_right': [grid_dis*3-car_size+delta, -car_size+delta, grid_dis*3+car_size+delta, car_size+delta],
                'right_top': [grid_dis*grid_num-car_size+delta, grid_dis*1-car_size+delta, grid_dis*grid_num+car_size+delta, grid_dis*1+car_size+delta],
                'right_mid': [grid_dis*grid_num-car_size+delta, grid_dis*2-car_size+delta, grid_dis*grid_num+car_size+delta, grid_dis*2+car_size+delta],
                'right_bot': [grid_dis*grid_num-car_size+delta, grid_dis*3-car_size+delta, grid_dis*grid_num+car_size+delta, grid_dis*3+car_size+delta],
                'bot_left':  [grid_dis*1-car_size+delta, grid_dis*grid_num-car_size+delta, grid_dis*1+car_size+delta, grid_dis*grid_num+car_size+delta],
                'bot_mid':   [grid_dis*2-car_size+delta, grid_dis*grid_num-car_size+delta, grid_dis*2+car_size+delta, grid_dis*grid_num+car_size+delta],
                'bot_right': [grid_dis*3-car_size+delta, grid_dis*grid_num-car_size+delta, grid_dis*3+car_size+delta, grid_dis*grid_num+car_size+delta]
        }

# 12 entrances
entrance_point = [ 
                [-car_size+delta, grid_dis*1-car_size+delta, car_size+delta, grid_dis*1+car_size+delta],
                [-car_size+delta, grid_dis*2-car_size+delta, car_size+delta, grid_dis*2+car_size+delta],
                [-car_size+delta, grid_dis*3-car_size+delta, car_size+delta, grid_dis*3+car_size+delta],
                [grid_dis*1-car_size+delta, -car_size+delta, grid_dis*1+car_size+delta, car_size+delta],
                [grid_dis*2-car_size+delta, -car_size+delta, grid_dis*2+car_size+delta, car_size+delta],
                [grid_dis*3-car_size+delta, -car_size+delta, grid_dis*3+car_size+delta, car_size+delta],
                [grid_dis*grid_num-car_size+delta, grid_dis*1-car_size+delta, grid_dis*grid_num+car_size+delta, grid_dis*1+car_size+delta],
                [grid_dis*grid_num-car_size+delta, grid_dis*2-car_size+delta, grid_dis*grid_num+car_size+delta, grid_dis*2+car_size+delta],
                [grid_dis*grid_num-car_size+delta, grid_dis*3-car_size+delta, grid_dis*grid_num+car_size+delta, grid_dis*3+car_size+delta],
                [grid_dis*1-car_size+delta, grid_dis*grid_num-car_size+delta, grid_dis*1+car_size+delta, grid_dis*grid_num+car_size+delta],
                [grid_dis*2-car_size+delta, grid_dis*grid_num-car_size+delta, grid_dis*2+car_size+delta, grid_dis*grid_num+car_size+delta],
                [grid_dis*3-car_size+delta, grid_dis*grid_num-car_size+delta, grid_dis*3+car_size+delta, grid_dis*grid_num+car_size+delta]
        ]

corner_point = [ 
                 [-car_size+delta, -car_size+delta, car_size+delta, car_size+delta],            # left_top
                 [grid_dis*grid_num-car_size+delta, -car_size+delta, grid_dis*grid_num+car_size+delta, car_size+delta],           # right_top
                 [-car_size+delta, grid_dis*grid_num-car_size+delta, car_size+delta, grid_dis*grid_num+car_size+delta],           # left_bottom
                 [grid_dis*grid_num-car_size+delta, grid_dis*grid_num-car_size+delta, grid_dis*grid_num+car_size+delta, grid_dis*grid_num+car_size+delta]           # right_bottom
        ]

intersect_point = [ 

                    [grid_dis*1-car_size+delta, grid_dis*1-car_size+delta, grid_dis*1+car_size+delta, grid_dis*1+car_size+delta],         # top_left
                    [grid_dis*2-car_size+delta, grid_dis*1-car_size+delta, grid_dis*2+car_size+delta, grid_dis*1+car_size+delta],        # top_middle
                    [grid_dis*3-car_size+delta, grid_dis*1-car_size+delta, grid_dis*3+car_size+delta, grid_dis*1+car_size+delta],        # top_right
                    [grid_dis*1-car_size+delta, grid_dis*2-car_size+delta, grid_dis*1+car_size+delta, grid_dis*2+car_size+delta],        # middle_left
                    [grid_dis*2-car_size+delta, grid_dis*2-car_size+delta, grid_dis*2+car_size+delta, grid_dis*2+car_size+delta],       # middle_middle
                    [grid_dis*3-car_size+delta, grid_dis*2-car_size+delta, grid_dis*3+car_size+delta, grid_dis*2+car_size+delta],       # middle_right
                    [grid_dis*1-car_size+delta, grid_dis*3-car_size+delta, grid_dis*1+car_size+delta, grid_dis*3+car_size+delta],        # bottom_left
                    [grid_dis*2-car_size+delta, grid_dis*3-car_size+delta, grid_dis*2+car_size+delta, grid_dis*3+car_size+delta],       # bottom_middle
                    [grid_dis*3-car_size+delta, grid_dis*3-car_size+delta, grid_dis*3+car_size+delta, grid_dis*3+car_size+delta]        # bottom_right
        ]

dir_possibility = [ 'straight', 'straight', 'straight', 'right', 'right', 'left']

# record the car on the board
mobility_list = []
deleteIndex = []

def checkEntrance(car, pos, oval):
    for i in range(len(entrance_point)):
        if(entrance_point[i][:] == pos[:]):
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
                    c.move(oval, car.movVector[0] * velocity, car.movVector[1] * velocity)

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
                    c.move(oval, car.movVector[0] * velocity, car.movVector[1] * velocity)

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
                    c.move(oval, car.movVector[0] * velocity, car.movVector[1] * velocity)

            return True
    return False

def checkCorner(car, pos, oval):
    if(pos[:] == corner_point[0][:]):
        if(car.getMovVector() == ( 0, -1)):
            car.setMovVectorFromCorner((1, 0))
        else:
            car.setMovVectorFromCorner((0, 1))
    elif(pos[:] == corner_point[1][:]):
        if(car.getMovVector() == ( 0, -1)):
            car.setMovVectorFromCorner((-1, 0))
        else:
            car.setMovVectorFromCorner((0, 1))
    elif(pos[:] == corner_point[2][:]):
        if(car.getMovVector() == ( 0, 1)):
            car.setMovVectorFromCorner((1, 0))
        else:
            car.setMovVectorFromCorner((0, -1))
    elif(pos[:] == corner_point[3][:]):
        if(car.getMovVector() == ( 0, 1)):
            car.setMovVectorFromCorner((-1, 0))
        else:
            car.setMovVectorFromCorner((0, -1))
    else:
        return False
    return True

def checkIntersect(car, pos, oval):
    for i in range(0, len(intersect_point)):
        if(pos[:] == intersect_point[i][:]):
            next_dir = random.choice(dir_possibility)
        #     print(next_dir)
            if(next_dir == 'straight'):
                car.setPrevIntersect(intersect_point[i])
            else:           # next_dir = right or left
                # print(next_dir)
                car.setMovVector(next_dir)        
                car.setPrevIntersect(intersect_point[i])
            c.move(oval, car.movVector[0] * velocity, car.movVector[1] * velocity)        
            return True
    return False    

def moveCar():
    for car in mobility_list:
        oval = car.getObj()
        pos = c.coords(oval)     # get the current position

        if(car.newCar == True):
            c.move(oval, car.movVector[0] * velocity, car.movVector[1] * velocity)
            car.setOldCar()
            continue
        
        if(checkEntrance(car, pos, oval)):
            continue
        elif(checkIntersect(car, pos, oval)):
            continue
        elif(checkCorner(car, pos, oval)):
            c.move(oval, car.movVector[0] * velocity, car.movVector[1] * velocity)            
            continue
        else:
            c.move(oval, car.movVector[0] * velocity, car.movVector[1] * velocity)
                

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
    for entrance_str, entrance_pos in entrance.items():
        n = random.randint(1, 101)
        if(n < poisson_1sec * 100):
            new_oval = c.create_oval(entrance_pos, fill=random.choice(fill_color), outline='')
            # set initial base station
            base_id = setInitBase(entrance_str)
            new_car = car.Car( entrance_str, new_oval, p_init, base_id, entrance_pos)
            mobility_list.append(new_car)

def deleteCar():
    # remove index in decreasing order
    global mobility_list
    global deleteIndex
    deleteIndex.sort(reverse=True)
    for delIdx in deleteIndex:
        delete = mobility_list.pop(delIdx)
        c.delete(delete.getObj())
        del delete        
    deleteIndex = []

def getDistance(p1x, p1y, p2x, p2y):
    return (math.sqrt(math.pow(p1x - p2x, 2) + math.pow(p1y - p2y, 2)))

def calPower(dis):
    return (p1 - 20 * math.log(dis/base, 10))

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
        oval = car.getObj()
        pos = c.coords(oval)     # get the current position
        
        car_x = (pos[0] + pos[2])/2
        car_y = (pos[1] + pos[3])/2

        old_id = car.getBaseID(policyStr)
        old_signal_dis = getDistance(car_x, car_y, base_station[old_id][0], base_station[old_id][1])
        
        old_signal_power = p0
        if(old_signal_dis != 0):
            old_signal_power = calPower(old_signal_dis)

        new_id = old_id
        new_signal_dis = old_signal_dis

        for i in range(len(base_station)):
            tmp_dis = getDistance(car_x, car_y, base_station[i][0], base_station[i][1])
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
        print( 'baseid: %d, old: %f, new: %f' % (car.getBaseID(policyStr), new_signal_power, old_signal_power))

def countdown(count):
    label['text'] = str(datetime.timedelta(seconds=count))
    if(count > 0):
        # move the cars on the canvas and remove exiting cars
        moveCar()
        deleteCar()
        
        # update the signals accroding to policies
        updatePower("best")
        updatePower("thres")
        updatePower("entropy")
        updatePower("my")
        
        # plot new cars
        plotCar()

        # every 1 second
        root.after(1, countdown, count-1)
    else:
        print("time's up")


######## Main #########
root = tk.Tk()
root.title('simulator')
geometry = str(grid_dis*grid_num + delta*2) + 'x' + str(grid_dis*grid_num + delta*2 + 30)
root.geometry(geometry)
root.resizable(0, 0)

c = tk.Canvas(root, height=grid_dis*grid_num, width=grid_dis*grid_num, bg='white')
c.pack(fill=tk.BOTH, expand=True)

w = grid_dis * grid_num +1
h = grid_dis * grid_num +1

# Creates all vertical lines at intevals of 100
for i in range(0, w, grid_dis):
    c.create_line([(i+delta, 0+delta), (i+delta, h+delta)], tag='grid_line', fill='gray')

# Creates all horizontal lines at intevals of 100
for i in range(0, h, grid_dis):
    c.create_line([(0+delta, i+delta), (w+delta, i+delta)], tag='grid_line', fill='gray')

# create base in the simulator
base_file = tk.PhotoImage(file='base.png')
c.create_image(grid_dis+delta, grid_dis+delta, anchor='center', image=base_file)
c.create_image(grid_dis+delta, grid_dis*(grid_num-1)+delta, anchor='center', image=base_file)
c.create_image(grid_dis*(grid_num-1)+delta, grid_dis*(grid_num-1)+delta, anchor='center', image=base_file)
c.create_image(grid_dis*(grid_num-1)+delta, grid_dis+delta, anchor='center', image=base_file)

# set up countdown label
label = tk.Label(root)
label.config(font=("Courier", 14))
countdown(countdown_time)
label.pack()

root.mainloop()