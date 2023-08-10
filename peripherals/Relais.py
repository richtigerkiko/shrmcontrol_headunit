import time
import pigpio

class Relais:
    def __init__(self, pi:pigpio.pi, channelPins:list[int]):
        self.pi = pi
        self.channelPins = channelPins
        for pin in self.channelPins:
            self.pi.set_mode(pin, pigpio.OUTPUT)
        
    def on(self, channel:int):
        self.pi.write(self.channelPins[channel - 1], 1)

    def off(self, channel:int):
        self.pi.write(self.channelPins[channel - 1], 0)
        
    def toggle(self, channel:int):
        currentState = bool(self.pi.read(self.channelPins[channel - 1]))
        self.pi.write(self.channelPins[channel - 1], not currentState)


if __name__ == "__main__":
    pi = pigpio.pi()
    relais = Relais(pi, [23, 24])
    relais.on(1)
    time.sleep(2)
    relais.on(2)
    time.sleep(2)
    relais.off(1)
    time.sleep(2)
    relais.off(2)
    time.sleep(1)
    relais.on(2)
    time.sleep(1)
    relais.toggle(2)
    time.sleep(1)
    relais.toggle(2)
    time.sleep(1)
    relais.toggle(2)
    time.sleep(1)
    relais.toggle(2)