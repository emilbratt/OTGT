class ScanItem:
    def __init__(self, led):
        print('setting LED LEDReporter.ScanItem()')
        if led == False:
            return
        led.blink(0.2,0.5)
