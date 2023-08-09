import pigpio

class Relais:
    def __init__(self, pi, channel1:int = 23, channel2:int = 24):
        self.channel1 = channel1
        self.channel2 = channel2
        self.pi = pi
        self.pi.set_mode(self.channel1, pigpio.OUTPUT)
        self.pi.set_mode(self.channel2, pigpio.OUTPUT)
        
    def on(self, channel:int):
        if channel == 1:
            self.pi
