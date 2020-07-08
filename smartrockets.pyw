import os
import time
import random
import math
from tkinter import *

random.seed(time.time())

session = 0
if not os.path.exists('smartrockets.log'):
    with open('smartrockets.log', 'a') as log:
        log.write('type, generation, position, start, goal, hit_target, iteration, success, session')
        
with open('smartrockets.log', 'r') as log:
    for line in log.readlines():
        if len(line) > 1:
            session = int(line.split(',')[-1]) + 1

# TODO: improve the log function for rockets
# TODO: make type an attribute of rockets
# TODO: calcNovelty as a function of calcFit for each rocket
# TODO: make rockets one array 
# TODO: replace reset canvas function by just using rockets inherent reset function
# TODO: get rid of references to global variables

class rocket:
    startX = 250
    startY = 490

    height = 20
    width = 5

    upForce = -5

    def __init__(self, c, dna):
        self.stuck = False
        self.hit_target = False;

        self.dna = dna

        # forces the rockets in a particular direction at the start
        self.sideForce = 270
        self.fitness = 0
        self.novelty = 0
        self.type = 'standard'

        # These are the two points of the line associated with the rocket, bottom and top
        self.x0 = rocket.startX
        self.y0 = rocket.startY
        self.x1 = rocket.startX
        self.y1 = self.y0 + rocket.height

        # This actually creates the line
        self.visual = c.create_line(self.x0, self.y0, self.x1, self.y1, width = rocket.width, fill="white")

    def draw(self, c, current):
        self.sideForce += self.dna[current]
        self.radAngle = (self.sideForce * math.pi) / 180

        self.x0 = self.x0 + rocket.upForce * -math.cos(self.radAngle)
        self.y0 = self.y0 + rocket.upForce * -math.sin(self.radAngle)
        self.x1 = self.x0 + rocket.height * math.cos(self.radAngle)
        self.y1 = self.y0 + rocket.height * math.sin(self.radAngle)

        self.visual = c.create_line(self.x0, self.y0, self.x1, self.y1, width = rocket.width, fill = "white")

        #test collision
        #side of screen
        if self.x1 > 500 or self.x1 < 0:
            self.stuck = True
        if self.y1 > 500 or self.y1 < 0:
            self.stuck = True
        
        #obstacles
        # # original
        # if self.x1 > 150 and self.x1 < 350 and self.y1 > 240 and self.y1 < 250:
        #     self.stuck = True
        # if self.x1 > 50 and self.x1 < 150 and self.y1 > 140 and self.y1 < 150:
        #     self.stuck = True
        # if self.x1 > 350 and self.x1 < 450 and self.y1 > 140 and self.y1 < 150:
        #     self.stuck = True
        # if self.x1 > 50 and self.x1 < 150 and self.y1 > 350 and self.y1 < 360:
        #     self.stuck = True
        # if self.x1 > 350 and self.x1 < 450 and self.y1 > 350 and self.y1 < 360:
        #     self.stuck = True

        # # custom
        if self.x1 > 150 and self.x1 < 350 and self.y1 > 240 and self.y1 < 250:
            self.stuck = True
        if self.x1 > 0 and self.x1 < 150 and self.y1 > 100 and self.y1 < 110:
            self.stuck = True
        if self.x1 > 140 and self.x1 < 150 and self.y1 > 110 and self.y1 < 250:
            self.stuck = True
        # if self.x1 > 350 and self.x1 < 450 and self.y1 > 350 and self.y1 < 360:
            # self.stuck = True

        #goal
        if self.x1 > endPoint[0] - 10 and self.x1 < endPoint[0] + 10 and self.y1 > endPoint[1] - 10 and self.y1 < endPoint[1] + 10:
            self.stuck = True
            self.hit_target = True
    
    def calcFit(self):
        if self.novelty > 0:
            self.fitness = self.novelty
            return self.novelty ** 2
        self.fitness = math.sqrt((self.startX - self.x1) ** 2 + (self.startY - self.y1) ** 2)
        self.fitness = self.fitness - (math.sqrt((endPoint[0] - self.x1) ** 2 + (endPoint[1] - self.y1) ** 2))
        self.fitness = math.floor(self.fitness)

        if (self.fitness <= 0):
            self.fitness = 1

        if (self.hit_target):
            self.fitness = 750
        
        return self.fitness ** 2

    
    def reset(self, c, dna):
        self.stuck = False
        self.hit_target = False

        self.dna = dna

        self.sideForce = 270
        self.fitness = 0

        c.delete(self.visual)

        self.x0 = rocket.startX
        self.y0 = rocket.startY
        self.x1 = rocket.startX
        self.y1 = self.y0 + rocket.height
    
    def log(self):
        with open('smartrockets.log', 'a') as log:
            log.write('{}, {}, {}, {}, {}, {}, {}, {}, {}\n'.format(self.type, generationCounter, (self.x1, self.y1), (self.startX, self.startY), (endPoint[0], endPoint[1]), self.hit_target, self.fitness, successful.values(), session))

