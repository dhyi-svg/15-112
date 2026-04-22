from cmu_graphics import *
import random, math

def onAppStart(app):
    app.centerx = app.width//2
    app.centery = app.height//2
    app.stars = stars(app)
    app.homeScreen = True
    app.characterSelect = False
    app.character = None
    app.gameStarted = False
    app.lineX, app.lineY = None, None
    app.asteroids = []
    app.lasers = []
    app.timeCounter = 0
    app.difficulty = 0
    app.stepsPerSecond = 30
    app.hp = 10
    app.score = 0
    app.gameOver = False
    
def stars(app):
    result = []
    for i in range(7):
        cx = app.width/6*((random.randint(0,7))) + 30
        cy = app.height/6*(random.randint(0,7)) + 30
        angle = random.randint(0,360)
        result.append((cx,cy,angle))
    return result

def background(app):
    backdrop = rgb(30, 40, 55)
    drawRect(0,0,app.width,app.height,fill = backdrop)
    for cx,cy,angle in app.stars:
        drawStar(cx,cy,10, 4, rotateAngle = angle, roundness = 50, fill = 'gold')
    drawOval(app.centerx, app.height, app.width, app.height/(2), fill = 'coral')

def startScreen(app):
    drawLabel('SHOOT YOUR BOSS!', app.centerx, app.height*2//5, size = app.width*3//40, font = 'Orbitron', fill = 'white', bold = True)
    drawRect(app.centerx, app.height*3//5, app.centerx, app.height*3//20, align = 'center', fill = 'moccasin')
    drawLabel('START', app.centerx, app.height*3//5, size = app.width//20, align = 'center', font = 'Orbitron')

def characterSelect(app):
    drawLabel('CHOOSE THE BOSS', app.centerx, app.height//8, size = app.width*3//40, font = 'Orbitron', fill = 'white', bold = True)
    drawImage('kosbie.png', app.centerx - 60, app.centery - 70, align = 'center')
    drawImage('sands.png', app.centerx + 60, app.centery -70, align = 'center')
    drawImage('thomas.jpeg', app.centerx -60, app.centery +50, align = 'center')
    drawImage('jiao.jpg', app.centerx +60, app.centery + 50, align = 'center')

def startGame(app):
    minimum = min(app.width, app.height)
    drawCircle(app.centerx, app.height*3//4, minimum//11, fill = 'gray', border = 'black')
    drawCircle(app.centerx, app.height*3//4, minimum//16, fill = 'gray', border = 'black')
    startX = app.centerx
    startY = app.height*3//4
    ux,uy = followMouse(app,startX,startY,app.lineX,app.lineY)
    x = startX + ux * (app.width*3//20)
    y = startY + uy * (app.height*3//20)
    x1 = startX + ux * (app.width//10)
    y1 = startY + uy * (app.height//10)
    drawLine(startX,startY, x1, y1, lineWidth = app.width//40)
    drawLine(startX, startY, x, y, lineWidth = app.width/100)
    if app.score < 10:
        drawLabel(f'00{app.score}',app.centerx,app.height//6,size = app.width*3//20, fill = 'white', bold = True, font = 'Orbitron')
    elif app.score < 100:
        drawLabel(f'0{app.score}',app.centerx,app.height//6,size = app.width*3//20, fill = 'white', bold = True, font = 'Orbitron')
    else:
        drawLabel(f'{app.score}',app.centerx,app.height//6,size = app.width*3//20, fill = 'white', bold = True, font = 'Orbitron')

def endScreen(app):
    if app.hp < 1:
        drawLabel(f"GGs", app.centerx, app.height//4,size = app.width//4, fill = 'white',bold = True, align = 'center')
        drawLabel(f"Your final score was: {app.score}!", app.centerx, app.centery,size = app.width//14, fill = 'white',bold = True, font = 'Orbitron', align = 'center')
    else:
        drawLabel(f"Wow I'm impressed!", app.centerx, app.height//4,size = app.width//4, fill = 'white',bold = True)
        drawLabel(f"Your final score was: {app.score}!", app.centerx, app.centery,size = app.width//5, fill = 'white',bold = True, font = 'Orbitron')

def followMouse(app,startX,startY,mX,mY):
    dx = mX - startX
    dy = mY - startY
    length = (dx**2 + dy**2)**(0.5)
    if length > 0:
        ux = dx/length
        uy = dy/length
        return (ux,uy)
    return (1,1)

def distance(x0,y0,x1,y1):
    return((x0-x1)**2 + (y0-y1)**2)**0.5

def checkInRect(app,mouseX,mouseY,x,y,width,height):
    left = x
    top = y
    if (left)<= mouseX <= (left+width) and (top) <= mouseY <=(top+height):
        return True
    return False


def checkInCircle(x0,y0,r,x1,y1):
    return (distance(x0,y0,x1,y1) <= r)

def homeScreenCheck(app,mouseX,mouseY):
    if checkInRect(app,mouseX, mouseY, 
                   app.centerx-app.centerx//2, app.height*3//5-app.height*3//40, app.centerx, app.height*3//20):
            app.characterSelect = True
            app.homeScreen = False

def checkCharacter(app,mouseX,mouseY):
    if checkInRect(app,mouseX,mouseY,
                   (app.centerx - 60)-50,(app.centery - 70)-50,
                   100,100):
        return 'kosbie'
    elif checkInRect(app,mouseX,mouseY,
                     (app.centerx + 60) - 50, (app.centery - 70) - 50,
                     100,100):
        return 'sands'
    elif checkInRect(app,mouseX,mouseY,
                     (app.centerx - 60)-50, (app.centery + 50) - 50,
                     100,100):
        return 'thomas'
    elif checkInRect(app,mouseX,mouseY,
                     (app.centerx + 60) - 50, (app.centery + 50)-50,
                     100,100):
        return 'jiao'


def checkGameEnd(app):
    if app.hp < 1:
        app.gameStarted = False
        app.gameEnded = True

def onStep(app):
    app.centerx = app.width//2
    app.centery = app.height//2
    if app.gameStarted:
        app.timeCounter += 1
        moveLaser(app)
        if app.timeCounter%300 ==0:
            app.difficulty += 1
        generateAsteroid(app)
        if app.timeCounter % 5 == 0:
            moveAsteroids(app)
        removeAsteroids(app)
        removeLaser(app)
        checkGameEnd(app)
        
class Asteroid:
    def __init__(self,app):
        self.x = random.randint(0,app.width)
        self.y = -50
        self.speed = random.randint(2, 6)
        minimum = min(app.width, app.height)
        lower = minimum*3//40
        higher = minimum*3//20
        self.size = random.randint(lower, higher)
        self.color = 'gray'
        self.hit = 0

class Laser:
    def __init__(self,app,mouseX,mouseY):
        self.startX = app.centerx
        self.startY = app.height*3//4  
        ux,uy = followMouse(app,self.startX,self.startY,mouseX,mouseY)
        self.x = self.startX + ux * (app.width*3//20)
        self.y = self.startY + uy * (app.height*3//20)
        speed = app.width//40  
        self.speedx = ux * speed
        self.speedy = uy * speed
        self.color = 'red'

def generateAsteroid(app):
    if app.difficulty <= 6:
        if app.timeCounter % 120 == 0:
            app.asteroids.append(Asteroid(app)) 
    elif app.difficulty <= 9:
        if app.timeCounter % 90 == 0:
            app.asteroids.append(Asteroid(app))
    elif app.difficulty <= 15:
        if app.timeCounter % 60 == 0:
            app.asteroids.append(Asteroid(app))
    elif app.difficulty <= 21:
        if app.timeCounter % 30 == 0:
            app.asteroids.append(Asteroid(app))
    else:
        app.gameStarted = False
        app.gameEnded = True

def removeAsteroids(app):
    minimum = min(app.width,app.height)
    for asteroid in app.asteroids:
        if asteroid.y > app.height - app.height//4-4:
            asteroid.color = 'red'
        if asteroid.y > app.height - app.height//4:
            app.asteroids.remove(asteroid)
            app.hp -= 1
        for laser in app.lasers:
            if checkInCircle(asteroid.x,asteroid.y,asteroid.size,laser.x,laser.y):
                asteroid.hit += 1
                if asteroid.size <= minimum//10:
                    app.asteroids.remove(asteroid)
                    app.score += 10
                elif 40 < asteroid.size <= minimum//8:
                    if asteroid.hit < 2:
                        asteroid.color = 'yellow'
                    else:
                        app.asteroids.remove(asteroid)
                        app.score += 30
                elif asteroid.size > minimum//8:
                    if asteroid.hit < 2:
                        asteroid.color = 'yellow'
                    elif 2 <= asteroid.hit < 3:
                        asteroid.color = 'orange'
                    else:
                        app.asteroids.remove(asteroid)
                        app.score += 50
                app.lasers.remove(laser)

def moveAsteroids(app):
    for asteroid in app.asteroids:
        asteroid.y += asteroid.speed   
    
def drawAsteroids(app):
    for a in app.asteroids:
        drawCircle(a.x, a.y, a.size, fill= a.color, border='black')
        if min(app.width, app.height) < 800:
            if app.character == 'kosbie':
                drawImage('kosbie_small.png',a.x,a.y,align = 'center')
            elif app.character == 'jiao':
                drawImage('jiao_small.jpg',a.x,a.y,align = 'center')
            elif app.character == 'sands':
                drawImage('sands_small.png',a.x,a.y,align = 'center')
            elif app.character == 'thomas':
                drawImage('thomas_small.jpeg',a.x,a.y,align = 'center')
        else:
            if app.character == 'kosbie':
                drawImage('kosbie.png',a.x,a.y,align = 'center')
            elif app.character == 'jiao':
                drawImage('jiao.jpg',a.x,a.y,align = 'center')
            elif app.character == 'sands':
                drawImage('sands.png',a.x,a.y,align = 'center')
            elif app.character == 'thomas':
                drawImage('thomas.jpeg',a.x,a.y,align = 'center')
   

def generateLaser(app,mouseX,mouseY):
    if len(app.lasers) < 5:
        app.lasers.append(Laser(app,mouseX,mouseY))

def drawLasers(app):
    for laser in app.lasers:   
        drawLine(laser.startX,laser.startY,laser.x,laser.y,fill = laser.color, lineWidth = app.width//100)

def moveLaser(app):
    if app.timeCounter%3==0:
        for laser in app.lasers:
            laser.startX += laser.speedx
            laser.startY += laser.speedy
            laser.x += laser.speedx
            laser.y += laser.speedy
    
def removeLaser(app):
    for laser in app.lasers:
        if laser.startX > app.width or laser.startX < 0 or laser.startY < 0:
            app.lasers.remove(laser)

def onMouseMove(app,mouseX,mouseY):
    app.lineX, app.lineY = mouseX, mouseY

def onMousePress(app,mouseX,mouseY):
    if app.homeScreen:
        homeScreenCheck(app,mouseX,mouseY)
    elif app.characterSelect:
        app.character = checkCharacter(app,mouseX,mouseY)
        if app.character != None:
            app.characterSelect = False
            app.gameStarted = True
            app.lineX, app.lineY = app.centerx, app.height*3//5
    elif app.gameStarted:
        generateLaser(app,mouseX,mouseY)

def onKeyPress(app,key):
    if key == 'l':
        app.stepsPerSecond = 60
    elif key == 'j':
        app.stepsPerSecond = 10
    elif key == 'k':
        app.stepsPerSecond = 30

def redrawAll(app):
    background(app)
    if app.homeScreen:
        startScreen(app)
    elif app.characterSelect:
        characterSelect(app)
    elif app.gameStarted:
        startGame(app)
        drawAsteroids(app)
        drawLasers(app)
    elif app.gameEnded:
        endScreen(app)


def main():
    runApp()

main()