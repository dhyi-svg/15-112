from cmu_graphics import *
import random

def onAppStart(app):
    app.centerx = app.width//2
    app.centery = app.width//2
    app.stars = stars(app)
    app.homeScreen = True
    app.characterSelect = False
    app.characterSelected = None
    app.gameStarted = False
    app.characters = ['kosbie', 'sands', 'thomas', 'jiao']
    app.lineX, app.lineY = None, None
    app.asteroids = []
    app.timeCounter = 0
    app.difficulty = 0
    app.stepsPerSecond = 30
    
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
    drawLabel('SHOOT YOUR BOSS!', app.centerx, app.centery -30, size = 30, font = 'orbitron', fill = 'white', bold = True)
    drawRect(app.centerx, app.centery + 40, app.width//2, 60, align = 'center', fill = 'moccasin')
    drawLabel('START', app.centerx, app.centery + 40, size = 25, align = 'center', font = 'orbitron')

def characterSelect(app):
    drawLabel('CHOOSE THE BOSS', app.centerx, app.centery//4, size = 30, font = 'orbitron', fill = 'white', bold = True)
    drawImage('kosbie.png', app.centerx - 60, app.centery - 70, align = 'center')
    drawImage('sands.png', app.centerx + 60, app.centery -70, align = 'center')
    drawImage('thomas.jpeg', app.centerx -60, app.centery +50, align = 'center')
    drawImage('jiao.jpg', app.centerx +60, app.centery + 50, align = 'center')

def startGame(app):
    print('y')
    drawCircle(app.width//2,app.height*3//4, app.width//11, fill = 'gray', border = 'black')
    startX = app.width//2
    startY = app.height*3//4 
    dx = startX - app.lineX
    dy = startY - app.lineY
    length = (dx**2 + dy**2)**(0.5)
    ux = dx/length
    uy = dy/length
    x = startX - ux * (app.width*3//20)
    y = startY - uy * (app.height*3//20)
    x1 = startX - ux * (app.width//10)
    y1 = startY - uy * (app.height//10)
    drawLine(startX,startY, x1, y1, lineWidth = 10)
    drawLine(startX, startY, x, y, lineWidth = 4)

def checkInRect(app,mouseX,mouseY,x,y,width,height):
    left = x
    top = y
    if (left)<= mouseX <= (left+width) and (top) <= mouseY <=(top+height):
        return True
    return False

def homeScreenCheck(app,mouseX,mouseY):
    if checkInRect(app,mouseX, mouseY, 
                   app.centerx-app.width//4, 
                   app.centery+40-60, 
                   app.width//2, 60,):
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


def onStep(app):
    app.timeCounter += 1
    if app.timeCounter > 300:
        app.difficulty += 1
    generateAsteroid(app)
    if app.timeCounter % 5 == 0:
        moveAsteroids(app)


def generateAsteroid(app):
    if app.difficulty <= 6:
        if app.timeCounter % 120 == 0:
            app.asteroids.append(Asteroid(app)) 
        
class Asteroid:
    def __init__(self,app):
        self.x = random.randint(0,app.width)
        self.y = -50
        self.speed = random.randint(2, 6)
        self.size = random.randint(20, 60)

def moveAsteroids(app):
    for asteroid in app.asteroids:
        asteroid.y += asteroid.speed   
        if asteroid.y > app.height - app.height//4:
            app.asteroids.remove(asteroid)
    
def drawAsteroids(app):
    for a in app.asteroids:
        drawCircle(a.x, a.y, a.size, fill='gray', border='black')
   

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
            app.lineX, app.lineY = app.width//2, app.height*3//5

def redrawAll(app):
    background(app)
    if app.homeScreen:
        startScreen(app)
    elif app.characterSelect:
        characterSelect(app)
    elif app.gameStarted:
        startGame(app)
        drawAsteroids(app)



def main():
    runApp()

main()
