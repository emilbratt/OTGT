class ScanItem:
    def __init__(self, led):
        if led == False:
            return
        led.off()
        led.value = 0.5
        led.blink(0.2,0.5)