class window:

    def __init__(self):
        self.generationCounter = 1
        self.rockets = []
        self.success = False
        self.genePool = []

        self.popSize = 20
        self.lifespan = 550         

        self.numSuccesses = 0

        self.endPoint = (50, 50)
    
        self.canvas = Canvas(root, height = 500, width = 500, bg = 'black')
        self.generationText = self.canvas.create_text(10, 10, anchor = 'nw', fill = 'white', font = 20)
        self.typeText = self.canvas.create_text(200, 10, anchor = 'nw', fill = 'white', font = 20)
        self.successText = self.canvas.create_text(200, 400, anchor = 'nw', fill = 'green', font = 20)
        self.canvas.itemconfig(self.generationText, text = "generation 1")
        self.canvas.itemconfig(self.typeText, text = "standard")

        self.visualEND = canvas.create_rectangle(endPoint[0] - 10, endPoint[1] - 10, endPoint[0] + 10, endPoint[1] + 10, fill = "green")

        # original
        # visualObstacle = canvas.create_rectangle(150, 250, 350, 240, fill = "white")
        # visualObstacle2 = canvas.create_rectangle(50, 150, 150, 140, fill = "white")
        # visualObstacle3 = canvas.create_rectangle(350, 150, 450, 140, fill = "white")
        # visualObstacle4 = canvas.create_rectangle(50, 360, 150, 350, fill = "white")
        # visualObstacle5 = canvas.create_rectangle(350, 360, 450, 350, fill = "white")

        # custom
        self.visualObstacle = canvas.create_rectangle(150, 250, 350, 240, fill = "white")
        self.visualObstacle2 = canvas.create_rectangle(0, 100, 150, 110, fill = "white")
        self.visualObstacle3 = canvas.create_rectangle(140, 110, 150, 250, fill = "white")
        # visualObstacle4 = canvas.create_rectangle(350, 360, 450, 350, fill = "white")


def calcNovelty(rockets):
    novelties = {}
    for r in rockets:
        novelties[r] = 0
        for r2 in rockets:
            if r2 == r:
                continue
            novelties[r] += math.sqrt((r.x1 - r2.x1) **2 + (r.y1 - r2.y1) **2)/5000
    for key, value in novelties.items():
        value = float(value)/max(novelties.values())
    
    for r in rockets:
        r.novelty = math.floor(novelties[r] * 750)
    
    return

def initialize():
    
    global generationCounter
    global success
    global rockets
    global rocketsNov
    global rocketsRand
    global genePool
    global genePoolNov
    global genePoolRand

    generationCounter = 1
    success = False
    rockets = []
    rocketsNov = []
    rocketsRand = []
    genePool = []
    genePoolNov = []
    genePoolRand = []

    # original
    # endPoint = (250, 50)

    # custom
    

    for i in range(popSize):
        newDNA = []
        newDNANov = []
        newDNARand = []

        for j in range(lifespan):
            newDNA.append(random.uniform(-10, 10))
            newDNANov.append(random.uniform(-10, 10))
            newDNARand.append(random.uniform(-10,10))

        newRocket = rocket(canvas, newDNA)
        newRocket.type = 'standard'
        newRocketNov = rocket(canvasNov, newDNANov)
        newRocketNov.type = 'novelty'
        newRocketRand = rocket(canvasRand, newDNARand)
        newRocketRand.type = 'random'
        rockets.append(newRocket)
        rocketsNov.append(newRocketNov)
        rocketsRand.append(newRocketRand)

def reset_canvas():
    global canvas
    global canvasNov
    global canvasRand

    global rockets
    global rocketsNov
    global rocketsRand
    
    global popSize

    canvasRand.itemconfig(successTextRand, text = '')
    canvasNov.itemconfig(successTextNov, text = '')
    canvas.itemconfig(successText, text = '')

    for i in range(popSize):
        canvas.delete(rockets[i].visual)
        canvasNov.delete(rocketsNov[i].visual)
        canvasRand.delete(rocketsRand[i].visual)

# def log_generation():
#     global log
#     global generationCounter

#     global rockets
#     global rocketsNov
#     global rocketsRand

