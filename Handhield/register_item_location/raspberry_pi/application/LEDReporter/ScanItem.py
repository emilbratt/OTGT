class ScanItem:
    def __init__(self, led):
        if led == False:
            return
        led.blink(0.2,0.5)
