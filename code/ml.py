import matplotlib.pyplot as plt # type: ignore
import numpy as np # type: ignore
from cmu_graphics import * # type: ignore
import random
app = app
size = 64
max_brain_size = 10
mutation = 5
mutation_changes = 1
app.setMaxShapeCount(size*size)
# possible errors: could be an issue that i don't have a connection to every single node? dunno yet it's not even working yet
# another error is the brain cannot grow, a bug with one node doesn't need grow or shrink those nodes

input_nodes = ['a','b','c','d','e','f','g','h','i','j','k','l']
# a - d = neighbor data
# e - h = wall data
# i = lifespan
# j = total surrounding bugs
# k = self.x
# l = self.y
# m = reward
# distance to nearest bug and direction to it
output_nodes = ['1','2','3','4','5']
actions = ['left','right','up','down','random']
# 1 = move up
    # 2 = move down
    # 3 = move left
    # 4 = move right
    # 5 = move random
class gridsquare:
    def __init__(self,x,y):
        self.shape = Rect(x,y,400/size,400/size,fill='white',border='black',borderWidth = 0.3)
        self.contains = None
    def update(self):
        self.shape.fill='white'
        
def bugbrain(brain = None):
    connections = {}
    if brain == None:
        # give it a random node tree
        # only for making the starting bugs
        while 1==1:
            foo = input_nodes[random.randint(0,len(input_nodes)-1)] + output_nodes[random.randint(0,len(output_nodes)-1)]
            weight = float(np.round((random.randint(0,400)/100)-2, decimals = 3))
            if foo not in connections.keys():
                connections.update({foo:weight})
            else:
                pass
            if len(connections.keys())>=max_brain_size:
                break

    else:
        connections = brain
        if random.randint(mutation, 100) == 100:# mutation succeed
            for i in range(mutation_changes):
                if random.randint(2,2)==1:
                    # change nodes
                    while 1==1:
                        foo = input_nodes[random.randint(0,len(input_nodes)-1)] + output_nodes[random.randint(0,len(output_nodes)-1)]
                        if foo not in connections.keys():
                            ra = random.choice(list(connections.values()))
                            del connections[random.choice(list(connections.keys()))]
                            connections.update({foo:ra})
                            break
                else:
                    # change weights
                    ra = random.choice(list(connections.keys()))
                    weight = float(np.round((random.randint(0,400)/100)-2, decimals = 3))
                    connections.update({ra:weight})
    return connections

def allNodes():
    brain = {}
    for i in input_nodes:
        for o in output_nodes:
            keyv = str(i) + str(o)
            rand = (random.randint(0,400)-200)/100
            brain.update({keyv:rand})
    return brain

def addToWeights(weights,output_node,brain,item,modifier = 1):
    if output_node in weights.keys():
        total = float(brain.get(item) + weights.get(output_node))*modifier
        return {output_node:total}
    else:
        total = float(brain.get(item))
        return {output_node:total}

# yk it would have been a lot simpler to just format the data dictionary.
# whatever tho i dont care cuz im evil lol

# returns the action the bug will take based off the brain structure and data given
def interpretBug(brain,data):
    weights = {}
    for item in brain.keys():
        input_node = item[0] # split into input node
        output_node = item[1] # split into output node
        if input_nodes.index(input_node) <=3:
            ls = ['left','right','up','down']
            cur = ls[input_nodes.index(input_node)]
            if data[0].get(cur) !=None:
                if data[0].get(cur).contains == None:
                    weights.update(addToWeights(weights,output_node,brain,item))
        
        if input_nodes.index(input_node) >=4 and input_nodes.index(input_node) < 8:
            ls = ['left','right','up','down']
            aea = input_nodes.index(input_node)-4
            cur = ls[aea]
            if cur in data[1]:
                weights.update(addToWeights(weights,output_node,brain,item))
        if input_node == 'i': # lifespan
            if data[2]>0:
                weights.update(addToWeights(weights,output_node,brain,item,(data[2]/50)))
        if input_node == 'j':
            if data[3]>0:
                weights.update(addToWeights(weights,output_node,brain,item,(data[3]/9)))
        if input_node == 'k':
            if data[4]>0:
                weights.update(addToWeights(weights,output_node,brain,item,(data[4]/size)))
        if input_node == 'l':
            if data[5]>0:
                weights.update(addToWeights(weights,output_node,brain,item,(data[5]/size)))
    
    if weights:
        maximum = max(weights.values())    
        max_node = None
        for item in weights.keys():
            if weights.get(item)== maximum:
                max_node = item
                break
    else:
        return 'die'
    
    action = actions[output_nodes.index(max_node)]

    return action # remember to change



