class ScanItem:
    def __init__(self, pin = 17):
        self.pin = pin
        try:
            from gpiozero import LED,PWMLED
            self.led = LED(self.pin)
            self.led.off()
            self.led.value = 0.5  # half brightness
            self.led.blink(0.2,0.5)
        except ModuleNotFoundError:
            print('gpiozero not found, skipping LED')
