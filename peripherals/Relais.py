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
        ison = self.isOn(channel)
        self.pi.write(self.channelPins[channel - 1], not ison)

    def isOn(self, channel:int) -> bool:
        return bool(self.pi.read(self.channelPins[channel - 1]))

if __name__ == "__main__":
    pi = pigpio.pi()
    relaisPins = [23, 24]
    relais = Relais(pi, relaisPins)
    
    relais.toggle(2)
    time.sleep(5)