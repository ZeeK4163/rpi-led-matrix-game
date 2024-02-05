#!/usr/bin/env python
from samplebase import SampleBase
from pynput import mouse
from utils import map0, earthquake0, tornado0, tornado1
import time
import threading
import random

class TurnState():
    e = threading.Event()
    run = True
    lastDisaster = None

class Colors():
    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (23, 173, 63)
    blue = (0, 128, 201)
    orange = (201, 121, 0)
    grey = (156, 156, 156)

class SimpleSquare(SampleBase):
    def __init__(self, *args, **kwargs):
        super(SimpleSquare, self).__init__(*args, **kwargs)

    def run(self):
        #creo la mappa
        offset_canvas = self.matrix.CreateFrameCanvas()
        offset_canvas = createMap0(self, offset_canvas)

        roundCount = 0

        while TurnState.run:
            #inizio turno, aspetta per 600 secondi e poi esegue il codice di fine turno
            TurnState.e.wait(timeout=600)

            #flash white means new turn started
            r, g, b = Colors.white
            offset_canvas.Fill(r, g, b)
            offset_canvas = self.matrix.SwapOnVSync(offset_canvas)
            time.sleep(0.1)

            offset_canvas = createMap0(self, offset_canvas)
            
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
                    offset_canvas = flood(self, offset_canvas)
                elif naturalDisaster == "earthquake":
                    offset_canvas = earthquake(self, offset_canvas, defineRotation())
                elif naturalDisaster == "tornado":
                    offset_canvas = tornado(self, offset_canvas, defineRotation())

            #reset thread per reimpostare il turno
            TurnState.e.clear()
            roundCount += 1

#create a map, filling the matrix with green and draw 2 rivers with given coords
def createMap0(self, offset_canvas):
    r, g, b = Colors.green
    offset_canvas.Fill(r, g, b)

    r, g, b = Colors.blue
    #left river
    for x, y in map0.leftRiver:
        offset_canvas.SetPixel(x, y, r, g, b)

    #right river
    for x, y in map0.rightRiver:
        offset_canvas.SetPixel(x, y, r, g, b)
    
    offset_canvas = self.matrix.SwapOnVSync(offset_canvas)
    return(offset_canvas)

def disasterProbability(prob):
    return random.binomialvariate(n=1, p = prob)

def defineRotation():
    return random.choices(["up", "right", "down", "left"])[0]

#flood of the two rivers
def flood(self, offset_canvas):
    r, g, b = Colors.blue
    for x, y in map0.leftRiver:
        if y>0:
            offset_canvas.SetPixel(x, y-1, r, g, b) #up
        if y<15:
            offset_canvas.SetPixel(x, y+1, r, g, b) #down
        if x>0:
            offset_canvas.SetPixel(x-1, y, r, g, b) #right
        if x<15:
            offset_canvas.SetPixel(x+1, y, r, g, b) #left
    
    for x, y in map0.rightRiver:
        if y>0:
            offset_canvas.SetPixel(x, y-1, r, g, b) #up
        if y<15:
            offset_canvas.SetPixel(x, y+1, r, g, b) #down
        if x>0:
            offset_canvas.SetPixel(x-1, y, r, g, b) #right
        if x<15:
            offset_canvas.SetPixel(x+1, y, r, g, b) #left
        
    offset_canvas = self.matrix.SwapOnVSync(offset_canvas)
    return(offset_canvas)

#create a tornado with given coords
def tornado(self, offset_canvas, rotation):
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
    
    r, g, b = Colors.grey
    for x, y in rotatedCoords:
        offset_canvas.SetPixel(x, y, r, g, b)
    offset_canvas = self.matrix.SwapOnVSync(offset_canvas)
    return(offset_canvas)

def earthquake(self, offset_canvas, rotation):
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

    #spawn earthquake
    r, g, b = Colors.orange

    for x, y in rtdCoordsLeft:
        offset_canvas.SetPixel(x, y, r, g, b)
    for x, y in rtdCoordsUp:
        offset_canvas.SetPixel(x, y, r, g, b)
    for x, y in rtdCoordsRight:
        offset_canvas.SetPixel(x, y, r, g, b)
    offset_canvas = self.matrix.SwapOnVSync(offset_canvas)
    time.sleep(0.2)

    #animation earthquake
    for _ in range(3):
        r, g, b = Colors.white
        for x, y in rtdCoordsLeft:
            offset_canvas.SetPixel(x, y, r, g, b)
        offset_canvas = self.matrix.SwapOnVSync(offset_canvas)
        time.sleep(0.3)
        r, g, b = Colors.orange
        for x, y in rtdCoordsLeft:
            offset_canvas.SetPixel(x, y, r, g, b)
        offset_canvas = self.matrix.SwapOnVSync(offset_canvas)

        r, g, b = Colors.white
        for x, y in rtdCoordsUp:
            offset_canvas.SetPixel(x, y, r, g, b)
        offset_canvas = self.matrix.SwapOnVSync(offset_canvas)
        time.sleep(0.3)
        r, g, b = Colors.orange
        for x, y in rtdCoordsUp:
            offset_canvas.SetPixel(x, y, r, g, b)
        offset_canvas = self.matrix.SwapOnVSync(offset_canvas)

        r, g, b = Colors.white
        for x, y in rtdCoordsRight:
            offset_canvas.SetPixel(x, y, r, g, b)
        offset_canvas = self.matrix.SwapOnVSync(offset_canvas)
        time.sleep(0.3)
        r, g, b = Colors.orange
        for x, y in rtdCoordsRight:
            offset_canvas.SetPixel(x, y, r, g, b)
        offset_canvas = self.matrix.SwapOnVSync(offset_canvas)

    return(offset_canvas)

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
    simple_square = SimpleSquare()
    if (not simple_square.process()):
        simple_square.print_help()
    