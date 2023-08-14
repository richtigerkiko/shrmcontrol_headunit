import asyncio
from actions_service import ActionService
from models.measurement import Measurement, MeasurementType
import logging
import pigpio

class DataProcesing:
    # sampleruleset
    ruleset = {
        "humidity": {
            "lowerthreshold": 88,
            "upperthreshold": 95,
            "lowercritical": 80,
            "uppercritical": -1,
            "unit": "%"
        },
        "co2": {
            "lowerthreshold": 450,
            "upperthreshold": 600,
            "lowercritical": -1,
            "uppercritical": 800,
            "unit": "ppm"
        },
        "waterlevel": {
            "lowerthreshold": 10,
            "upperthreshold": -1,
            "lowercritical": 5,
            "uppercritical": -1,
            "unit": "%"
        }
    }
    def __init__(self, measurements:list[Measurement], ruleset:dict):
        self.measurements = measurements
        self.actionsService = ActionService(25, pigpio.pi())
        self.alarms = []
        
    def process(self):
        # do something with self.data
        return self.data
    
    def process_humidity(self):
        currentHumidity = next((measurement for measurement in self.measurements if measurement.measurementType == MeasurementType.HUMIDITY), None)
        if currentHumidity == None: 
            self.alarms.append("No humidity measurement found")
            return
        ruleset = self.ruleset["humidity"]
        
        if ruleset["lowerthreshold"] > currentHumidity.value:
            logging.info("Humidity is too low, starting humidifier")
            asyncio.run(self.actionsService.start_humidifier())
            self.alarms.append("Humidity is too low")
        pass
    
    def process_co2(self):
        pass
    
    def process_waterlevel(self):
        pass
    
    def process_temperature(self):
        pass
