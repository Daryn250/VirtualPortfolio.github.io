from cmu_graphics import *
# don't forget to run: pip install cmu-graphics
# my implementation of the a star search algorithm
import random
import math
size = 30
app.setMaxShapeCount(size*size*2)
array = []
# fix array
class Square:
    def __init__(self,x,y,weight,modified):
        self.shape = Rect((x*400)/size,(y*400)/size,400/size,400/size,border='black',fill='white',borderWidth = 0.1)
        self.listpos = x,y
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = None
        self.active = True
    
for i in range(size):
    array.append([])
for x in range(size):
    for y in range(size):
        a = Square(x,y,0,False)
        array[x].insert(y, a)
for x in range(size):
    for y in range(size):
        if random.randint(1,3)==1:
            array[y][x].shape.fill='black'
            array[y][x].active = False


# start sim
# random point as finish and start
finish = array[random.randint(0,size-1)][random.randint(0,size-1)]
finish.shape.fill = 'lime'
start = array[random.randint(0,size-1)][random.randint(0,size-1)]
start.shape.fill='red'

def Heuristic(a,b):
    # manhattan distance implementation
    ax = (a.shape.left*400)/size
    ay = (a.shape.top*400)/size
    bx = (b.shape.left*400)/size
    by = (b.shape.top*400)/size
    return (abs(ax - bx) + abs(ay - by))/400
    
def returnSteps(a,b):
    # a = start node, b = current node
    ax = (a.shape.left*400)/size
    ay = (a.shape.top*400)/size
    bx = (b.shape.left*400)/size
    by = (b.shape.top*400)/size
    return (abs(bx - ax) + abs(by - ay))

def returnMinWeight(a):
    min = a[0]
    for item in a:
        if item.f<min.f:
            item = min
    return min
    
def neighbors(a):
    lis = []
    x, y = a.listpos
    for i in range(3):
        if (x+i)>size:
            pass
        else:
            for b in range(3):
                if (y+b)>size:
                    pass
                else:
                    e = array[(x+i)-1][(y+b)-1]
                    if ((y+b)-1)>=0 and (x+i)-1>=0:
                        if e.active == True:
                            lis.append(e)
    return lis






# node properties
max = Heuristic(start,finish)*200

opened = [start]
closed = []    
def step():
    amt = 0
    start.g = 0
    start.h = Heuristic(start,finish)
    start.f = start.g + start.h
    start.parent = None
    while len(opened)>0:
        if amt>max:
            return current
        amt+=1
        current = returnMinWeight(opened)
        if current == finish:
            return True
        opened.remove(current)
        closed.append(current)
        for n in neighbors(current):
            if n in closed:
                continue
            tentative_g = current.g + (returnSteps(current,n)/size)
            
            if n not in opened:
                opened.append(n)
            elif tentative_g>=n.g:
                continue
            
            n.parent = current
            n.g = tentative_g
            n.h = Heuristic(n,finish)
            n.f = n.h + n.g
        
            
    return current
        
        
def reconstructPath(current):
    while current!=None:
        current.shape.fill='orange'
        Label(rounded(current.g),current.shape.centerX,current.shape.centerY,align='center',size=10)
        current = current.parent
    
     

    
    

def onKeyPress(key):
    if key == 'w':
        a = step()
        if a == True:
            print('finished')
            reconstructPath(finish)
            finish.shape.fill='lime'
            start.shape.fill='red'
        else:
            print('unable to find a path')
            reconstructPath(a)
            finish.shape.fill='lime'
            start.shape.fill='red'
            
cmu_graphics.run()
