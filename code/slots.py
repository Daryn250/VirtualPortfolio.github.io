from cmu_graphics import *
# don't forget to run: pip install cmu-graphics
#slots
import random
import math
app.background = gradient(rgb(40,40,40),rgb(60,60,60),start='top')
border = Rect(-500,0,1500,400, border=rgb(60,60,60),borderWidth=125,fill = None)
score = Label(0,200,75,size=30,fill='white')
score.hidden = 0
app.bet = 10
app.isRigged = True

# lines
# bets
# score
# A K Q J - 10/3, 30/4, 50/5 
# 7s are free slots
# cool animations 

spinning = [[],[],[]]
coolListName = []
successDisplay = []
coolAnimation = []

def A(x,y,row,column):
    a = Rect(x-25,y-25,50,50,fill='crimson')
    a.text = Label('A',a.centerX+3,a.centerY,size=25,bold=True,font = 'cinzel')
    a.vy = 10
    a.row = row
    a.column = column
    return a

def K(x,y,row,column):
    k = Rect(x-25,y-25,50,50,fill='orangeRed')
    k.text = Label('K',k.centerX+3,k.centerY,size=25,bold=True,font = 'cinzel')
    k.vy = 10
    k.row = row
    k.column = column
    return k

def Q(x,y,row,column):
    q = Rect(x-25,y-25,50,50,fill='orange')
    q.text = Label('Q',q.centerX+3,q.centerY,size=25,bold=True,font = 'cinzel')
    q.vy = 10
    q.row = row
    q.column = column
    return q

def J(x,y,row,column):
    j = Rect(x-25,y-25,50,50,fill='dodgerBlue')
    j.text = Label('J',j.centerX+3,j.centerY,size=25,bold=True,font = 'cinzel')
    j.vy = 10
    j.row = row
    j.column = column
    return j

def S(x,y,row,column):
    s = Rect(x-25,y-25,50,50,fill='chartreuse')
    s.text = Label(0,s.centerX,s.centerY)
    s.free = Circle(s.centerX,s.centerY,15,fill='white')
    s.vy = 10
    s.row = row
    s.column = column
    return s

def T(x,y,row,column):
    t = Rect(x-25,y-25,50,50,fill='hotPink')
    t.text = Label('10',t.centerX,t.centerY,size=25,bold=True,font = 'cinzel')
    t.vy = 10
    t.row = row
    t.column = column
    return t

def N(x,y,row,column):
    n = Rect(x-25,y-25,50,50,fill='darkCyan')
    n.text = Label('9',n.centerX,n.centerY,size=25,bold=True,font = 'cinzel')
    n.vy = 10
    n.row = row
    n.column = column
    return n
    

for i in range(5):
    spinAnimation = Rect(75,100+(i*50),250,50,fill=gradient('red',rgb(230,0,0),start='bottom'))
    spinAnimation.vy = 8
    coolListName.append(spinAnimation)
for y in range(3):
    for x in range(5):
        spinning[y].append(None)

def result():
    offsety = -125
    weights = []
    for y in range(3):
        for x in range(5):
            chance = random.randint(0,2)
            if chance > 1 and len(weights)>2:
                type = choice(weights)
            else:
                type = random.randint(1,7)
            if type == 1:
                spinning[y][x] = A(100+(x*50),(y*50)+offsety,x,y)
                weights.append(1)
            elif type == 2:
                spinning[y][x] = K(100+(x*50),(y*50)+offsety,x,y)
                weights.append(2)
            elif type == 3:
                spinning[y][x] = Q(100+(x*50),(y*50)+offsety,x,y)
                weights.append(3)
            elif type == 4:
                spinning[y][x] = J(100+(x*50),(y*50)+offsety,x,y)
                weights.append(4)
            elif type == 5:
                spinning[y][x] = S(100+(x*50),(y*50)+offsety,x,y)
            elif type == 6:
                weights.append(6)
                spinning[y][x] = T(100+(x*50),(y*50)+offsety,x,y)
            elif type == 7:
                weights.append(7)
                spinning[y][x] = N(100+(x*50),(y*50)+offsety,x,y)

