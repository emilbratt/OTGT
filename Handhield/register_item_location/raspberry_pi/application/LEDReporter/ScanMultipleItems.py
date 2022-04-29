class ScanMultipleItems:
    def __init__(self, led):
        print('setting LED LEDReporter.ScanMultipleItems()')
        if led == False:
            return
        led.off()
        led.value = 0.5
        led.on()
