class ScanShelf:
    def __init__(self, led):
        if led == False:
            return
        led.blink(0.05,0.2)
