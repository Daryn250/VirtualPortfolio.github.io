from cmu_graphics import *
# don't forget to run: pip install cmu-graphics
##### variable declaration
import random
# creating groups for each tile
void=Group()
forests=Group()
oceans=Group()
deserts=Group()
mountains=Group()
# creating technical groups
toSearch=Group()
remove=Group()
# detailing
detailing=Group()
# more technical groups
boardValues=Group()
searcherValues=Group()
# settings
# defaults are 8, 6, 4, 2, 4
desertinforestrand = 100
forestinoceanrand = 100
oceanindesertrand = 100
forestinmountainrand = 100
mountaininforest = 100
reducedDebug=True
size=1
# lists to be able to remove tiles later
toRemove=[]
toForest=[]
toOcean=[]
toDesert=[]
toMountain=[]
# lists for getting the string
fullList=[]
currentValues=[]
# technical
wpressed=Label(1,-75,-75)
apa=Label(0,1000,1000)
app.setMaxShapeCount(50000)
progressBar=Line(20,20,380,20,fill='gray',opacity=70,visible=False,lineWidth=10)
###
###
# creating the size of the board, supports 1,2,3: 3 not reccomended but it works sometimes

s=size
for y in range(10*s):
    for i in range(10*s):
        placeholder=Rect((40*i)/s,(y*40)/s,40/s,40/s,fill='white',border='black')
        void.add(placeholder)
        placeholder.defnum=0
print(str(s*10)+' by '+str(s*10)+' board created')
if size==3:
    print('good luck')
# instructions
print('this program is console heavy, and most proccesses will act like they are frozen. check the console for what is currently happening.')
print('-----------------------------------')
print('instructions: press 0 to load a preset, or hit 1 2 3 4 to change the tile you are placing and then click to replace with that tile. once you have done that then simply hit 6 to run the program 10 times.')
print('(please note that this program is heavily unoptomized and that anything could break)')
##### end of variable declaration and board creation
# detailing the board after finishing
def detail():
    print('detailing...')
    for forest in forests.children:
        detail=Rect(forest.centerX-10,forest.centerY-10,20,20,fill='lightGreen',opacity=random.randint(1,25),align='center',rotateAngle=random.randint(-2,2))
        detailing.add(detail)
        detail=Rect(forest.centerX+10,forest.centerY-10,20,20,fill='lightGreen',opacity=random.randint(1,25),align='center',rotateAngle=random.randint(-2,2))
        detailing.add(detail)
        detail=Rect(forest.centerX-10,forest.centerY+10,20,20,fill='lightGreen',opacity=random.randint(1,25),align='center',rotateAngle=random.randint(-2,2))
        detailing.add(detail)
        detail=Rect(forest.centerX+10,forest.centerY+10,20,20,fill='lightGreen',opacity=random.randint(1,25),align='center',rotateAngle=random.randint(-2,2))
        detailing.add(detail)
    print('forests detailed')
    for ocean in oceans.children:
        detail=Rect(ocean.centerX-10,ocean.centerY-10,20,20,fill='blue',opacity=random.randint(1,25),align='center',rotateAngle=random.randint(0,5))
        detailing.add(detail)
        detail=Rect(ocean.centerX+10,ocean.centerY-10,20,20,fill='blue',opacity=random.randint(1,25),align='center',rotateAngle=random.randint(-5,0))
        detailing.add(detail)
        detail=Rect(ocean.centerX-10,ocean.centerY+10,20,20,fill='blue',opacity=random.randint(1,25),align='center',rotateAngle=random.randint(0,5))
        detailing.add(detail)
        detail=Rect(ocean.centerX+10,ocean.centerY+10,20,20,fill='blue',opacity=random.randint(1,25),align='center',rotateAngle=random.randint(-5,0))
        detailing.add(detail)
    print('oceans detailed')
    for desert in deserts.children:
        detail=Rect(desert.centerX-10,desert.centerY-10,20,20,fill='goldenrod',opacity=random.randint(1,25),align='center',rotateAngle=random.randint(-5,5))
        detailing.add(detail)
        detail=Rect(desert.centerX+10,desert.centerY-10,20,20,fill='goldenrod',opacity=random.randint(1,25),align='center',rotateAngle=random.randint(-5,5))
        detailing.add(detail)
        detail=Rect(desert.centerX-10,desert.centerY+10,20,20,fill='goldenrod',opacity=random.randint(1,25),align='center',rotateAngle=random.randint(-5,5))
        detailing.add(detail)
        detail=Rect(desert.centerX+10,desert.centerY+10,20,20,fill='goldenrod',opacity=random.randint(1,25),align='center',rotateAngle=random.randint(-5,5))
        detailing.add(detail)
    print('deserts detailed')
    for mountain in mountains.children:
        detail=Rect(mountain.centerX-10,mountain.centerY-10,20,20,fill='darkGray',opacity=random.randint(1,25),align='center',rotateAngle=random.randint(-10,-5))
        detailing.add(detail)
        detail=Rect(mountain.centerX+10,mountain.centerY-10,20,20,fill='darkGray',opacity=random.randint(1,25),align='center',rotateAngle=random.randint(5,10))
        detailing.add(detail)
        detail=Rect(mountain.centerX-10,mountain.centerY+10,20,20,fill='darkGray',opacity=random.randint(1,25),align='center',rotateAngle=random.randint(-10,-5))
        detailing.add(detail)
        detail=Rect(mountain.centerX+10,mountain.centerY+10,20,20,fill='darkGray',opacity=random.randint(1,25),align='center',rotateAngle=random.randint(5,10))
        detailing.add(detail)
    print('mountains detailed')  # adding details to the board after creation
