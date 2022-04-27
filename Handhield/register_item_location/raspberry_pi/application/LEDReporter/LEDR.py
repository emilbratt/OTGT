class LEDR:
    '''
        use a connected LED to display feedback
    '''
    def __init__(self):
        self.led = None
        try:
            from gpiozero import LED,PWMLED
            self.available = True
            self.led = LED(17)
        except ModuleNotFoundError:
            self.available = False
            print('gpiozero not found, disabling LED')
