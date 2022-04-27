class ScanShelf:
    def __init__(self, led):
        if led == False:
            return
        led.off()
        led.value = 0.5
        led.blink(0.05,0.2)