def createCoinAnimation(x,y,value):
    coin = Rect(x,y,10,10,fill='white')
    coin.centerX = x
    coin.centerY = y
    coin.value = value
    if coin.value>24:
        coin.fill = 'red'
    if coin.value>49:
        coin.fill = 'gold'
    if coin.value>499:
        coin.fill = 'lightBlue'
        coin.width = 30
        coin.height = 30
    coin.vx = (random.randint(1,40)-20)
    coin.vy = (random.randint(1,40)-20)
    coolAnimation.append(coin)


def checkList(a, b, checking,highlight=False, runs = 4):
    amt = 1
    if spinning[a][b].text.value == 0:
        a = checking[1][0]
        b = checking[1][1]
    for i in range(runs):
        if (i+1)>amt:
            break
        
        if spinning[a][b].text.value == spinning[checking[i][0]][checking[i][1]].text.value:
            amt+=1
            if highlight:
                spinning[checking[i][0]][checking[i][1]].border = 'white'
        elif spinning[checking[i][0]][checking[i][1]].text.value == 0:
            amt+=1
    return amt

def checkHorizontal():
    # from left check the right, if right is same then continue checking, if 3 then 10 pts, if 4 then 25, if 5 then 50
    for i in range(3):
        baller = [[i,1],[i,2],[i,3],[i,4]]
        
        if checkList(i,0,baller) > 4:
            
            createCoinAnimation(200,200,50)
            successDisplay.append(Line(spinning[i][0].left-10,spinning[i][0].centerY,spinning[i][4].right+10,spinning[i][4].centerY,fill='white',lineWidth = 20))
        
        elif checkList(i,0,baller) > 3:
            
            createCoinAnimation(200,200,30)
            successDisplay.append(Line(spinning[i][0].left-10,spinning[i][0].centerY,spinning[i][3].right+10,spinning[i][3].centerY,fill='white',lineWidth = 20))
        
        elif checkList(i,0,baller) > 2:
            
            createCoinAnimation(200,200,10)
            successDisplay.append(Line(spinning[i][0].left-10,spinning[i][0].centerY,spinning[i][2].right+10,spinning[i][2].centerY,fill='white',lineWidth = 20))

def checkDiagonal():
    dia = [[0,1],[1,2],[2,3],[2,4]]
    if checkList(0,0,dia) > 4:

        createCoinAnimation(200,200,50)
        successDisplay.append(Line(100,150,300,250,fill='white',lineWidth=20))
    
    rev = [[2,1],[1,2],[0,3],[0,4]]
    if checkList(2,0,rev) > 4:

        createCoinAnimation(200,200,50)
        successDisplay.append(Line(100,250,300,150,fill='white',lineWidth=20))

def checkVS():
    v1 = [[1,1],[2,2],[1,3],[0,4]]
    if checkList(0,0,v1) > 4:

        successDisplay.append(Line(100,150,200,250,fill='white',lineWidth=20))
        successDisplay.append(Line(200,250,300,150,fill='white',lineWidth=20))
        createCoinAnimation(200,200,50)
    
    v2 = [[1,1],[0,2],[1,3],[2,4]]
    if checkList(2,0,v2) > 4:

        successDisplay.append(Line(100,250,200,150,fill='white',lineWidth=20))
        successDisplay.append(Line(200,150,300,250,fill='white',lineWidth=20))
        createCoinAnimation(200,200,50)

def checkBigWin():
    erm = []
    for y in range(3):
        for x in range(5):
            erm.append([y,x])
    if checkList(0,0,erm, runs=15) > 14:
        createCoinAnimation(200,200,500)
        successDisplay.append(Line(0,200,400,200,fill='white',lineWidth=100,opacity=50))
        successDisplay.append(Line(0,200,400,200,fill='white',lineWidth=50,opacity=25))
        successDisplay.append(Line(0,200,400,200,fill='white',lineWidth=25,opacity=100))
        successDisplay.append(Label('BIG WIN!',200,350,font='cinzel',fill='black',size = 75))
        successDisplay.append(Label('BIG WIN!',205,355,font='cinzel',fill='white',size = 75))

app.steps = 0
app.spinTime = 120
app.resetableValue = 120
app.spinning = True
app.stepsPerSecond = 60

