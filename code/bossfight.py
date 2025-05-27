from cmu_graphics import *
# don't forget to run: pip install cmu-graphics
# bossfight thing
# import some funny stuff
import random
import time
# create the game
for i in range(1):
    print('w,a,s,d to move, e to dodge, you have 3 dodges. good luck')
    # settings
    sidesVisible=True
    # groups
    meteors=Group()
    particles=Group()
    darts=Group()
    smolLasers=Group()
    circs=Group()
    plasmas=Group()
    pillars=Group()
    lasers=Group()
    sides=Group()
    sides=Group(
        Rect(0,0,400,70,fill='salmon',opacity=30,visible=sidesVisible),
        Rect(0,70,50,330,fill='salmon',opacity=30,visible=sidesVisible),
        Rect(350,70,50,330,fill='salmon',opacity=30,visible=sidesVisible),
        Rect(50,350,300,50,fill='salmon',opacity=30,visible=sidesVisible))
    shadows=Group()
    coordLasers=Group()
    lightnings=Group()
    remove=Group()
    pillarHit=Group()
    smollestg=Group()
    grid=Group()
    cheaps=Group()
    lws=Group()
    patterns=Group()
    obls=Group()
    chars=Group()
    
    # string settings
    playerColor='white'
    otherColor='black'
    playerHurt='salmon'
    dashColor='orange'
    
    # main assets
    app.background=rgb(61,60,60)
    timer=Label('0:00',200,375,fill='white',size=13,align='center')
    player=Rect(0,0,20,20,align='center',fill=playerColor)
    boss=Rect(200,200,20,20,align='center',fill='gray',visible=True)
    for i in range(4):
        meteor=Rect(200,200,10,10,fill='gray',visible=False)
        meteors.add(meteor)
    bossCenterer=Line(200,200,200,120,visible=False)
    gravitateAt=Label('bottom',500,500)
    hitGroundRecently=Label(False,500,500)
    meteorSpread=Label(40,500,500)
    meteorSpreadSwap=Label(True,500,500)
    doublejump=Label(True,500,500)
    playerHP=Label(3,500,500,fill=otherColor)
    dodgeCount=Label(3,500,500,fill=otherColor)
    currentTime=Label(time.time(),500,500)
    waitUntil=Label(time.time(),500,500)
    label=Label('Prepare.',200,300,fill='white',size=30,visible=False)
    steps=Label(None,375,375,visible=False)
    rbttr=Rect(350,200,20,20,fill='red',align='center',visible=False)
    rbttr2=Rect(50,200,20,20,fill='red',align='center',visible=False)
    
    # number settings
    playerTrailsPerFrame=4
    speed=0.3 #0.3
    gravitySpeed=0.6 #0.6
    jumpHeight=10
    app.stepsPerSecond=60
    app.steps=0
    app.laserSteps=0
    boss.dx=0
    boss.dy=0
    player.dx=0
    player.dy=0
    app.end=0
    app.level=1
    app.dashes=3
    app.wait=999999999999999
    app.ddelay=0
    app.tempx=0
    rbttr.dx=0
    rbttr.dy=0
    rbttr2.dx=0
    rbttr2.dy=0
    
    # true false settings
    playerTrail=True
    gravity=Label(True,500,500)
    canJump=True
    particlesOn=True
    app.circleAttacks=False
    app.dashing=False
    app.attacking=False
    invulnerable=Label(False,500,500)
    app.invincibility=False
    debug=False
    rbttr.start=False
    
    ####### special setting
    app.cryFromTheHeavens=True
    ####### turns on story, but is difficult, most flushed out mode. if false, random attacks.
    
    # creating things
    def credits():
        # prints the credits
        print('chris played this and he\'s SCREAMING at me to be in the credits')
        print('also i did everything myself lol')
        
    # colliding engine, if player hits an area just send player back and mess with the dx/dy
    def collision(collider,obj):
        if obj.contains(collider.left,collider.centerY):
            collider.left=obj.right
            collider.dx=-collider.dx/1.5
        if obj.contains(collider.right,collider.centerY):
            collider.right=obj.left
            collider.dx=-collider.dx/1.5
        if obj.contains(collider.centerX,collider.bottom):
            collider.bottom=obj.top
            collider.dy=-collider.dy/1.5
        if obj.contains(collider.centerX,collider.top):
            collider.top=obj.bottom
            collider.dy=-collider.dy/1.5
            
    # create the central spinning lasers
    def createLasers():
        laserAmount=1
        for i in range(4):
            laserAmount+=1
            x,y=getPointInDir(boss.centerX,boss.centerY,(laserAmount*(360/3))+boss.rotateAngle*(1),299)
            laser=Line(boss.centerX,boss.centerY,x,y,fill='white',opacity=100,lineWidth=1)
            lasers.add(laser)
            laser.toBack()
            
    # particle engine
    def addParticles(target,dx1,dx2,dy1,dy2,color,rand1,rand2,opacity):
        for i in range(random.randint(rand1,rand2)):
            hitparticle=Rect(target.centerX,target.centerY,4,4,fill=color,opacity=opacity)
            hitparticle.dx=random.randint(dx1,dx2)
            hitparticle.dy=random.randint(dy1,dy2)
            #hitparticle.rotate=random.randint(-10,10)
            particles.add(hitparticle)
            
    def updateParticles():
        for hitparticle in particles:
            hitparticle.centerX+=hitparticle.dx
            hitparticle.centerY+=hitparticle.dy
            #hitparticle.rotateAngle+=hitparticle.rotate
            hitparticle.dy+=1
            if hitparticle.opacity>0:
                hitparticle.opacity-=5
            else:
                particles.remove(hitparticle)
                
    # player updating / hitting
    def playerHit(hitOrUpdate):
        if hitOrUpdate=='hit':
            if app.invincibility==False:
                if app.dashing==False:
                    if invulnerable.value==False:
                        waitUntil.value=time.time()+2.5
                        player.fill=playerHurt
                        invulnerable.value=True
                        playerHP.value-=1
                        addParticles(player,-5,5,-5,5,player.fill,1,5,100)
                        
        if hitOrUpdate=='update': 
            if int(currentTime.value)>=int(waitUntil.value) and invulnerable.value==True:
                player.fill=playerColor
                invulnerable.value=False
                
        # player dash
        if app.steps>app.end:
            app.dashing=False
            player.fill=playerColor
            app.end=99999999999999
            
    # create the small darts
    def createDarts():
        for i in str(random.randint(5,20)):
            dart=RegularPolygon(random.randint(175,225),random.randint(175,225),5,3,fill=playerColor)
            dart.dx=random.randint(-2,2)
            dart.dy=random.randint(-3,3)
            darts.add(dart)
            
    # update if gravity works
    def gravityOn(on,side):
        if on==True:
            gravity.value=False
            gravitateAt=side
            if side=='bottom':
                player.dy-=1
            if side=='top':
                player.dy+=1
            if side=='left':
                player.dx+=1
            if side=='right':
                player.dx-=1
        if on==False:
            gravity.value=True
            
    # update all attacks
    def updateAttacks():
        for dart in darts:
            dart.rotateAngle=angleTo(dart.centerX,dart.centerY,player.centerX,player.centerY)
            if dart.centerX<player.centerX:
                dart.dx+=0.2
            else:
                dart.dx+=-0.2
            if dart.centerY<player.centerY:
                dart.dy+=0.2
            else:
                dart.dy+=-0.2
            dart.centerX+=dart.dx
            dart.centerY+=dart.dy
            if dart.left>400 or dart.right<0 or dart.top>400 or dart.bottom<0:
                darts.remove(dart)
                
            if dart.hitsShape(player):
                darts.remove(dart)
                playerHit('hit')
                
        for smol in smolLasers:
            if smol.lineWidth<10:
                smol.lineWidth+=0.3
            else:
                smol.fill='red'
                
                if smol.opacity>4:
                    smol.opacity-=2
                else:
                    smolLasers.remove(smol)
                    
            if smol.hitsShape(player) and smol.opacity>90 and smol.fill=='red':
                playerHit('hit')
                
        for circ in circs:
            circ.radius+=1
            if circ.opacity>2:
                circ.opacity-=1
            else:
                circs.remove(circ)
                
            if circ.hitsShape(player) and circ.opacity>50:
                playerHit('hit')
                
            # gravity swapping
            if app.steps%120==0:
                grav=['left','right','top','bottom']
                gravitateAt.value=choice(grav)
                player.dx=random.randint(-5,5)
                player.dy=random.randint(-5,5)
        plasmaAmount=0
        for plasma in plasmas:
            plasmaAmount+=1
            plasma.rotateAngle+=5
            if plasma.centerX<player.centerX:
                plasma.dx+=0.05
            else:
                plasma.dx+=-0.05
                
            if plasma.centerY<player.centerY:
                plasma.dy+=0.05
            else:
                plasma.dy+=-0.05
                
            plasma.centerX+=plasma.dx
            plasma.centerY+=plasma.dy
            if plasma.left>400 or plasma.right<0 or plasma.top>400 or plasma.bottom<0:
                plasmas.remove(plasma)
                
            if app.steps%(5*plasmaAmount)==0:
                addParticles(plasma,-1,1,-1,1,'red',1,3,100)
                
            if plasma.hitsShape(player):
                playerHit('hit')
                
        for pillar in pillars:
            temp=Rect(pillar.centerX,395,50,3,fill='orange',align='center')
            temp.toBack()
            remove.add(temp)
            pillarHitTest=Rect(500,0,45,20,visible=False,fill='gray')
            pillarHit.add(pillarHitTest)
            pillar.centerX+=pillar.dx
            pillar.centerY+=pillar.dy
            if pillar.bottom<400:
                pillar.dy+=gravitySpeed/2
                
            if pillar.bottom>400:
                pillar.bottom=400
                
            if pillar.bottom==400:
                for temp in remove:
                    remove.remove(temp)
                    pass
                
                if pillar.opacity>90:
                    pillar.opacity-=0.1
                    
                elif pillar.opacity>2:
                    pillar.opacity-=2
                    
                else:
                    pillars.remove(pillar)
                    
            if pillar.hitsShape(player) and pillar.opacity>50:
                    collision(player,pillar)
            for pillarHitTest in pillarHit:
                if pillar.bottom>350:
                    pillarHitTest.centerX=pillar.centerX
                    pillarHitTest.centerY=pillar.bottom
                
                if pillarHitTest.hitsShape(player) and pillar.opacity>75:
                    playerHP.value=-1
                    pillarHit.remove(pillarHitTest)
                pillarHit.remove(pillarHitTest)
                
        laserAmount=0
        fireXlasers=3
        laserSpeed=1
        for laser in lasers:
            laserAmount+=1
            x,y=getPointInDir(boss.centerX,boss.centerY,(laserAmount*(360/fireXlasers))+boss.rotateAngle*(laserSpeed),299)
            laser.x2=x
            laser.y2=y
            if laser.lineWidth<10:
                laser.lineWidth+=0.2
            else:
                laser.fill='red'
                if laser.hitsShape(player) and laser.opacity>90:
                    playerHit('hit')
                    
                if laser.opacity<100 and laser.opacity>=5:
                    laser.opacity-=5
                    
                elif laser.opacity<5:
                    lasers.remove(laser)
                    
        for cl in coordLasers:
            if cl.lineWidth<30:
                cl.lineWidth+=0.3
            else:
                cl.fill='red'
                if cl.opacity>4:
                    cl.opacity-=2
                    cl.lineWidth+=0.1
                    
                if cl.opacity<5:
                    coordLasers.remove(cl)
                    
                if cl.hitsShape(player) and cl.opacity>75:
                    playerHit('hit')
                    
        for object in lightnings:
            if object.opacity>2:
                object.opacity-=2
            else:
                lightnings.remove(object)
                
            if object.hitsShape(player) and object.opacity>70:
                playerHit('hit')
                
        for smollest in smollestg:
            smollest.centerX+=smollest.dx
            smollest.centerY+=smollest.dy
            if smollest.centerX>450 or smollest.centerY>450:
                smollestg.remove(smollest)
                
                for griddy in grid:
                    grid.remove(griddy)
                    
            if smollest.hitsShape(player):
                playerHit('hit')
                smollestg.remove(smollest)
                
        for cheap in cheaps:
            cheap.centerY+=3
            if cheap.centerY>500:
                cheaps.remove(cheap)
                
            if cheap.hitsShape(player):
                playerHit('hit')
                cheaps.remove(cheap)
                
        for lw in lws:
            if lw.lineWidth<lw.size:
                lw.lineWidth+=lw.size/120
                
            else:
                lw.fill='red'
                if lw.opacity>2:
                    lw.opacity-=1
                    
                elif lw.opacity<3:
                    lws.remove(lw)
                    
            if lw.opacity>75 and lw.fill=='red':
                if lw.hitsShape(player):
                    playerHit('hit')
                    
        for pattern in patterns:
            pattern.rotateAngle+=pattern.speed
            pattern.centerX+=pattern.dx
            pattern.centerY+=pattern.dy
            if pattern.opacity>99 and pattern.switch==False:
                pattern.switch=True
                
            elif pattern.opacity<100 and pattern.switch==False:
                pattern.opacity+=0.5
                
            if pattern.switch==True:
                pattern.fill='red'
                
                if pattern.opacity>2 and pattern.fill=='red':
                    pattern.opacity-=1
                else:
                    patterns.remove(pattern)
                    
                if pattern.hitsShape(player) and pattern.switch==True and pattern.opacity>80:
                    playerHit('hit')
                    
        if rbttr.start==True:
            
            if rbttr.centerX>player.centerX:
                rbttr.dx-=0.05
                
            elif rbttr.centerX<player.centerX:
                rbttr.dx+=0.05
                
            if rbttr.centerY>player.centerY:
                rbttr.dy-=0.05
                
            elif rbttr.centerY<player.centerY:
                rbttr.dy+=0.05
                
            if rbttr.left<0:
                rbttr.left=0
                rbttr.dx=-rbttr.dx
                
            if rbttr.right>400:
                rbttr.right=400
                rbttr.dx=-rbttr.dx
                
            if rbttr.top<0:
                rbttr.top=0
                rbttr.dy=-rbttr.dy
                
            if rbttr.bottom>400:
                rbttr.bottom=400
                rbttr.dy=-rbttr.dy
            
            if rbttr2.centerX>player.centerX:
                rbttr2.dx-=0.05
                
            elif rbttr2.centerX<player.centerX:
                rbttr2.dx+=0.05
                
            if rbttr2.centerY>player.centerY:
                rbttr2.dy-=0.05
                
            elif rbttr2.centerY<player.centerY:
                rbttr2.dy+=0.05
                
            if rbttr2.left<0:
                rbttr2.left=0
                rbttr2.dx=-rbttr2.dx
                
            if rbttr2.right>400:
                rbttr2.right=400
                rbttr2.dx=-rbttr2.dx
                
            if rbttr2.top<0:
                rbttr2.top=0
                rbttr2.dy=-rbttr2.dy
                
            if rbttr2.bottom>400:
                rbttr2.bottom=400
                rbttr2.dy=-rbttr2.dy
                
        for obl in obls:
            if obl.switch==False:
                if obl.radius>=obl.size:
                    pass
                
                else:
                    obl.radius+=obl.size/240
                    
                if obl.opacity<99.7:
                    obl.opacity+=0.3
            
            if obl.opacity>=99.8:
                obl.switch=True
            
            if obl.switch==True:
                if obl.opacity>0.3:
                    obl.opacity-=0.3
                    obl.radius+=obl.size/60
                else:
                    obls.remove(obl)
                    
        for char in chars:
            char.centerX+=char.dx
            char.centerY+=char.dy
            char.dx=char.dx/1.01
            char.dy=char.dy/1.01
            # collisions for characters
            if char.top<0:
                char.top=0
                char.dy=-char.dy/3
                char.dx=char.dx/1.5
                
            if char.bottom>400:
                char.bottom=400
                char.dy=-char.dy/3
                char.dx=char.dx/1.5
                
            if char.left<0:
                char.left=0
                char.dx=-char.dy/3
                char.dy=char.dx/1.5
                
            if char.right>400:
                char.right=400
                char.dx=-char.dy/3
                char.dy=char.dx/1.5
                
            if char.hitsShape(player):
                char.dx+=player.dx/3
                char.dy+=player.dy/3
                
    # update the meteors in the center that don't do anything lol
    def updateMeteors():
        boss.rotateAngle+=1
        bossCenterer.x1=boss.centerX
        bossCenterer.y1=boss.centerY
        meteorAmount=0
        if meteorSpread.value>50:
            meteorSpreadSwap.value=False
            
        elif meteorSpread.value<30:
            meteorSpreadSwap.value=True
            
        if meteorSpreadSwap.value==True:
            meteorSpread.value+=0.1
        else:
            meteorSpread.value-=0.1
            
        for meteor in meteors:
                meteorAmount+=1
                x,y=getPointInDir(boss.centerX,boss.centerY,meteorAmount*90+boss.rotateAngle,meteorSpread.value)
                bossCenterer.x2=x
                bossCenterer.y2=y
                meteor.centerX=x
                meteor.centerY=y
                meteor.rotateAngle+=1.5
    # small lasers that rain from the sky at random areas
    def smallLasers():
        x=random.randint(0,400)
        x2=random.randint(0,400)
        smol=Line(x,0,x2,400,fill='white',lineWidth=1)
        smolLasers.add(smol)
        
    # wave attack in the center that messes with gravity
    def circleAttack():
        for meteor in meteors:
            circ=Circle(meteor.centerX,meteor.centerY,1,fill=None,border='red')
            circs.add(circ)
            
    # giant spinning pentagons of death (i hate these)
    def plasmaCutter():
        plasma=RegularPolygon(boss.centerX,boss.centerY,25,5,fill=None,border='red',borderWidth=3)
        plasma.dx=random.randint(-2,2)
        plasma.dy=random.randint(-2,2)
        plasmas.add(plasma)
        
    # massive pillar that just 1 taps
    def megaPillar(x):
        pillar=Rect(x,-500,50,200,fill='gray',align='center')
        pillar.dx=0
        pillar.dy=0
        pillars.add(pillar)
        
    # coordinated laser
    def coordLaser(x1,y1,x2,y2):
        cl=Line(x1,y1,x2,y2,fill='white',lineWidth=1)
        coordLasers.add(cl)
        
    # lightning bolt attack
    def lightning(x):
        start=rounded(x)
        one=Line(start,-20,random.randint(start-80,start+80),random.randint(120,160),fill='white',lineWidth=10)
        two=Line(one.x2,one.y2-5,random.randint(start-80,start+80),random.randint(240,320),fill='white',lineWidth=9)
        three=Line(two.x2,two.y2-5,random.randint(start-80,start+80),420,fill='white',lineWidth=8)
        lightnings.add(one)
        lightnings.add(two)
        lightnings.add(three)
        
    # traces a path for the small lasers and moves them along that path
    def smallestLasers(x_or_y,amt,speed):
        if x_or_y=='x':
            x=400/amt
            y=0
            for i in range(amt):
                griddy=Line(x*i,y,x*i,400,fill='white',lineWidth=1,opacity=25)
                grid.add(griddy)
                smollest=Line(x*i,-100,x*i,-90,fill='red',lineWidth=3)
                smollest.dx=0
                smollest.dy=speed
                smollestg.add(smollest)
                
        if x_or_y=='y':
            x=0
            y=400/amt
            for i in range(amt):
                griddy=Line(x,y*i,400,y*i,fill='white',lineWidth=1,opacity=25)
                grid.add(griddy)
                smollest=Line(-100,y*i,-90,y*i,fill='red',lineWidth=3)
                smollestg.add(smollest)
                smollest.dx=speed
                smollest.dy=0
                
    # one single small laser that's really annoying if you don't know it's there
    def cheapshot():
        cheap=Line(player.centerX,-50,player.centerX,-45,fill='red',lineWidth=3,opacity=60)
        cheaps.add(cheap)
        
    # a laser that is just a wall
    def laserwall(x1,y1,x2,y2,size):
        lw=Line(x1,y1,x2,y2,fill='white',lineWidth=1)
        lw.size=size
        lws.add(lw)
        
    # pattern attack that can move in different directions with different angles
    def how(x1,y1,amt,dir,speed,dx,dy):
        for i in range(amt):
            i+=1
            x,y=getPointInDir(x1,y1,(dir*90)+((90/amt)*i),500)
            pattern=Line(x1,y1,x,y,fill='white',opacity=3)
            pattern.dx=dx
            pattern.dy=dy
            pattern.switch=False
            pattern.speed=speed
            patterns.add(pattern)
            
    # a giant white orb that just hides everything
    def obliteration(x,y,size):
        obl=Circle(x,y,(size/240),fill='white',opacity=0)
        obl.size=size
        obl.switch=False
        obls.add(obl)
        
    # making an ai that runs all the attacks and that changes if cfth is on
    def ai():
        if app.circleAttacks==True and app.cryFromTheHeavens==False:
            if app.steps%30==0:
                circleAttack()
                
        elif app.circleAttacks==False:
            gravitateAt.value='bottom'
        
        if app.attacking==False:
            if app.cryFromTheHeavens==False:
                p=random.randint(1,6)
                if p==1:
                    app.wait=app.steps+300//app.level
                    createLasers()
                    
                if p==2:
                    app.wait=app.steps+100//app.level
                    createDarts()
                    
                if p==3:
                    app.wait=app.steps+50//app.level
                    for i in range(5):
                        smallLasers()
                        
                if p==4:
                    app.wait=app.steps+300//app.level
                    app.circleAttacks=True
                    
                if p==5:
                    app.wait=app.steps+100//app.level
                    for i in range(5):
                        plasmaCutter()
                        
                if p==6:
                    app.wait=app.steps+100//app.level
                    megaPillar(player.centerX)
                    
                app.attacking=True
                    
            if app.cryFromTheHeavens==True:
                if app.steps==1:
                    label.visible=True
                    playerHP.value=0
                    
                if app.steps==60:
                    label.visible=False
                    coordLaser(0,0,0,400)
                    coordLaser(400,0,400,400)
                
                if app.steps==90:
                    coordLaser(0,0,390,0)
                    coordLaser(0,390,400,390)
                
                if app.steps==90:
                    smallestLasers('x',5,6)
                
                if app.steps==120:
                    for i in range(4):
                        megaPillar(50*i)
                
                if app.steps==200:
                    smallestLasers('y',10,6)
                
                if app.steps==230:
                    for i in range(10):
                        smallLasers()
                
                if app.steps==360:
                    label.visible=True
                    label.value='What?'
                    cheapshot()
                
                if app.steps==450:
                    label.value='You\'re still alive...'
                
                if app.steps==490:
                    coordLaser(player.centerX,0,player.centerX,400)
                
                if app.steps==700:
                    label.value='how is this possible?'
                    for i in range(5):
                        coordLaser(20+i*80,0,10+i*80,400)
                
                if app.steps==760:
                    for i in range(5):
                        coordLaser(20+i*80,0,30+i*80,400)
                
                if app.steps==1000:
                    label.value='NO!'
                    createLasers()
                
                if app.steps==1120:
                    label.value='YOU CAN\'T WIN'
                
                if app.steps==1180:
                    label.visible=False
                
                if app.steps==1240:
                    label.visible=True
                    label.value='DON\'T DO THIS'
                    for laser in lasers:
                        laser.opacity=95
                
                if app.steps==1500:
                    label.value='I WON\'T LET YOU'
                
                for i in range(20):
                    if app.steps==(1500+(5*i)):
                        lightning(50)
                        lightning(350)
                
                if app.steps==1800:
                    label.visible=False
                    smallestLasers('y',10,10)
                
                for i in range(5):
                    if app.steps==(1900+(30*i)):
                        coordLaser(player.centerX,0,player.centerX,400)
                
                if app.steps==2250:
                    for i in range(5):
                        plasmaCutter()
                    laserwall(400,0,400,400,100)
                    laserwall(0,0,0,400,100)
                
                if app.steps==2500:
                    label.visible=True
                    label.value='how are you not dead?'
                
                if app.steps==2620:
                    label.value='this can\'t be possible...'
                
                if app.steps==2680:
                    label.visible=False
                    for i in range(5):
                        megaPillar(40+(80*i))
                
                if app.steps==2800:
                    laserwall(100,0,100,400,150)
                    laserwall(300,0,300,400,150)
                
                if app.steps==3000:
                    laserwall(0,100,400,100,150)
                    laserwall(0,300,400,300,150)
                
                if app.steps==3120:
                    label.visible=True
                    label.value='Impossible.'
                
                if app.steps==3180:
                    gravityOn(True,'bottom')
                    how(0,0,6,1,0,0,0)
                    how(400,0,6,2,0,0,0)
                    how(0,400,6,4,0,0,0)
                    how(400,400,6,3,0,0,0)
                
                if app.steps==3500:
                    how(0,0,7,1,0.1,0,0)
                    how(400,0,7,2,0.1,0,0)
                    how(0,400,7,4,0.1,0,0)
                    how(400,400,7,3,0.1,0,0)
                
                if app.steps==3800:
                    how(0,0,7,1,-0.1,0,0)
                    how(400,0,7,2,-0.1,0,0)
                    how(0,400,7,4,-0.1,0,0)
                    how(400,400,7,3,-0.1,0,0)
                
                if app.steps==4100:
                    gravityOn(False,'bottom')
                
                if app.steps==4200:
                    label.value='a worthy opponent'
                
                if app.steps==4290:
                    label.value='needs a worthy battle.'
                
                if app.steps==4380:
                    label.value='prepare.'
                
                if app.steps==4500:
                    app.background=rgb(91,60,110)
                    label.visible=False
                    megaPillar(player.centerX)
                    laserwall(0,0,400,400,50)
                    laserwall(400,0,0,400,50)
                
                if app.steps>4560 and app.steps<4690:
                    if app.steps%30==0:
                        circleAttack()
                
                if app.steps==4700:
                    gravitateAt.value='bottom'
                
                if app.steps==4760:
                    gravityOn(True,'bottom')
                    how(200,200,5,1,0.1,0,0)
                    how(200,200,5,2,0.1,0,0)
                    how(200,200,5,3,0.1,0,0)
                    how(200,200,5,4,0.1,0,0)
                    laserwall(0,0,0,400,50)
                    laserwall(400,0,400,400,50)
                    laserwall(0,400,400,400,50)
                    laserwall(0,0,400,0,50)
                
                if app.steps==4900:
                    how(200,200,5,1,-0.1,0,0)
                    how(200,200,5,2,-0.1,0,0)
                    how(200,200,5,3,-0.1,0,0)
                    how(200,200,5,4,-0.1,0,0)
                
                if app.steps==5000:
                    smallestLasers('x',10,10)
                
                if app.steps==5150:
                    gravityOn(False,'bottom')
                
                if app.steps==5200:
                    for i in range(5):
                        coordLaser(40+(i*80),0,50+(i*80),400)
                
                if app.steps==5240:
                    for i in range(8):
                        coordLaser(10+(i*80),0,20+(i*80),400)
                
                if app.steps==5400:
                    gravityOn(True,'bottom')
                    how(0,0,6,1,0.1,0,0)
                    how(400,400,6,3,-0.1,0,0)
                
                if app.steps==5460:
                    how(0,400,6,0,-0.2,0,0)
                    how(400,0,6,2,0.2,0,0)
                
                if app.steps==5700:
                    gravityOn(False,'bottom')
                    smallestLasers('x',10,10)
                    smallestLasers('y',5,10)
                
                if app.steps>5760 and app.steps<5920:
                    if app.steps%30==0:
                        app.tempx+=2
                        megaPillar((app.tempx*40)-35)
                
                if app.steps==6000:
                    app.background=rgb(45,66,44)
                    label.visible=True
                    label.value='wow.'
                
                if app.steps==6090:
                    label.value='you think you can beat me?'
                
                if app.steps==6180:
                    label.value='no.'
                
                if app.steps==6270:
                    label.visible=False
                    boss.visible=False
                    for meteor in meteors:
                        meteor.visible=False
                
                if app.steps==6360:
                    gravityOn(True,'bottom')
                    how(0,0,20,1,0.1,0,0)
                    how(0,0,20,1,-0.1,0,0)
                    how(400,400,20,3,0.1,0,0)
                    how(400,400,20,3,-0.1,0,0)
                
                if app.steps==6600:
                    for i in range(4):
                        i+=1
                        how(200,200,10,i,-0.3,0,0)
                
                if app.steps==6800:
                    gravityOn(True,'bottom')
                    for i in range(2):
                        i+=1
                        how(0,200,10,i,-0.2,0,0)
                        how(400,200,10,i+2,-0.2,0,0)
                    laserwall(80,0,80,400,190)
                    laserwall(320,0,320,400,190)
                
                if app.steps==7000:
                    for i in range(4):
                        x=random.randint(50,350)
                        y=random.randint(50,350)
                        for t in range(4):
                            t+=1
                            how(x,y,3,t,0,0,0)
                
                if app.steps==7200:
                    for i in range(4):
                        x=random.randint(50,350)
                        y=random.randint(50,350)
                        for t in range(4):
                            t+=1
                            how(x,y,3,t,0,0,0)
                
                if app.steps>7500 and app.steps<7880:
                    gravityOn(True,'bottom')
                    if player.centerX>200:
                        player.dx-=1.5
                    
                    elif player.centerX<200:
                        player.dx+=1.5
                    
                    elif player.centerX==200:
                        player.dx=player.dx/3
                        pass
                    
                    if player.centerY>200:
                        player.dy-=1.5
                    
                    elif player.centerY<200:
                        player.dy+=1.5
                    
                    elif player.centerY==200:
                        player.dy=player.dy/3
                        pass
                
                if app.steps==7800:
                    coordLaser(0,200,400,200)
                
                if app.steps==8100:
                    label.visible=True
                    label.value='JUST DIE ALREADY'
                
                if app.steps==8300:
                    label.value='actually..'
                
                if app.steps==8500:
                    label.value='do you see that?'
                    label.size=27
                
                if app.steps==8620:
                    label.value='to your sides?'
                    rbttr.visible=True
                    rbttr2.visible=True
                
                if app.steps==8700:
                    label.value='this won\'t hurt at all.'
                
                if app.steps==8730:
                    rbttr.start=True
                
                if app.steps>8730 and app.steps<9300:
                    rbttr.centerX+=rbttr.dx
                    rbttr.centerY+=rbttr.dy
                    rbttr2.centerX+=rbttr2.dx
                    rbttr2.centerY+=rbttr2.dy
                    if app.steps%118==0:
                        lightning(rbttr2.centerX)
                        
                    if app.steps%120==0:
                        for i in range(4):
                            i+=1
                            how(rbttr.centerX,rbttr.centerY,3,i,-0.1,0,0)
                            how(rbttr.centerX,rbttr.centerY,3,i,0.1,0,0)
                            
                if app.steps==9500:
                    gravityOn(False,'bottom')
                    label.value='for my last trick.'
                    rbttr.visible=False
                    rbttr2.visible=False
                
                if app.steps==9560:
                    label.value='I have a surprise.'
                
                if app.steps==9620:
                    label.value='enjoy.'
                    obliteration(200,200,400)
                
                if app.steps==9940:
                    app.background=rgb(130,56,57)
                    cheapshot()
                    for obj in sides:
                        obj.visible=False
                    label.visible=False
                
                if app.steps==10500:
                    label.visible=True
                    label.value='how?'
                
                if app.steps==10600:
                    label.value='how are you so strong?'
                    obliteration(0,0,30)
                    obliteration(400,0,30)
                    obliteration(0,400,30)
                    obliteration(400,400,30)
                
                if app.steps==11000:
                    obliteration(200,200,600)
                    obliteration(200,200,500)
                    obliteration(200,200,400)
                    obliteration(200,200,300)
                
                if app.steps==11400:
                    label.visible=False
                
                if app.steps==11700:
                    label.visible=False
                    label.value='impossible.'
                    for i in range(len(label.value)):
                        char=Label(label.value[i],100+(i*20),300,size=27,fill='white')
                        char.dx=random.randint(-2,2)/2.2
                        char.dy=random.randint(-2,2)/2.2
                        chars.add(char)
                
                if app.steps>12000 and app.steps<12200:
                    for char in chars:
                        if char.centerX>190:
                            char.dx-=0.1
                        
                        if char.centerX<210:
                            char.dx+=0.1
                        
                        if char.centerY>190:
                            char.dy-=0.1
                        
                        if char.centerY<210:
                            char.dy+=0.1
                        
                        if char.centerX==200:
                            chars.remove(char)
                        
                        if char.centerY==200:
                            chars.remove(char)
                
                if app.steps>12200 and app.steps<12259:
                    for char in chars:
                        if char.opacity>2:
                            char.opacity-=2
                        
                        else:
                            chars.remove(char)
                if app.steps==12260:
                    Rect(0,0,400,400,fill='green',opacity=50)
                    
                    if app.invincibility==False:
                        Label('Cry From The Heavens',200,200,fill='white',size=30,align='center',bold=True)
                        Label('--< Complete >--',200,250,fill='white',size=40,align='center',bold=True)
                    
                    if app.invincibility==True:
                        Label('Cry From The Heavens',200,200,fill='white',size=30,align='center',bold=True)
                        Label('--< Cheater >--',200,250,fill='white',size=40,align='center',bold=True)
                    
                    timer.size=20
                    timer.bold=True
                    timer.toFront()
                    timer.value='Survived '+timer.value+' seconds'
                    credits()
                    app.stop()
                
                pass
            
            
        if app.attacking==True:
            
            if app.wait<=app.steps:
                app.attacking=False
                
                if app.circleAttacks==True:
                    app.circleAttacks=False
                    gravitateAt.value='bottom'
                
                for laser in lasers:
                    if laser.opacity>5:
                        laser.opacity=95
                        
                        
                        
                        
                        
                        
                        
                        
    # every step update everything
    def onStep():
        # important stuff
        currentTime.value=time.time()
        player.toFront()
        playerHP.toFront()
        app.steps+=1
        steps.value=app.steps
        # gravity
        
        if gravity.value==True:
            if gravitateAt.value=='bottom':
        
                if player.centerY<390:
                    player.dy+=gravitySpeed
        
            if gravitateAt.value=='right':
                if player.centerX<390:
                    player.dx+=gravitySpeed
            
            if gravitateAt.value=='left':
                if player.centerX>10:
                    player.dx-=gravitySpeed
            
            if gravitateAt.value=='top':
                if player.centerY>10:
                    player.dy-=gravitySpeed
    
        if gravity.value==False:
            player.dx=player.dx/1.03
            player.dy=player.dy/1.03
        
        # player dx and dy
        player.centerY+=player.dy
        player.centerX+=player.dx
        # collisions for walls
        for i in range(1):
            if player.centerY>390:
                player.centerY=390
                hitGroundRecently.value=True
                
            if player.centerY<10:
                player.centerY=10
                hitGroundRecently.value=True
                
            if player.centerX>390:
                player.centerX=390
                hitGroundRecently.value=True
                
            if player.centerX<10:
                player.centerX=10
                hitGroundRecently.value=True
                
        # bouncing and stopping for walls
        for i in range(1):
            if player.centerX==10:
                player.dx=-player.dx/3
            
            if player.centerX==390:
                player.dx=-player.dx/3
            
            if player.centerY==10:
                player.dy=-player.dy/3
            
            if player.centerY==390:
                player.dy=-player.dy/3
            
            if gravitateAt.value=='bottom':
                if player.centerY==390:
                    player.dx=player.dx/1.5
            
            if gravitateAt.value=='right':
                if player.centerX==390:
                    player.dy=player.dy/1.5
            
            if gravitateAt.value=='left':
                if player.centerX==10:
                    player.dy=player.dy/1.5
            
            if gravitateAt.value=='top':
                if player.centerY==10:
                    player.dx=player.dx/1.5
                    
        # shadows and particles
        if playerTrail==True:
            if app.steps%playerTrailsPerFrame==0:
                playerShadow=Rect(player.centerX,player.centerY,20,20,opacity=70,align='center',fill=player.fill)
                shadows.add(playerShadow)
                
        # player trail end
        for playerShadow in shadows:
            if playerShadow.opacity>0:
                playerShadow.opacity-=5
                playerShadow.width-=1
                playerShadow.height-=1
                playerShadow.centerX+=0.5
                playerShadow.centerY+=0.5
                
            else:
                shadows.remove(playerShadow)
                
        # player Shadow end
        for i in range(1):
            if particlesOn==True:
                if (player.dx>3 and player.centerX<=11):
                    addParticles(player,0,5,-5,5,playerColor,2,5,100)
                
                if (player.dy>3 and player.centerY<=11):
                    addParticles(player,-5,5,0,5,playerColor,2,5,100)
                
                if (player.dx<-3 and player.centerX>=389):
                    addParticles(player,-5,0,-5,5,playerColor,2,5,100)
                
                if (player.dy<-3 and player.centerY>=389):
                    addParticles(player,-5,5,-5,0,playerColor,2,5,100)
                    
        # particles for sides
        updateParticles()
        # boss stuff
        updateMeteors()
        updateAttacks()
        ai()
        # timer for the seconds survived
        timer.value=str(app.steps//60)
        playerHit('update')
        # player doublejump
        if player.centerY>350 or player.centerX>350 or player.centerX<40 or player.centerY<70 and doublejump.value==False:
            doublejump.value=True
            
        #death message
        if playerHP.value<0:
            Rect(0,0,400,400,fill='red',opacity=50)
            Label('YOU DIED LOL',200,200,fill='white',size=40,align='center',bold=True)
            timer.size=20
            timer.bold=True
            timer.toFront()
            timer.value='Survived '+timer.value+' seconds'
            app.stop()
            
        # make player hp the center of the player
        sides.toBack()
        if app.cryFromTheHeavens==False:
            playerHP.centerX=player.centerX
            playerHP.centerY=player.centerY
            
        else:
            dodgeCount.toFront()
            dodgeCount.fill='tomato'
            dodgeCount.centerX=player.centerX
            dodgeCount.centerY=player.centerY
            dodgeCount.value=app.dashes
            
        obls.toFront()
        #### end of onstep, onto key movements
    # keys
    def onKeyPress(key):
        if key==('w'):
            if canJump==True and gravity.value==True:
                if player.centerY>350 or player.centerX>350 or player.centerX<40 or player.centerY<70:
                    if gravitateAt.value=='bottom':
                        player.dy=-jumpHeight
                        
                elif doublejump.value==True:
                    if gravitateAt.value=='bottom':
                        player.dy=-jumpHeight
                        doublejump.value=False
                        addParticles(player,-5,5,-5,5,'lightGray',2,5,100)
                        
        if key=='a':
            if canJump==True and gravity.value==True:
                if player.centerY>350 or player.centerX>350 or player.centerX<40 or player.centerY<70:
                    if gravitateAt.value=='right':
                        player.centerX-=2
                        player.dx=-jumpHeight
                        
                elif doublejump.value==True:
                    if gravitateAt.value=='right':
                        player.centerX-=2
                        player.dx=-jumpHeight
                        doublejump.value=False
                        addParticles(player,-5,5,-5,5,'lightGray',2,5,100)
                        
        if key=='d':
            if canJump==True and gravity.value==True:
                if player.centerY>350 or player.centerX>350 or player.centerX<40 or player.centerY<70:
                    if gravitateAt.value=='left':
                        player.centerX+=2
                        player.dx=jumpHeight
                        
                elif doublejump.value==True:
                    if gravitateAt.value=='left':
                        player.centerX+=2
                        player.dx=jumpHeight
                        doublejump.value=False
                        addParticles(player,-5,5,-5,5,'lightGray',2,5,100)
                        
        if key=='s':
            if canJump==True and gravity.value==True:
                if player.centerY>350 or player.centerX>350 or player.centerX<40 or player.centerY<70:
                    if gravitateAt.value=='top':
                        player.centerY+=2
                        player.dy=jumpHeight
                        
                elif doublejump.value==True:
                    if gravitateAt.value=='top':
                        player.centerY+=2
                        player.dy=jumpHeight
                        doublejump.value=False
                        addParticles(player,-5,5,-5,5,'lightGray',2,5,100)
                        
        #keys for gravity switching
        if debug==True:
            if key=='up':
                gravitateAt.value='top'
                
            if key=='down':
                gravitateAt.value='bottom'
                
            if key=='left':
                gravitateAt.value='left'
                
            if key=='right':
                gravitateAt.value='right'
                
            if key=='r':
                if gravity.value==True:
                    gravityOn(True,'bottom')
                    
                else:
                    gravityOn(False,'bottom')
                    
            if key=='k':
                createLasers()
                createDarts()
                smallLasers()
                circleAttack()
                plasmaCutter()
                center=0
                for i in range(10):
                    center+=40
                    megaPillar(center)
                    
            if key=='t':
                createLasers()
                
        if key=='e':
            if app.dashing==False and app.dashes!=0:
                app.dashing=True
                app.end=app.steps+80
                player.fill=dashColor
                app.dashes-=1
                player.dx+=player.dx*2
                player.dy+=player.dy*2
                
        if key=='p':
            print(app.steps)
            
                
        # end
    def onKeyHold(keys):
        if 'a' in keys:
            if gravitateAt.value=='bottom' or gravitateAt.value=='top':
                player.dx+=-speed
                
            if gravitateAt.value=='left':
                player.dx-=speed
                
        if 'd' in keys:
            if gravitateAt.value=='bottom' or gravitateAt.value=='top':
                player.dx+=speed
                
            if gravitateAt.value=='right':
                player.dx-=-speed
                
        if 's' in keys:
            if gravity.value==True:
                player.dy+=speed*2
                if gravitateAt.value=='bottom':
                    player.dx=player.dx/1.5
                    
            else:
                if gravitateAt.value=='bottom':
                    player.dy+=speed
                    
        if 'w' in keys:
            if gravity.value==True:
                if gravitateAt.value=='left' or gravitateAt.value=='right':
                    player.dy+=-speed
                    
            else:
                player.dy-=speed

cmu_graphics.run()
