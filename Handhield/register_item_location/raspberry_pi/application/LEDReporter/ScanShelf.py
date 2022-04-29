class ScanShelf:
    def __init__(self, led):
        print('setting LED LEDReporter.ScanShelf()')
        if led == False:
            return
        led.off()
        led.value = 0.5
        led.blink(0.05,0.2)
