from cmu_graphics import *
# don't forget to run: pip install cmu-graphics
import math as np
app.background = rgb(15,15,15)
app.currentLine = 0
app.current = 0
words = ['abhor', 'above', 'abuse', 'again', 'after', 'alley', 'angst', 'baggy', 'baits', 'basal', 'bends',
'bravo', 'carve', 'caked', 'check', 'cheek', 'clash', 'dents', 'depth', 'demon', 'enact', 'feast', 'flame',
'fauna', 'gripe', 'heart', 'heros', 'hydra', 'lakes', 'loose', 'motes', 'opera', 'palmy', 'prude', 'rabbi',
'ratio', 'rolls', 'rawed', 'rowdy', 'slink', 'smoke', 'soggy', 'spill', 'title', 'timid', 'tinge', 'truck',
'venom', 'vexed', 'warms', 'warns', 'words', 'yarns', 'zebra', 'zones']
word = choice(words).lower()
all = []
app.steps =0
class Input:
    def __init__(self, x, y, number, line):
        self.shape = Rect(x, y, 60, 60, fill=rgb(80,80,90))
        self.x = self.shape.centerX
        self.y = self.shape.centerY
        self.position = number
        self.letter = word[number]
        self.label = Label('',self.x,self.shape.bottom-5,align='bottom',fill='white',size=60)
        self.line = line
        self.enabled = False
for y in range(5):
    for x in range(5):
        all.append(Input((10+(x*80)), 5+(y*70), x, y))

def win():
    sleep(2)
    Rect(0,0,400,400,fill=rgb(50,50,60))
    Label('YOU WIN!',200,150,size=30,align='center',fill='white')
    Label("The Word Was: " + word,200,200,size=30,align='center',fill='white')
    app.stop()
    
def lose():
    sleep(2)
    Rect(0,0,400,400,fill=rgb(50,50,60))
    Label('you lost...',200,150,size=30,align='center',fill='red')
    Label("The Word Was: " + word,200,200,size=30,align='center',fill='white')
    app.stop()
    
def wordComp(word):
    a = {}
    for i in range(5):
        if word[i] in a:
            a[word[i]] +=1
        else:
            a[word[i]] = 1
    return a

def testGuess(foo):
    if foo == word:
        for input in all:
            if input.line == app.currentLine and input.enabled == True:
                input.shape.fill = 'chartreuse'
        win()
    a = {}
    for input in all:
        if input.line == app.currentLine and input.enabled == True:
            if input.letter == foo[input.position]:
                input.shape.fill = 'chartreuse'
                
            if input.shape.fill!='chartreuse': # if not green
                if input.label.value in word: 
                    input.shape.fill = 'yellow'
                    input.label.fill = rgb(80,80,90)
    app.currentLine+=1
    app.current = 0
    app.steps = 0

def onKeyPress(key):
    if key != 'enter' and key != 'backspace':
        if app.current<5:
            for input in all:
                if input.line == app.currentLine and input.position == app.current and input.enabled == True:
                    input.label.value = key.lower()
                    input.label.bottom = input.shape.bottom-5
            app.current+=1
    if key == 'backspace':
        for input in all:
            if input.line == app.currentLine and input.position == app.current-1 and input.enabled == True:
                input.label.value = ''
                input.label.bottom = input.shape.bottom-5
        if app.current>=1:
            app.current-=1
    if key == 'enter' and app.current == 5:
        guess = ''
        for input in all:
            if input.line == app.currentLine and input.enabled == True:
                guess += input.label.value # don't forget to clear the value of app.guess when done
        testGuess(guess)
    pass

app.stepsPerSecond = 60
def onStep():
    app.steps+=1
    for input in all:
        if app.currentLine == input.line:
            input.enabled=True # when this is disabled set app steps to 0
        elif app.currentLine != input.line:
            input.enabled = False
        if input.enabled == False and input.shape.width>31:
            input.shape.width=15*np.cos(-.03*app.steps)+45
            input.shape.height=15*np.cos(-.03*app.steps)+45
            input.label.size = 15*np.cos(-.03*app.steps)+45
            input.label.bottom = input.shape.bottom-5
            input.shape.centerX = input.x
            input.shape.centerY = input.y
        if input.enabled == True and input.shape.width<59:
            input.shape.width=15*np.cos(.03*app.steps-((np.pi*100)/4))+45
            input.shape.height=15*np.cos(.03*app.steps-((np.pi*100)/4))+45
            input.label.size =15*np.cos(.03*app.steps-((np.pi*100)/4))+45
            input.label.bottom = input.shape.bottom-5
            input.shape.centerX = input.x
            input.shape.centerY = input.y
    if app.currentLine>4:
        lose()
cmu_graphics.run()