def onStep():
    app.steps += 1
    if app.spinning == True:
        app.resetableValue -= 1
        if app.resetableValue<1:
            result()
            app.spinning = False
    if app.spinning == False:
        if app.steps == 160:

            checkHorizontal()
        if app.steps == 170:
            if app.bet>19:
                checkDiagonal()
        if app.steps == 180:
            if app.bet>29:
                checkVS()
        if app.steps == 190:
            checkBigWin()
            
    for y in spinning:
        for item in y:
            try:
                item.centerY+=item.vy
                item.text.centerY+=item.vy
                try:
                    item.free+=item.vy
                except:
                    pass
                if item.bottom>265-(50*(2-item.column)):
                    item.vy = 0
                    item.centerY = 250-(50*(2-item.column))
                    item.text.centerY = 250-(50*(2-item.column))
                    try:
                        item.free.centerY = item.centerY
                    except:
                        pass
                if item.centerY < -6000:
                    item.visible = False
                    item.text.visible = False
                    try:
                        item.free.visible = False
                    except:
                        pass
                    spinning.remove(item)
                    app.group.remove(item)
            except:
                pass
        if app.spinning == True:
            for item in coolListName:
                item.visible=True
                item.centerY+=item.vy
                if item.top>275:
                    item.top=75
                    item.toFront()
            
        else:
            for item in coolListName:
                item.visible=False
    border.toFront()
    score.toFront()
    for item in successDisplay:
        item.toFront()
        if item.opacity>0:
            item.opacity-=1
        else:
            item.centerX = -6000
            successDisplay.remove(item)
        
    for item in coolAnimation:
        item.toFront()
        item.centerX+=item.vx
        item.centerY+=item.vy
        item.vx = item.vx/1.1
        item.vy = item.vy/1.1
        if item.centerX>score.centerX:
            item.vx+=(score.centerX-item.centerX)/100
        if item.centerX<score.centerX:
            item.vx+=(score.centerX-item.centerX)/100
        if item.centerY>score.centerY:
            item.vy+=(score.centerY-item.centerY)/100
        if item.centerY<score.centerY:
            item.vy+=(score.centerY-item.centerY)/100
        
        if distance(item.centerX,item.centerY,score.centerX,score.centerY)<3:
            item.visible=False
            score.hidden+=item.value
            coolAnimation.remove(item)
    
    if score.hidden-score.value>100:
        if score.value < score.hidden:
            score.value+=2
    else:
        if score.value < score.hidden:
            score.value+=1
    if score.value > score.hidden:
        score.value-=1
    
    if score.value<0:
        score.fill='red'
    else:
        score.fill = 'white'
            
def onKeyPress(key):
    if key == "space" or key == 'enter':
        if app.spinning == False and app.steps>200:
            for y in spinning:
                for item in y:
                    try:
                        item.centerX, item.centerY = 0,-7000
                        item.text.centerX, item.text.centerY = 0,0
                    except:
                        pass
            app.spinning = True
            app.steps = 0
            app.resetableValue = app.spinTime
            score.hidden-=app.bet
    if key == "up":
        if app.spinning == False and app.steps>200:
            if app.bet<30:
                app.bet+=10
            successDisplay.append(Label('Betting: ' + str(app.bet),200,325,fill='white',size = 30))
            
    if key == "down":
        if app.spinning == False and app.steps>200:
            if app.bet>10:
                app.bet-=10
            successDisplay.append(Label('Betting: ' + str(app.bet),200,325,fill='white', size = 30))
            
    if key == "up" or key == "down":
        if app.spinning==False:
            if app.bet > 9:
                for i in range(3):
                    successDisplay.append(Line(75,150+(i*50),325,150+(i*50),fill='white',lineWidth=1))
            if app.bet > 19:
                successDisplay.append(Line(100,150,300,250,fill='white',lineWidth=1))
                successDisplay.append(Line(100,250,300,150,fill='white',lineWidth=1))
            if app.bet > 29:
                successDisplay.append(Line(100,150,200,250,fill='white',lineWidth=1))
                successDisplay.append(Line(200,250,300,150,fill='white',lineWidth=1))
                
                successDisplay.append(Line(100,250,200,150,fill='white',lineWidth=1))
                successDisplay.append(Line(200,150,300,250,fill='white',lineWidth=1))
        
cmu_graphics.run()
