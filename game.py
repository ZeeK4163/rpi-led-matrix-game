
from samplebase import SampleBase
from pynput import mouse
from utils import map0, earthquake0, tornado0, tornado1
import time
import threading
import random
import numpy as np
import threading

class TurnState():
    e = threading.Event()
    run = True
    lastDisaster = None

class Colors():
    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (51, 204, 51)
    darkGreen = (51, 153, 51)
    blue = (51, 153, 255)
    darkBlue = (0, 51, 204)
    orange = (201, 121, 0)
    grey = (156, 156, 156)

class Game(SampleBase):
    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)

    def run(self):
        #creo la mappa
        defaultMapScreenCanvas = self.matrix.CreateFrameCanvas()
        offScreenCanvas = self.matrix.CreateFrameCanvas()
        whiteCanvas = self.matrix.CreateFrameCanvas()
        blankCanvas = self.matrix.CreateFrameCanvas()

        mapCoords = createMap0()
        for row in range(len(mapCoords)):
            for col in range(len(mapCoords[row])):
                r, g, b = mapCoords[row][col]
                defaultMapScreenCanvas.SetPixel(row, col, r, g, b)
        self.matrix.SwapOnVSync(defaultMapScreenCanvas)
        
        blankCanvas.Fill = (0, 0, 0)

        roundCount = 0
        while TurnState.run:
            print("turno ", roundCount)
            #inizio turno, aspetta per 600 secondi e poi esegue il codice di fine turno
            TurnState.e.wait(timeout=600)

            self.matrix.SwapOnVSync(blankCanvas)
            time.sleep(0.3)

            if roundCount == 0:             #probability of a disaster in round 0
                disaster = disasterProbability(0.1) 
            elif roundCount == 1:           #probability of a disaster in round 1
                disaster = disasterProbability(0.7)
            elif roundCount >= 2:           #probability of a disaster in round 2 or higher
                disaster = disasterProbability(0.85)

            if disaster:
                #genero un disastro, se l'ultimo salvato è none o diverso lo salvo, sennò controllo se è uguale all'ultimo e in caso lo cambio
                naturalDisaster = random.choices(["flood", "earthquake", "tornado"])[0]
                if TurnState.lastDisaster == None or TurnState.lastDisaster != naturalDisaster:
                    TurnState.lastDisaster = naturalDisaster
                elif TurnState.lastDisaster == naturalDisaster:
                    while(TurnState.lastDisaster == naturalDisaster):
                        naturalDisaster = random.choices(["flood", "earthquake", "tornado"])[0]
                    TurnState.lastDisaster = naturalDisaster
                
                if naturalDisaster == "flood":
                    floodCoords = flood()
                    for row in range(len(floodCoords)):
                        for col in range(len(floodCoords[row])):
                            r, g, b = floodCoords[row][col]
                            offScreenCanvas.SetPixel(row, col, r, g, b)
                    self.matrix.SwapOnVSync(offScreenCanvas)
                elif naturalDisaster == "tornado":
                    tornadoCoords = tornado(defineRotation())
                    for row in range(len(tornadoCoords)):
                        for col in range(len(tornadoCoords[row])):
                            r, g, b = tornadoCoords[row][col]
                            offScreenCanvas.SetPixel(row, col, r, g, b)
                    self.matrix.SwapOnVSync(offScreenCanvas)
                elif naturalDisaster == "earthquake":
                    eqCrds, eaLeftCrds, eaUpCrds, eaRightCrds = earthquake(defineRotation())
                    for row in range(len(eqCrds)):
                        for col in range(len(eqCrds[row])):
                            r, g, b = eqCrds[row][col]
                            offScreenCanvas.SetPixel(row, col, r, g, b)
                    self.matrix.SwapOnVSync(offScreenCanvas)
                    for _ in range(3):
                        for row in range(len(eaLeftCrds)):
                            for col in range(len(eaLeftCrds[row])):
                                r, g, b = eaLeftCrds[row][col]
                                offScreenCanvas.SetPixel(row, col, r, g, b)
                        time.sleep(0.3)
                        self.matrix.SwapOnVSync(offScreenCanvas)
                        for row in range(len(eaUpCrds)):
                            for col in range(len(eaUpCrds[row])):
                                r, g, b = eaUpCrds[row][col]
                                offScreenCanvas.SetPixel(row, col, r, g, b)
                        time.sleep(0.3)
                        self.matrix.SwapOnVSync(offScreenCanvas)
                        for row in range(len(eaRightCrds)):
                            for col in range(len(eaRightCrds[row])):
                                r, g, b = eaRightCrds[row][col]
                                offScreenCanvas.SetPixel(row, col, r, g, b)
                        time.sleep(0.3)
                        self.matrix.SwapOnVSync(offScreenCanvas)
                    for row in range(len(eqCrds)):
                        for col in range(len(eqCrds[row])):
                            r, g, b = eqCrds[row][col]
                            offScreenCanvas.SetPixel(row, col, r, g, b)
                    time.sleep(0.3)
                    self.matrix.SwapOnVSync(offScreenCanvas)
                time.sleep(5)
            self.matrix.SwapOnVSync(defaultMapScreenCanvas)
            TurnState.e.clear()
            roundCount += 1
        #when exiting the whole canvas turn black
        self.matrix.SwapOnVSync(blankCanvas)
        time.sleep(0.5)