everyBug = []
class bug:
    def __init__(self,x,y,brain=None):
        self.fill = 'blue'
        self.data = []
        self.last_move = 'NEW'
        self.x = x
        self.y = y
        self.parent = all[self.x][self.y]
        self.parent.shape.fill = self.fill

        if brain == None:
            self.brain = bugbrain(allNodes())
        else:
            self.brain = brain

        self.lifespan = 50
        
        everyBug.append(self)
    def update_data(self):
        
        self.data.append(neighbor_data(self.x,self.y))
        self.data.append(touchingWalls(self.x,self.y))
        self.data.append(self.lifespan)
        self.data.append(totalSurroundingBugs(self.x,self.y))
        self.data.append(self.x)
        self.data.append(self.y)
        self.move(interpretBug(self.brain,self.data))
        
        self.lifespan-=1
    def move(self, dir):
        if dir == 'random':
            dir = random.choice(['up','down','left','right'])
        if dir == 'up':
            if (self.y)>0:
                b = all[self.x][self.y-1]
                if b.contains == None:
                    b.contains = self
                    b.shape.fill = self.fill
                    self.parent.contains = None
                    self.parent.shape.fill='white'
                    self.y-=1
        if dir == 'down':
            if (self.y)<size-1:
                b = all[self.x][self.y+1]
                if b.contains == None:
                    b.contains = self
                    b.shape.fill = self.fill
                    self.parent.contains = None
                    self.parent.shape.fill='white'
                    self.y+=1
        if dir == 'left':
            if (self.x)>0:
                b = all[self.x-1][self.y]
                if b.contains == None:
                    b.contains = self
                    b.shape.fill = self.fill
                    self.parent.contains = None
                    self.parent.shape.fill='white'
                    self.x-=1
        if dir == 'right':
            if (self.x)<size-1:
                b = all[self.x+1][self.y]
                if b.contains == None:
                    b.contains = self
                    b.shape.fill = self.fill
                    self.parent.contains = None
                    self.parent.shape.fill='white'
                    self.x+=1
        self.last_move = dir
        self.parent = all[self.x][self.y]
        self.reward = calculateReward(self.x,self.y)
        if dir == 'die':
            self.parent.shape.fill = 'white'
            self.parent.contains = None
            everyBug.remove(self)
            del self

# make grid
all = []
for i in range(size):
    all.append([]) # fixes an out of range bug kinda
for x in range(size):
    for y in range(size):
        a = gridsquare((x*400)/size,(y*400)/size)
        all[x].insert(y,a)

def neighbor_data(x,y):
    data = {}
    if x>0:
        data.update({"left": all[x-1][y]})
    if x<size-1:
        data.update({"right": all[x+1][y]})
    if y>0:
        data.update({"up": all[x][y-1]})
    if y<size-1:
        data.update({"down": all[x][y+1]})
    return data

def touchingWalls(x,y):
    data = []
    if x==0:
        data.append("left")
    elif x==size:
        data.append("right")
    else:
        data.append(None)
        data.append(None)
    if y==0:
        data.append("up")
    elif y==size:
        data.append("down")
    else:
        data.append(None)
        data.append(None)
    return data

def totalSurroundingBugs(x,y):
    counter = 0
    for item in neighbor_data(x,y).values():
        if item.contains != None:
            counter +=1
    return counter

def calculateReward(x,y):
    r = 0 
    if x<size-1:
        r += x
    if y<size-1:
        r += y
    return r



# let there be bugs!
def makeBugs(brain = None):
    for i in range(size):
        a = rounded(size/2)
        b = i-1
        if b%2 == 0:
            all[a][b].contains = bug(a,b,brain)
makeBugs()

app.steps = 0

app.stepsPerSecond = 100
def onStep():
    app.steps+=1
    for bug in everyBug:
        bug.update_data()
    if app.steps%100 == 0:
        maxbug_reward = -1
        maxbug = None
        for bug in everyBug:
            if bug.reward > maxbug_reward:
                maxbug = bug
                maxbug_reward = maxbug.reward
        a = maxbug.brain
        counter = 0
        for bug in everyBug:
            bug.parent.shape.fill = 'white'
            bug.parent.contains = None
            everyBug.remove(bug)
            del bug
            counter +=1
        print(counter)
        makeBugs(a)
        

        ## not all bugs are being deleted, very big issue prolly

def onResize():
    for x in range(size):
        for y in range(size):
            all[x][y].shape.left = (x*app.width)/size
            all[x][y].shape.top = (y*app.height)/size
            all[x][y].shape.width = app.width/size
            all[x][y].shape.height = app.height/size
    tooltip.width = (app.width*50)/400
    tooltip.height = (app.height*30)/400
    tooltip.text.size = (app.height*7)/400
cmu_graphics.run()