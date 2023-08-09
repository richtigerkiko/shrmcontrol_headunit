from statistics import mean
import pigpio
import time
import math


class HC_SR04:
    def __init__(self, pi, triggerPin:int = 17, echoPin:int = 27):
        self.triggerPin = triggerPin
        self.echoPin = echoPin
        self.pi = pi
        self.pi.set_mode(self.triggerPin, pigpio.OUTPUT)
        self.pi.set_mode(self.echoPin, pigpio.INPUT)
        
    def measure(self):
        self.pi.write(self.triggerPin, 1)
        time.sleep(0.001)
        self.pi.write(self.triggerPin, 0)
        
    
        tStart = time.time()
        tStop = time.time()
    
        while self.pi.read(self.echoPin) == 0:
            tStart = time.time()
            if(tStart-tStop > 3): break
            
        while self.pi.read(self.echoPin) == 1:
            tStop = time.time()
            if(tStop - tStart > 1): break
            
        tElapsed = tStop - tStart
        distance = (tElapsed * 34300) / 2 # distance (cm) = time (s) * speed of sound (cm/s) / 2
        
        return math.floor(distance)

    def __del__(self):
        self.pi.stop()
        
    def tripplemeasureaverage(self):
        measures = []
        for i in range(3):
            measures.append(self.measure())
            time.sleep(0.1)
        average = mean(measures)
        return math.floor(average)
    
    def calculatePercentFilled(self, containerHeight: int) -> float:
        distanceToWaterSurface = self.tripplemeasureaverage()
        filledHeight = containerHeight - distanceToWaterSurface
        percent = (filledHeight / containerHeight) * 100
        return round(percent, 2)
        
if __name__ == '__main__':
    try:
        sensor = HC_SR04(pi=pigpio.pi())
        while True:
            print(sensor.tripplemeasureaverage())
            print(sensor.calculatePercentFilled(40))
            time.sleep(1)
    except KeyboardInterrupt:
        sensor.__del__()