def disasterProbability(prob):
    return np.random.binomial(n=1, p = prob)

def defineRotation():
    return random.choices(["up", "right", "down", "left"])[0]           
            
def createMap0():
    r, g, b = Colors.green
    map = []
    for x in range(32):
        row = []
        for y in range(32):
            row.append((r, g, b))
        map.append(row)
    #scacchiera
    r, g, b = Colors.darkGreen
    for y in range(32):
        if (y % 2) == 0:
            for x in range(1, 32, 2):
                map[x][y] = (r, g, b)
        else:
            for x in range(0, 32, 2):
                map[x][y] = (r, g, b)
    
    #left river
    for x, y in map0.leftRiver:
        r, g, b = Colors.darkBlue
        map[x*2][y*2] = (r, g, b)
        map[(x*2)+1][(y*2)+1] = (r, g, b)
        #r, g, b = Colors.blue
        map[(x*2)+1][(y*2)] = (r, g, b)
        map[(x*2)][(y*2)+1] = (r, g, b)
    #right river
    for x, y in map0.rightRiver:
        r, g, b = Colors.darkBlue
        map[x*2][y*2] = (r, g, b)
        map[(x*2)+1][(y*2)+1] = (r, g, b)
        #r, g, b = Colors.blue
        map[(x*2)+1][(y*2)] = (r, g, b)
        map[(x*2)][(y*2)+1] = (r, g, b)
    return(map)

def flood():
    riverLst = []
    floodLst = []
    for x, y in map0.leftRiver:
        riverLst.append((x, y))
        if y>0:
            floodLst.append((x, y-1)) #up
        if y<15:
            floodLst.append((x, y+1)) #down
        if x>0:
            floodLst.append((x-1, y)) #right
        if x<15:
            floodLst.append((x+1, y)) #left
    
    for x, y in map0.rightRiver:
        riverLst.append((x, y))
        if y>0:
            floodLst.append((x, y-1)) #up
        if y<15:
            floodLst.append((x, y+1)) #down
        if x>0:
            floodLst.append((x-1, y)) #right
        if x<15:
            floodLst.append((x+1, y)) #left

    map = createMap0()
    r, g, b = Colors.blue
    for x, y in floodLst:
        map[x*2][y*2] = (r, g, b)
        map[(x*2)+1][(y*2)+1] = (r, g, b)
        map[(x*2)+1][(y*2)] = (r, g, b)
        map[(x*2)][(y*2)+1] = (r, g, b)
    r, g, b = Colors.darkBlue
    for x, y in riverLst:
        map[x*2][y*2] = (r, g, b)
        map[(x*2)+1][(y*2)+1] = (r, g, b)
        map[(x*2)+1][(y*2)] = (r, g, b)
        map[(x*2)][(y*2)+1] = (r, g, b)
    return(map)

def tornado(rotation):
    coords = []
    if random.choices([0, 1])[0] == 0:
        coords = tornado0.coords
    else:
        coords = tornado1.coords
    
    rotatedCoords = []
    if rotation == "up":
        rotatedCoords = coords
    elif rotation == "right":
        for x, y in coords:
            rotatedCoords.append((15 - y, x))
    elif rotation == "down":
        for x, y in coords:
            rotatedCoords.append((15 - x, 15 -y))
    elif rotation == "left":
        for x, y in coords:
            rotatedCoords.append((y, 15 - x))
        
    map = createMap0()
    r, g, b = Colors.grey
    for x, y in rotatedCoords:
        map[x*2][y*2] = (r, g, b)
        map[(x*2)+1][(y*2)+1] = (r, g, b)
        map[(x*2)+1][(y*2)] = (r, g, b)
        map[(x*2)][(y*2)+1] = (r, g, b)
    return(map)