# adding labels to all tiles (highly unoptomized) (but i dont care L + ratio)
def addLabels():
    labelAmount=0
    for labels in boardValues:
        boardValues.remove(label)
        labelAmount-=1
    for forest in forests.children:
        labels=Label(1,forest.centerX,forest.centerY,align='center',fill='red',visible=False)
        boardValues.add(labels)
        labelAmount+=1
    for ocean in oceans.children:
        labels=Label(2,ocean.centerX,ocean.centerY,align='center',fill='red',visible=False)
        boardValues.add(labels)
        labelAmount+=1
    for desert in deserts.children:
        labels=Label(3,desert.centerX,desert.centerY,align='center',fill='red',visible=False)
        boardValues.add(labels)
        labelAmount+=1
    for mountain in mountains.children:
        labels=Label(4,mountain.centerX,mountain.centerY,align='center',fill='red',visible=False)
        boardValues.add(labels)
        labelAmount+=1
    if reducedDebug==False:
        print('currentLabels:'+str(labelAmount)) #adding labels to all places where 
# adding labels for the searcher and adding the heatmap of concentration
# creates a string for each tile of the adjacent tiles and then sends the string to the next functions
def searcherLabels():
    apa.value=0
    for searching in toSearch:
        searcherValue=Label((searching.opacity//10)-5,searching.centerX,searching.centerY)
        toSearch.add(searcherValue)
        adjacentPhysical=Label(0,searching.centerX,searching.centerY+(10/s),size=7,fill='blue')
        apa.value+=1
        adjacentStringNSEW=[0,0,0,0]
        for labels in boardValues:
            
            if adjacentPhysical.centerX-(40/s)==labels.centerX and adjacentPhysical.centerY-(10/s)==labels.centerY:
                if 0 in adjacentStringNSEW:
                    adjacentStringNSEW.remove(0)
                    adjacentStringNSEW.insert(0,labels.value)
                
            if adjacentPhysical.centerX+(40/s)==labels.centerX and adjacentPhysical.centerY-(10/s)==labels.centerY:
                if 0 in adjacentStringNSEW:
                    adjacentStringNSEW.remove(0)
                    adjacentStringNSEW.insert(1,labels.value)
                
            if adjacentPhysical.centerX==labels.centerX and adjacentPhysical.centerY-(50/s)==labels.centerY:
                if 0 in adjacentStringNSEW:
                    adjacentStringNSEW.remove(0)
                    adjacentStringNSEW.insert(2,labels.value)
                
            if adjacentPhysical.centerX==labels.centerX and adjacentPhysical.centerY+(30/s)==labels.centerY:
                if 0 in adjacentStringNSEW:
                    adjacentStringNSEW.remove(0)
                    adjacentStringNSEW.insert(3,labels.value)
                
            adjacentPhysical.value=[adjacentStringNSEW[0],adjacentStringNSEW[1],adjacentStringNSEW[2],adjacentStringNSEW[3]]
            boardValues.add(adjacentPhysical)
# updating the colors of each value of tile
# works by taking each label and adding opacity to the main searcher when adjacent tiles are found and then locks the tile
def colorUpdate(lvalue,color):
    colorruns=0
    for searching in toSearch:
        for labels in boardValues:
            nlock=0
            slock=0
            elock=0
            wlock=0
            if searching.centerX==labels.centerX-(40/s) and searching.centerY==labels.centerY and elock==0:
                if labels.value==lvalue:
                    searching.fill=color
                    if searching.opacity!=100:
                        searching.opacity+=10
                    elock+=1
                    
            if searching.centerX==labels.centerX+(40/s) and searching.centerY==labels.centerY and wlock==0:
                if labels.value==lvalue:
                    searching.fill=color
                    if searching.opacity!=100:
                        searching.opacity+=10
                    wlock+=1
                    
            if searching.centerY==labels.centerY-(40/s) and searching.centerX==labels.centerX and slock==0:
                if labels.value==lvalue:
                    searching.fill=color
                    if searching.opacity!=100:
                        searching.opacity+=10
                    slock+=1
                    
            if searching.centerY==labels.centerY+(40/s) and searching.centerX==labels.centerX and nlock==0:
                if labels.value==lvalue:
                    searching.fill=color
                    if searching.opacity!=100:
                        searching.opacity+=10
                    nlock+=1
            colorruns+=1
        if reducedDebug==False:
            print('north:'+str(nlock) +', east:'+ str(elock)+', south:'+str(slock)+', west:'+str(wlock))
    if reducedDebug==False:
        print(str(lvalue)+' updated with color '+ str(color)+' with '+str(colorruns)+' runs')
# searching for each adjacent tile to a non-placeholder tile and adding a label
# for each placeholder it adds 4 labels 
def Searchtime():
    searchingAmount=0
    labelsVisible=False
    for forest in forests.children:
        label1=Circle(forest.centerX,forest.centerY-(40/s),5,visible=labelsVisible)
        remove.add(label1)
        label1=Circle(forest.centerX,forest.centerY+(40/s),5,visible=labelsVisible)
        remove.add(label1)
        label1=Circle(forest.centerX-(40/s),forest.centerY,5,visible=labelsVisible)
        remove.add(label1)
        label1=Circle(forest.centerX+(40/s),forest.centerY,5,visible=labelsVisible)
        remove.add(label1)
    for ocean in oceans.children:
        label1=Circle(ocean.centerX,ocean.centerY-(40/s),5,visible=labelsVisible)
        remove.add(label1)
        label1=Circle(ocean.centerX,ocean.centerY+(40/s),5,visible=labelsVisible)
        remove.add(label1)
        label1=Circle(ocean.centerX-(40/s),ocean.centerY,5,visible=labelsVisible)
        remove.add(label1)
        label1=Circle(ocean.centerX+(40/s),ocean.centerY,5,visible=labelsVisible)
        remove.add(label1)
    for desert in deserts.children:
        label1=Circle(desert.centerX,desert.centerY-(40/s),5,visible=labelsVisible)
        remove.add(label1)
        label1=Circle(desert.centerX,desert.centerY+(40/s),5,visible=labelsVisible)
        remove.add(label1)
        label1=Circle(desert.centerX-(40/s),desert.centerY,5,visible=labelsVisible)
        remove.add(label1)
        label1=Circle(desert.centerX+(40/s),desert.centerY,5,visible=labelsVisible)
        remove.add(label1)
    for mountain in mountains.children:
        label1=Circle(mountain.centerX,mountain.centerY-(40/s),5,visible=labelsVisible)
        remove.add(label1)
        label1=Circle(mountain.centerX,mountain.centerY+(40/s),5,visible=labelsVisible)
        remove.add(label1)
        label1=Circle(mountain.centerX-(40/s),mountain.centerY,5,visible=labelsVisible)
        remove.add(label1)
        label1=Circle(mountain.centerX+(40/s),mountain.centerY,5,visible=labelsVisible)
        remove.add(label1)

    for label1 in remove.children:
        for placeholder in void.children:
            if placeholder.hitsShape(label1):
                searching=Rect(placeholder.centerX-(20/s),placeholder.centerY-(20/s),(40/s),(40/s),fill='cyan',opacity=50)
                toSearch.add(searching)
                searchingAmount+=1
                if reducedDebug==False:
                    print('amount of searching tiles=' + str(searchingAmount))
                void.remove(placeholder)
                remove.clear()
    remove.clear()
# replace placeholder with forest tile
def replaceForest(x,y):            
    forest=Rect(x-(20/s),y-(20/s),40/s,40/s,fill='forestGreen',opacity=100)
    forests.add(forest)
# replace placeholder with ocean tile
def replaceOcean(x,y):            
    water=Rect(x-(20/s),y-(20/s),40/s,40/s,fill='mediumSlateBlue',opacity=100)
    oceans.add(water)
# replace placeholder with desert tile
def replaceDesert(x,y):            
    desert=Rect(x-(20/s),y-(20/s),40/s,40/s,fill='paleGoldenrod',opacity=100)
    deserts.add(desert)
# replace placeholder with mountain tile
def replaceMountain(x,y):            
    mountain=Rect(x-(20/s),y-(20/s),40/s,40/s,fill='gray',opacity=100)
    mountains.add(mountain)
# code to collapse and combine all previous steps and place tiles with random probabilities based on their string
def collapse():
    collapses=0
    for adjacentPhysical in boardValues.children:
        # declares variables
        currentValues=[0,0,0,0]
        forestWeight=0
        oceanWeight=0
        desertWeight=0
        mountainWeight=0
        # takes the string and removes a bunch of unneeded stuff from it
        fullList=str(adjacentPhysical.value).split()
        currentValues=str(adjacentPhysical.value).strip('[]').split(', ')
        # checks the values in the list and then adds weight for each value that matches
        if len(currentValues)==4:
            if reducedDebug==False:
                print(str(currentValues))
            while('1' in currentValues):
                forestWeight+=1
                currentValues.remove('1')
                if reducedDebug==False:
                    print('forestWeight Updated to '+str(forestWeight))
            while('2' in currentValues):
                oceanWeight+=1
                currentValues.remove('2')
                if reducedDebug==False:
                    print('oceanWeight Updated to '+str(oceanWeight))
            while('3' in currentValues):
                desertWeight+=1
                currentValues.remove('3')
                if reducedDebug==False:
                    print('desertWeight Updated to '+str(desertWeight))
            while('4' in currentValues):
                mountainWeight+=1
                currentValues.remove('4')
                if reducedDebug==False:
                    print('mountainWeight Updated to '+str(mountainWeight))
            if reducedDebug==False:
                print('weights: f'+str(forestWeight)+',o'+str(oceanWeight)+',d'+str(desertWeight)+',m'+str(mountainWeight))
            ### part 2 (placing tiles)
            maxWeight=max(forestWeight,oceanWeight,desertWeight,mountainWeight)
            if reducedDebug==False:
                print('max:'+str(maxWeight))
            # if the max weight is - then place a - tile and more randomization
            if maxWeight==forestWeight:
                if reducedDebug==False:
                    print('max is forest, fw:'+str(forestWeight)+',max:'+str(maxWeight))
                for searching in toSearch:
                    if searching not in toForest and searching.contains(adjacentPhysical.centerX,adjacentPhysical.centerY):
                        if forestWeight==4:
                            toForest.append(searching)
                        elif forestWeight==3 and random.randint(1,8)==1:
                            toDesert.append(searching)
                        elif forestWeight==2 and random.randint(1,5)==1:
                            toDesert.append(searching)
                        elif forestWeight==1 and random.randint(1,3)==1:
                            toDesert.append(searching)
                        else:
                            toForest.append(searching)
                        if reducedDebug==False:
                            print('forest added to list')
                    
            elif maxWeight==oceanWeight:
                print('max is ocean')
                for searching in toSearch:
                    if searching not in toOcean and searching.contains(adjacentPhysical.centerX,adjacentPhysical.centerY):
                        if oceanWeight==4:
                            toOcean.append(searching)
                        elif oceanWeight==3 and random.randint(1,8)==1:
                            toDesert.append(searching)
                        elif oceanWeight==2 and random.randint(1,5)==1:
                            toDesert.append(searching)
                        elif oceanWeight==1 and random.randint(1,3)==1:
                            toDesert.append(searching)
                        else:
                            toOcean.append(searching)
                        if reducedDebug==False:
                            print('ocean added to list')
                    
            elif maxWeight==desertWeight:
                if reducedDebug==False:
                    print('max is desert')
                for searching in toSearch:
                    if searching not in toDesert and searching.contains(adjacentPhysical.centerX,adjacentPhysical.centerY):
                        if desertWeight==4:
                            toDesert.append(searching)
                        elif desertWeight==3 and random.randint(1,8)==1:
                            if random.randint(1,2)==1:
                                toOcean.append(searching)
                            else:
                                toForest.append(searching)
                        elif desertWeight==2 and random.randint(1,5)==1:
                            if random.randint(1,2)==1:
                                toOcean.append(searching)
                            else:
                                toForest.append(searching)
                        elif desertWeight==1 and random.randint(1,3)==1:
                            if random.randint(1,2)==1:
                                toOcean.append(searching)
                            else:
                                toForest.append(searching)
                        else:
                            toForest.append(searching)
                        if reducedDebug==False:
                            print('desert added to list')
                    
            elif maxWeight==mountainWeight:
                if reducedDebug==False:
                    print('max is mountain')
                for searching in toSearch:
                    if searching not in toMountain and searching.contains(adjacentPhysical.centerX,adjacentPhysical.centerY):
                        if mountainWeight==4:
                            toMountain.append(searching)
                        elif mountainWeight==3 and random.randint(1,8)==1:
                            toForest.append(searching)
                        elif mountainWeight==2 and random.randint(1,5)==1:
                            toForest.append(searching)
                        elif mountainWeight==1 and random.randint(1,3)==1:
                            toForest.append(searching)
                        else:
                            toMountain.append(searching)
                        if reducedDebug==False:
                            print('mountain added at to list')
            # counting the amount of collapses and then prints the end of the loop and how much has been completed
            collapses+=1 
            if reducedDebug==False:
                print('***************END OF LOOP****************')
            print(str(rounded((collapses/apa.value)*100))+'% done or '+str(collapses)+' out of '+str(apa.value))  
            
            ### removing the appended from the lists and actually placing tiles based on randomization
            
            boardValues.remove(adjacentPhysical)
            
            for searching in toForest:
                if random.randint(1,desertinforestrand)==1:
                    replaceDesert(searching.centerX,searching.centerY)
                elif random.randint(1,mountaininforest)==1:
                    replaceMountain(searching.centerX,searching.centerY)
                else:
                    replaceForest(searching.centerX,searching.centerY)
                toForest.remove(searching)
                toSearch.remove(searching)
            if reducedDebug==False:
                print('forest cleared')
            
            for searching in toOcean:
                if random.randint(1,forestinoceanrand)==1:
                    replaceForest(searching.centerX,searching.centerY)
                else:
                    replaceOcean(searching.centerX,searching.centerY)
                toOcean.remove(searching)
                toSearch.remove(searching)
            if reducedDebug==False:
                print('ocean cleared')
            
            for searching in toDesert:
                if random.randint(1,oceanindesertrand)==1:
                    replaceOcean(searching.centerX,searching.centerY)
                else:
                    replaceDesert(searching.centerX,searching.centerY)
                toDesert.remove(searching)
                toSearch.remove(searching)
            if reducedDebug==False:
                print('desert cleared')
            
            for searching in toMountain:
                if random.randint(1,forestinmountainrand)==1:
                    replaceForest(searching.centerX,searching.centerY)
                else:
                    replaceMountain(searching.centerX,searching.centerY)
                toMountain.remove(searching)
                toSearch.remove(searching)
            if reducedDebug==False:
                print('mountain cleared')
            
    print('---------------END OF TASK-----------------')
# code for replacing with tiles
def onMousePress(mouseX,mouseY):
    for placeholder in void:
        if placeholder.hits(mouseX,mouseY):
            if wpressed.value==1:
                replaceForest(placeholder.centerX,placeholder.centerY)
                void.remove(placeholder)
            if wpressed.value==2:
                replaceOcean(placeholder.centerX,placeholder.centerY)
                void.remove(placeholder)
            if wpressed.value==3:
                replaceDesert(placeholder.centerX,placeholder.centerY)
                void.remove(placeholder)
            if wpressed.value==4:
                replaceMountain(placeholder.centerX,placeholder.centerY)
                void.remove(placeholder)
# code for key pressing
# better detailed instructions
# to run the code, you can either hit (1,2,3,4) for different tiles and click on a placeholder tile to change it
# to the selected tile, or hit 0 and enter (1, sus, or rand) then press either a to run the program once, or 6 to
# run it 10 times and complete the entire board.
def onKeyPress(key):
    wpressed.value=1
    if key==('down'):
        Searchtime()
    if key==('c'):
        colorUpdate(1,'salmon')
        colorUpdate(2,'salmon')
        colorUpdate(3,'salmon')
        colorUpdate(4,'salmon')
    if key==('b'):
        collapse()
    if key==('d'):
        detail()
    if key==('up'):
        detailing.clear()
    if key==('i'):
        addLabels()
    if key==('0'):
        presetType=app.getTextInput('preset?')
        if presetType=='1':
            onMousePress(220,180)
            onMousePress(260,220)
            onMousePress(220,260)
            onMousePress(180,220)
            wpressed.value+=1
            onMousePress(300,340)
        if presetType=='sus':
            onMousePress(140,140)
            onMousePress(180,140)
            onMousePress(220,140)
            onMousePress(100,180)
            onMousePress(140,180)
            onMousePress(100,220)
            onMousePress(140,220)
            onMousePress(180,220)
            onMousePress(220,220)
            onMousePress(140,260)
            onMousePress(180,260)
            onMousePress(220,260)
            onMousePress(140,300)
            onMousePress(220,300)
            onMousePress(140,340)
            onMousePress(220,340)
            wpressed.value+=1
            onMousePress(180,180)
            onMousePress(220,180)
            onMousePress(260,180)
        if presetType=='rand':
            for i in range(random.randint(3,20)):
                onMousePress(random.randint(0,400),random.randint(0,400))
            wpressed.value+=1
            for i in range(random.randint(3,20)):
                onMousePress(random.randint(0,400),random.randint(0,400))
            wpressed.value+=1
            for i in range(random.randint(3,20)):
                onMousePress(random.randint(0,400),random.randint(0,400))
            wpressed.value+=1
            for i in range(random.randint(3,20)):
                onMousePress(random.randint(0,400),random.randint(0,400))
        print('preset generated:'+presetType)
    if key==('-'):
        searcherLabels()
    if key==('r'):
        for labels in boardValues.children:
            boardValues.remove(labels)
        for searcherValue in toSearch:
            toSearch.remove(searcherValue)
    # tileswapper
    if key==('1'):
        wpressed.value=1
    if key==('2'):
        wpressed.value=2
    if key==('3'):
        wpressed.value=3
    if key==('4'):
        wpressed.value=4
    # all together now
    if key==('a'):
        print('function Searchtime() started')
        Searchtime()
        print('function addLabels() started')
        addLabels()
        print('function colorUpdate() started')
        for i in range(4):
            colorUpdate(1+i,'salmon')
        print('function searcherLabels() started')
        searcherLabels()
        print('function collapse() started')
        collapse()
        print('clearing boardValues')
        for labels in boardValues.children:
            boardValues.remove(labels)
        print('clearing searcherValues')
        for searcherValue in toSearch:
            toSearch.remove(searcherValue)
        # or 'down' 'i' 'c' '-' 'b' 'r'
    if key==('6'):
        progressBar.visible=True
        progressBar.x2=progressBar.x1
        progressBar.toFront()
        onKeyPress('a')
        print('---------------END OF RUN 1-----------------')
        progressBar.x2+=.1*360
        progressBar.toFront()
        onKeyPress('a')
        print('---------------END OF RUN 2-----------------')
        progressBar.x2+=.1*360
        progressBar.toFront()
        onKeyPress('a')
        print('---------------END OF RUN 3-----------------')
        progressBar.x2+=.1*360
        progressBar.toFront()
        onKeyPress('a')
        print('---------------END OF RUN 4-----------------')
        progressBar.x2+=.1*360
        progressBar.toFront()
        onKeyPress('a')
        print('---------------END OF RUN 5-----------------')
        progressBar.x2+=.1*360
        progressBar.toFront()
        onKeyPress('a')
        print('---------------END OF RUN 6-----------------')
        progressBar.x2+=.1*360
        progressBar.toFront()
        onKeyPress('a')
        print('---------------END OF RUN 7-----------------')
        progressBar.x2+=.1*360
        progressBar.toFront()
        onKeyPress('a')
        print('---------------END OF RUN 8-----------------')
        progressBar.x2+=.1*360
        progressBar.toFront()
        onKeyPress('a')
        print('---------------END OF RUN 9-----------------')
        progressBar.x2+=.1*360
        progressBar.toFront()
        onKeyPress('a')
        print('---------------END OF RUN 10-----------------')
        progressBar.x2+=.1*360
        progressBar.toFront()
        detail()
        progressBar.visible=False
# SUPERPOSITION SUDOKU
cmu_graphics.run()
