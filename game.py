from samplebase import SampleBase
from pynput import mouse
from utils import map0, earthquake0, tornado0, tornado1
import time
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
        offset_canvas = self.matrix.CreateFrameCanvas()
        offset_canvas = createMap0(self, offset_canvas)

        while TurnState.run:
            #inizio turno, aspetta per 600 secondi e poi esegue il codice di fine turno
            TurnState.e.wait(timeout=600)
            
            
def createMap0(self, offset_canvas):
    r, g, b = Colors.green
    offset_canvas.Fill(r, g, b)
    
    r, g, b = Colors.darkGreen
    for y in range(32):
        if (y % 2) == 0:
            for x in range(1, 32, 2):
                offset_canvas.SetPixel(x, y, r, g, b)
        else:
            for x in range(0, 32, 2):
                offset_canvas.SetPixel(x, y, r, g, b)
    
    #left river
    for x, y in map0.leftRiver:
        r, g, b = Colors.blue
        offset_canvas.SetPixel(x*2, y*2, r, g, b)
        offset_canvas.SetPixel((x*2)+1, (y*2)+1, r, g, b)
        r, g, b = Colors.darkBlue
        offset_canvas.SetPixel((x*2)+1, (y*2), r, g, b)
        offset_canvas.SetPixel((x*2), (y*2)+1, r, g, b)

    #right river
    for x, y in map0.rightRiver:
        r, g, b = Colors.blue
        offset_canvas.SetPixel(x*2, y*2, r, g, b)
        offset_canvas.SetPixel((x*2)+1, (y*2)+1, r, g, b)
        r, g, b = Colors.darkBlue
        offset_canvas.SetPixel((x*2)+1, (y*2), r, g, b)
        offset_canvas.SetPixel((x*2), (y*2)+1, r, g, b)
    
    offset_canvas = self.matrix.SwapOnVSync(offset_canvas)
    return(offset_canvas)


def on_mouse_click(mouse_position_x, mouse_position_y, button, is_pressed):
    if button == mouse.Button.right and is_pressed:
        #TurnState.e.set()
        pass
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