def earthquake(rotation):
    coordsLA =  earthquake0.leftArm
    coordsUA =  earthquake0.upperArm
    coordsRA =  earthquake0.rightArm

    rtdCoordsLeft = []
    rtdCoordsUp = []
    rtdCoordsRight = []
    if rotation == "up":
        rtdCoordsLeft = coordsLA
        rtdCoordsUp = coordsUA
        rtdCoordsRight = coordsRA
    elif rotation == "right":
        for x, y in coordsLA:
            rtdCoordsLeft.append((15 - y, x))
        for x, y in coordsUA:
            rtdCoordsUp.append((15 - y, x))
        for x, y in coordsRA:
            rtdCoordsRight.append((15 - y, x))
    elif rotation == "down":
        for x, y in coordsLA:
            rtdCoordsLeft.append((15 - x, 15 -y))
        for x, y in coordsUA:
            rtdCoordsUp.append((15 - x, 15 -y))
        for x, y in coordsRA:
            rtdCoordsRight.append((15 - x, 15 -y))
    elif rotation == "left":
        for x, y in coordsLA:
            rtdCoordsLeft.append((y, 15 - x))
        for x, y in coordsUA:
            rtdCoordsUp.append((y, 15 - x))
        for x, y in coordsRA:
            rtdCoordsRight.append((y, 15 - x))

    map = createMap0()
    #spawn earthquake
    r, g, b = Colors.orange
    for x, y in rtdCoordsLeft:
        map[x*2][y*2] = (r, g, b)
        map[(x*2)+1][(y*2)+1] = (r, g, b)
        map[(x*2)+1][(y*2)] = (r, g, b)
        map[(x*2)][(y*2)+1] = (r, g, b)
    for x, y in rtdCoordsUp:
        map[x*2][y*2] = (r, g, b)
        map[(x*2)+1][(y*2)+1] = (r, g, b)
        map[(x*2)+1][(y*2)] = (r, g, b)
        map[(x*2)][(y*2)+1] = (r, g, b)
    for x, y in rtdCoordsRight:
        map[x*2][y*2] = (r, g, b)
        map[(x*2)+1][(y*2)+1] = (r, g, b)
        map[(x*2)+1][(y*2)] = (r, g, b)
        map[(x*2)][(y*2)+1] = (r, g, b)
    
    mapLA = [ele[:] for ele in map]
    mapUA = [ele[:] for ele in map]
    mapRA = [ele[:] for ele in map]

    #used for animation
    r, g, b = Colors.white
    for x, y in rtdCoordsLeft:
        mapLA[x*2][y*2] = (r, g, b)
        mapLA[(x*2)+1][(y*2)+1] = (r, g, b)
        mapLA[(x*2)+1][(y*2)] = (r, g, b)
        mapLA[(x*2)][(y*2)+1] = (r, g, b)

    r, g, b = Colors.white
    for x, y in rtdCoordsUp:
        mapUA[x*2][y*2] = (r, g, b)
        mapUA[(x*2)+1][(y*2)+1] = (r, g, b)
        mapUA[(x*2)+1][(y*2)] = (r, g, b)
        mapUA[(x*2)][(y*2)+1] = (r, g, b)

    r, g, b = Colors.white
    for x, y in rtdCoordsRight:
        mapRA[x*2][y*2] = (r, g, b)
        mapRA[(x*2)+1][(y*2)+1] = (r, g, b)
        mapRA[(x*2)+1][(y*2)] = (r, g, b)
        mapRA[(x*2)][(y*2)+1] = (r, g, b)
    
    return(map, mapLA, mapUA, mapRA)
    


def on_mouse_click(mouse_position_x, mouse_position_y, button, is_pressed):
    if button == mouse.Button.right and is_pressed:
        TurnState.e.set()
    if button == mouse.Button.middle and is_pressed:
        TurnState.run = False
        TurnState.e.set()

mouse_listener = mouse.Listener(on_click=on_mouse_click)

# Main function
if __name__ == "__main__":
    mouse_listener.start()
    game = Game()
    if (not game.process()):
        game.print_help()