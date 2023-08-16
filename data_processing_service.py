import asyncio
from actions_service import ActionService
from models.alarm import Alarm, AlarmType
from models.measurement import Measurement, MeasurementType
import logging
import pigpio

class DataProcesing:
    # sampleruleset
    ruleset = {
        "humidity": {
            "lowerthreshold": 90,
            "upperthreshold": 95,
            "lowercritical": 80.0,
            "uppercritical": -1,
            "unit": "%"
        },
        "co2": {
            "lowerthreshold": 450,
            "upperthreshold": 550,
            "lowercritical": -1,
            "uppercritical": 800,
            "unit": "ppm"
        },
        "waterlevel": {
            "lowerthreshold": 15,
            "upperthreshold": -1,
            "lowercritical": 10,
            "uppercritical": -1,
            "unit": "%"
        }
    }
    def __init__(self, pi):
        self.measurements = []
        self.actionsService = ActionService(25, pi)
        self.alarms: list[Alarm] = []
        
        
    def process(self, measurements:list[Measurement], ruleset:dict = None):
        # run all process steps:
        logging.info("Starting data processing")
        self.measurements = measurements
        self.actionsService.start_tentLight()
        if ruleset != None:
            self.ruleset = ruleset
        self.process_humidity()
        # self.process_co2()
        self.process_waterlevel()
    
    def process_humidity(self):
        currentHumidity = next((measurement for measurement in self.measurements if measurement.measurementType == MeasurementType.HUMIDITY), None)
        if currentHumidity == None: 
            self.alarms.append(Alarm(AlarmType.Critical, "No humidity measurement found, sensor not connected?"))
            return
        ruleset = self.ruleset["humidity"]
        
        if (ruleset["lowercritical"] != -1 and ruleset["lowercritical"] > currentHumidity.value):
            logging.critical("Humidity is critically low, starting humidifier and sending alarms")
            asyncio.run(self.actionsService.start_humidifier())
            self.alarms.append(Alarm(AlarmType.Critical, "Humidity is too low, starting humidifier"))
            
        elif (ruleset["lowerthreshold"] != -1 and ruleset["lowerthreshold"] > currentHumidity.value):
            logging.info("Humidity is too low, starting humidifier")
            asyncio.run(self.actionsService.start_humidifier())
            self.alarms.append(Alarm(AlarmType.Info, "Humidity is too low, starting humidifier"))
            
        elif ruleset["uppercritical"] != -1 and ruleset["uppercritical"] < currentHumidity.value:
            logging.critical("Humidity is critically high, stopping humidifier and sending alarms")
            asyncio.run(self.actionsService.stop_humidifier())
            self.alarms.append(Alarm(AlarmType.Critical, "Humidity is too high, stopping humidifier"))
            
        elif ruleset["upperthreshold"] != -1 and ruleset["upperthreshold"] < currentHumidity.value:
            logging.info("Humidity is getting too high, stopping humidifier")
            asyncio.run(self.actionsService.stop_humidifier())
            self.alarms.append(Alarm(AlarmType.Info, "Humidity is getting too high, stopping humidifier"))

    def process_co2(self):
        currentCo2 = next((measurement for measurement in self.measurements if measurement.measurementType == MeasurementType.CO2), None)
        if currentCo2 == None: 
            self.alarms.append(Alarm(AlarmType.Critical, "No co2 measurement found, sensor not connected?"))
            return
        ruleset = self.ruleset["co2"]
        
        if ruleset["lowercritical"] != -1 and ruleset["lowercritical"] > currentCo2.value:
            logging.critical("Co2 is critically low, this will never happen but just in case")
            self.alarms.append(Alarm(AlarmType.Critical, "Co2 is too low, it cant be to low lol"))
        
        elif ruleset["lowerthreshold"] != -1 and ruleset["lowerthreshold"] > currentCo2.value:
            logging.info("Co2 is perfect, turning of Tentfan")
            self.actionsService.stop_tentFan()
            self.alarms.append(Alarm(AlarmType.Info, "Co2 is perfect, turning of Tentfan"))
        
        elif ruleset["uppercritical"] != -1 and ruleset["uppercritical"] < currentCo2.value:
            logging.critical("Co2 is critically high, starting Tentfan and sending alarms")
            self.actionsService.start_tentFan()
            self.alarms.append(Alarm(AlarmType.Critical, "Co2 is too high, starting Tentfan, if its not going down check the tent and the sensor"))
        
        elif ruleset["upperthreshold"] != -1 and ruleset["upperthreshold"] < currentCo2.value:
            logging.info("Co2 is getting too high, starting Tentfan")
            self.actionsService.start_tentFan()
            self.alarms.append(Alarm(AlarmType.Info, "Co2 is getting too high, starting Tentfan"))
        pass
    
    def process_waterlevel(self):
        pass
    
    def process_temperature(self):
        pass
