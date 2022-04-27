class StartLED:
    def __init__(self, pin = 17):
        self.led = None
        try:
            from gpiozero import LED,PWMLED
            self.led = LED(pin)

        except ModuleNotFoundError:
            print('gpiozero not found, disabling LED')
            