#     log.write('standard, {}, {}, {}, {}, {}, {}\n'.format((generationCounter, rockets[i].x1, rockets[i].y1), (rockets[i].startX, rockets[i].startY), (endPoint[0], endPoint[1]), rockets[i].hit_target))
#     log.write('novelty, {}, {}, {}, {}, {}, {}\n'.format((generationCounter, rockets[i].x1, rockets[i].y1), (rockets[i].startX, rockets[i].startY), (endPoint[0], endPoint[1]), rockets[i].hit_target))
#     log.write('random, {}, {}, {}, {}, {}, {}\n'.format((generationCounterrockets[i].x1, rockets[i].y1), (rockets[i].startX, rockets[i].startY), (endPoint[0], endPoint[1]), rockets[i].hit_target))
        

generationCounter = 1
rockets = []
rocketsNov = []
rocketsRand = []
genePool = []
genePoolNov = []
genePoolRand = []

successful = {}
successful['Rand'] = 0
successful['Standard'] = 0
successful['Nov'] = 0
success = False

popSize = 20
lifespan = 550

endPoint = (50,50)

root = Tk()
root.title('smart rockets')
root.resizable(False, False)
    
canvas = Canvas(root, height = 500, width = 500, bg = 'black')
canvasNov = Canvas(root, height = 500, width = 500, bg = 'black')
canvasRand = Canvas(root, height = 500, width = 500, bg = 'black')
generationText = canvas.create_text(10, 10, anchor = 'nw', fill = 'white', font = 20)
generationTextNov = canvasNov.create_text(10, 10, anchor = 'nw', fill = 'white', font = 20)
generationTextRand = canvasRand.create_text(10,10,anchor='nw',fill='white',font=20)
typeText = canvas.create_text(200, 10, anchor = 'nw', fill = 'white', font = 20)
typeTextNov = canvasNov.create_text(200, 10, anchor = 'nw', fill = 'white', font = 20)
typeTextRand = canvasRand.create_text(200, 10, anchor = 'nw', fill = 'white', font = 20)
successText = canvas.create_text(200, 400, anchor = 'nw', fill = 'green', font = 20)
successTextNov = canvasNov.create_text(200, 400, anchor = 'nw', fill = 'green', font = 20)
successTextRand = canvasRand.create_text(200, 400, anchor = 'nw', fill = 'green', font = 20)

canvas.itemconfig(generationText, text = "generation 1")
canvasNov.itemconfig(generationTextNov, text = "generation 1")
canvasRand.itemconfig(generationTextRand, text = 'generation 1')
canvas.itemconfig(typeText, text = "standard")
canvasNov.itemconfig(typeTextNov, text = "novelty")
canvasRand.itemconfig(typeTextRand, text = "random")




visualEND = canvas.create_rectangle(endPoint[0] - 10, endPoint[1] - 10, endPoint[0] + 10, endPoint[1] + 10, fill = "green")
visualENDNov = canvasNov.create_rectangle(endPoint[0] - 10, endPoint[1] - 10, endPoint[0] + 10, endPoint[1] + 10, fill = "green")
visualENDRand = canvasRand.create_rectangle(endPoint[0] - 10, endPoint[1] - 10, endPoint[0] + 10, endPoint[1] + 10, fill = "green")

# original
# visualObstacle = canvas.create_rectangle(150, 250, 350, 240, fill = "white")
# visualObstacle2 = canvas.create_rectangle(50, 150, 150, 140, fill = "white")
# visualObstacle3 = canvas.create_rectangle(350, 150, 450, 140, fill = "white")
# visualObstacle4 = canvas.create_rectangle(50, 360, 150, 350, fill = "white")
# visualObstacle5 = canvas.create_rectangle(350, 360, 450, 350, fill = "white")

# custom
visualObstacle = canvas.create_rectangle(150, 250, 350, 240, fill = "white")
visualObstacle2 = canvas.create_rectangle(0, 100, 150, 110, fill = "white")
visualObstacle3 = canvas.create_rectangle(140, 110, 150, 250, fill = "white")
# visualObstacle4 = canvas.create_rectangle(350, 360, 450, 350, fill = "white")

visualObstacleNov = canvasNov.create_rectangle(150, 250, 350, 240, fill = "white")
visualObstacleNov2 = canvasNov.create_rectangle(0, 100, 150, 110, fill = "white")
visualObstacleNov3 = canvasNov.create_rectangle(140, 110, 150, 250, fill = "white")

