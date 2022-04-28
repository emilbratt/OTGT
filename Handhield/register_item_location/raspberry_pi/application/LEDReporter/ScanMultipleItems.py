class ScanMultipleItems:
    def __init__(self, led):
        print('setting LED LEDReporter.ScanMultipleItems()')
        if led == False:
            return
        led.on()
