# conways game of life rq
from cmu_graphics import * #type: ignore
import math
# dont forget to run: pip install cmu-graphics
app.on = True
size = 10

cas = []
class CA:
    def __init__(self,x,y):
        self.shape = Rect((x*400)/size,(y*400)/size,400/size,400/size,fill='red')
        self.x = x
        self.y = y
        cas.append(self)
        pass
    def kill_self(self):
        self.shape.fill='black'
        all[self.x][self.y] = None
        to_remove.remove(self.shape)
        del self
        



all = []
for x in range(size):
    all.append([])
    for i in range(size):
        all[x].append(None)
all_neighbor = []
for x in range(size):
    all_neighbor.append([])
    for y in range(size):
        all_neighbor[x].append(0)

def neighbors(x,y):
    nn = 0
    for i in range(-1,2):
        for j in range(-1,2):
            if 0 <= x+i < size and 0 <= y+j < size:
                e = all[x+i][y+j]
                if e != None:
                    if e == all[x][y]:
                        pass
                    else:
                        nn +=1
    return nn


# must fix the part where it doesnt delete the actual shapes it leaves behind. 
to_remove = Group()
rem_list = []
def a():
    for x in range(size):
        for y in range(size):
            all_neighbor[x].insert(y,neighbors(x,y))

    for x in range(size):
        for y in range(size):
            cell = all[x][y]
            
            if all_neighbor[x][y] < 2 and cell is not None:
                if cell in cas:
                    to_remove.add(cell.shape)
                    rem_list.append(cell)
                

            elif all_neighbor[x][y] == 3:
                if all[x][y] == None:
                    all[x][y] = CA(x, y)

            elif all_neighbor[x][y] > 3 and cell is not None:
                if cell in cas:
                    to_remove.add(cell.shape)
                    rem_list.append(cell)
    
    for item in rem_list:  # slice to a copy
        item.kill_self()
    rem_list.clear()

def onKeyPress(key):
    if key =='space':
        app.on = not app.on

def onStep():
    if app.on == False:
        a()


def onMousePress(mouseX,mouseY):
    mx = math.floor((mouseX*size)/400)
    my = math.floor((mouseY*size)/400)
    if all[mx][my] == None:
        all[mx][my] = CA(mx,my)
        

cmu_graphics.run()