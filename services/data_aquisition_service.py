import time
import pigpio
import mh_z19
from datetime import datetime

from models.measurement import Measurement, MeasurementType

from peripherals.Camera import Camera
from peripherals.DHT22 import DHT22
from peripherals.HC_SR04 import HC_SR04

class DataAquisition:
    
    measurements:Measurement = []
    imagePath = ""
    rememberedMinute = -1
    
    def __init__(self):
        self.pigPio = pigpio.pi()
        self.cam = Camera("/home/alex/pics")
        self.dht22 = DHT22(self.pigPio, 4)
        self.mhz19 = mh_z19
        self.hc_sr04: HC_SR04 = HC_SR04(self.pigPio, 23, 24)
    
    def run(self):
        # Every minute, take a picture
        if self.rememberedMinute != time.localtime().tm_min:
            self.imagePath = self.cam.takePicture()
            self.measurements.append(Measurement(datetime.now(), MeasurementType.Picture, self.imagePath, "path"))
        
        # Temperature and Humidity 
        self.dht22.trigger()
        temp = self.dht22.temperature()
        humidity = self.dht22.humidity()
        
        self.measurements.append(Measurement(datetime.now(), MeasurementType.TEMPERATURE, temp, "°C"))
        self.measurements.append(Measurement(datetime.now(), MeasurementType.HUMIDITY, humidity, "%"))
        
        # CO2
        try:
            co2 = self.mhz19.read()["co2"]
        except:
            co2 = -1
        self.measurements.append(Measurement(datetime.now(), MeasurementType.CO2, co2, "ppm"))
        
        datetime.datetime.now()
        # Water Level
        level = self.hc_sr04.calculatePercentFilled()
        self.measurements.append(Measurement(datetime.now(), MeasurementType.WaterLevel, level, "%"))
        
    def __str__(self):
        returnStr = "Measurements:\n"
        for measurement in self.measurements:
            returnStr += f"{measurement.measurement_type}({measurement.value} {measurement.unit})\n"