visualObstacleRand = canvasRand.create_rectangle(150, 250, 350, 240, fill = "white")
visualObstacleRand2 = canvasRand.create_rectangle(0, 100, 150, 110, fill = "white")
visualObstacleRand3 = canvasRand.create_rectangle(140, 110, 150, 250, fill = "white")


initialize()


while 1 and sum(successful.values()) < 100:
    #run through simulation
    for i in range(lifespan):
        all_stuck = True
        all_stuckNov = True
        all_stuckRand = True

        for j in range(popSize):
            if rockets[j].stuck == False:
                canvas.delete(rockets[j].visual)
                rockets[j].draw(canvas, i)

                canvas.pack(side = 'left')
                root.update_idletasks()
                root.update()

                all_stuck = False
            
            if rockets[j].hit_target == True:
                successful['Standard'] += 1
                canvas.itemconfig(successText, text = 'SUCCESS')
                print('standard wins! - generation {}'.format(generationCounter))
                success = True
                break

            if rocketsNov[j].stuck == False:
                canvasNov.delete(rocketsNov[j].visual)
                rocketsNov[j].draw(canvasNov, i)

                canvasNov.pack(side = 'left')
                root.update_idletasks()
                root.update()

                all_stuckNov = False
            
            if rocketsNov[j].hit_target == True:
                successful['Nov'] += 1
                canvasNov.itemconfig(successTextNov, text = 'SUCCESS')
                print('novelty wins! - generation {}'.format(generationCounter))
                success = True
                break

            if rocketsRand[j].stuck == False:
                canvasRand.delete(rocketsRand[j].visual)
                rocketsRand[j].draw(canvasRand, i)

                canvasRand.pack(side = 'left')
                root.update_idletasks()
                root.update()

                all_stuckRand = False
            
            if rocketsRand[j].hit_target == True:
                successful['Rand'] += 1
                canvasRand.itemconfig(successTextRand, text = 'SUCCESS')
                print('random wins! - generation {}'.format(generationCounter))
                success = True
                break

        if (all_stuck == False or all_stuckNov == False or all_stuckRand == False):
            time.sleep(0.01)

        if(success):
            break

    

    # calc novelty
    calcNovelty(rocketsNov)

    #calc fitness
    for i in range(popSize):
        for j in range(rockets[i].calcFit()):
            genePool.append(rockets[i].dna)
        for j in range(rocketsNov[i].calcFit()):
            genePoolNov.append(rocketsNov[i].dna)

    for i in range(popSize):
        rockets[i].log()
        rocketsNov[i].log()
        rocketsRand[i].log()
    time.sleep(1)
    
    if (success):
        reset_canvas()
        initialize()
        continue

    #create new population
    for i in range(popSize):
        newDNA = []
        newDNANov = []

        parent1 = random.choice(genePool)
        parent2 = random.choice(genePool)

        parentNov1 = random.choice(genePoolNov)
        parentNov2 = random.choice(genePoolNov)

        while parent1 == parent2:
            parent2 = random.choice(genePool)

        while parentNov1 == parentNov2:
            parentNov2 = random.choice(genePoolNov)

        for j in range(lifespan):
            parents = [parent1[j], parent2[j]]
            _ = random.choice(parents)
            newDNA.append(_)
            parentsNov = [parentNov1[j], parentNov2[j]]
            _nov = random.choice(parentsNov)
            newDNANov.append(_nov)

        #mutate
        if random.randint(0, 2) == 0:
            for j in range(math.floor(lifespan / 20)):
                randIndex = random.randint(0, lifespan - 1)
                newDNA.pop(randIndex)
                newDNA.insert(randIndex, random.uniform(-10, 10))
        
        if random.randint(0, 2) == 0:
            for j in range(math.floor(lifespan / 20)):
                randIndex = random.randint(0, lifespan - 1)
                newDNANov.pop(randIndex)
                newDNANov.insert(randIndex, random.uniform(-10, 10))

        rockets[i].reset(canvas, newDNA)
        rocketsNov[i].reset(canvasNov, newDNANov)
        newDNARand = []

        for j in range(lifespan):
            newDNARand.append(random.uniform(-10,10))

        rocketsRand[i].reset(canvasRand, newDNARand)

    genePool.clear()
    genePoolNov.clear()
    genePoolRand.clear()
    generationCounter = generationCounter + 1
    canvas.itemconfig(generationText, text = ("generation " + str(generationCounter)))
    canvasNov.itemconfig(generationTextNov, text = ("generation " + str(generationCounter)))
    canvasRand.itemconfig(generationTextRand, text = ("generation " + str(generationCounter)))

print(successful)