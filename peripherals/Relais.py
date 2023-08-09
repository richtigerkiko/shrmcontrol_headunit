import time
import pigpio

class Relais:
    def __init__(self, pi:pigpio.pi, channel1:int = 23, channel2:int = 24):
        self.channel1 = channel1
        self.channel2 = channel2
        self.pi = pi
        self.pi.set_mode(self.channel1, pigpio.OUTPUT)
        self.pi.set_mode(self.channel2, pigpio.OUTPUT)
        
    def on(self, channel:int):
        if channel == 1:
            self.pi.write(self.channel1, 1)
        elif channel == 2:
            self.pi.write(self.channel2, 1)

    def off(self, channel:int):
        if channel == 1:
            self.pi.write(self.channel1, 0)
        elif channel == 2:
            self.pi.write(self.channel2, 0)


if __name__ == "__main__":
    pi = pigpio.pi()
    relais = Relais(pi)
    relais.on(1)
    time.sleep(2)
    relais.on(2)
    time.sleep(2)
    relais.off(1)
    time.sleep(2)
    relais.off(2)
    time.sleep(1)
    relais.on(2)