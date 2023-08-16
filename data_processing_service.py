import asyncio
import uuid
from actions_service import ActionService
from models.alarm import Alarm, AlarmType
from models.measurement import Measurement, MeasurementType
import logging
import pigpio

from models.ruleset import Rule, RuleSet

class DataProcesing:
    def __init__(self, pi):
        self.measurements = []
        self.actionsService = ActionService(25, pi)
        self.alarms: list[Alarm] = []
        
        
    def process(self, measurements:list[Measurement], ruleset:RuleSet = None):
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
        
        ruleset = next((rule for rule in self.ruleset.rules if rule.name == "HUMIDITY"), None)
        if(ruleset == None): self.alarms.append(Alarm(AlarmType.Critical, "No humidity rules found, this should never happen"))
        
        elif(ruleset.force_on):
            logging.info("Forcing humidifier on")
            asyncio.run(self.actionsService.start_humidifier())
            self.alarms.append(Alarm(AlarmType.Info, "Forcing humidifier on"))
        
        elif(ruleset.force_off):
            logging.info("Forcing humidifier off")
            asyncio.run(self.actionsService.stop_humidifier())
            self.alarms.append(Alarm(AlarmType.Info, "Forcing humidifier off"))
            
        elif(ruleset.lower_critical != -1 and ruleset.lower_critical > currentHumidity.value):
            logging.critical("Humidity is critically low, starting humidifier and sending alarms")
            asyncio.run(self.actionsService.start_humidifier())
            self.alarms.append(Alarm(AlarmType.Critical, "Humidity is too low, starting humidifier"))
        
        elif(ruleset.lower_threshold != -1 and ruleset.lower_threshold > currentHumidity.value):
            logging.info("Humidity is too low, starting humidifier")
            asyncio.run(self.actionsService.start_humidifier())
            self.alarms.append(Alarm(AlarmType.Info, "Humidity is too low, starting humidifier"))
        
        elif(ruleset.upper_critical != -1 and ruleset.upper_critical < currentHumidity.value):
            logging.critical("Humidity is critically high, stopping humidifier and sending alarms")
            asyncio.run(self.actionsService.stop_humidifier())
            self.alarms.append(Alarm(AlarmType.Critical, "Humidity is too high, stopping humidifier"))
            
        elif(ruleset.upper_threshold != -1 and ruleset.upper_threshold < currentHumidity.value):
            logging.info("Humidity is getting too high, stopping humidifier")
            asyncio.run(self.actionsService.stop_humidifier())
            self.alarms.append(Alarm(AlarmType.Info, "Humidity is getting too high, stopping humidifier"))

    def process_co2(self):
        currentCo2 = next((measurement for measurement in self.measurements if measurement.measurementType == MeasurementType.CO2), None)
        if currentCo2 == None: 
            self.alarms.append(Alarm(AlarmType.Critical, "No co2 measurement found, sensor not connected?"))
            return
        
        ruleset = next((rule for rule in self.ruleset.rules if rule.name == "CO2"), None)
        if(ruleset == None): self.alarms.append(Alarm(AlarmType.Critical, "No CO2 rules found, this should never happen"))
        
        elif(ruleset.lower_critical != -1 and ruleset.lower_critical > currentCo2.value):
            logging.critical("Co2 is critically low, this will never happen but just in case")
            self.alarms.append(Alarm(AlarmType.Critical, "Co2 is too low, it cant be to low lol"))
        
        elif ruleset.lower_threshold != -1 and ruleset.lower_threshold > currentCo2.value:
            logging.info("Co2 is perfect, turning of Tentfan")
            self.actionsService.stop_tentFan()
            self.alarms.append(Alarm(AlarmType.Info, "Co2 is perfect, turning of Tentfan"))
        
        elif ruleset.upper_critical != -1 and ruleset.upper_threshold < currentCo2.value:
            logging.critical("Co2 is critically high, starting Tentfan and sending alarms")
            self.actionsService.start_tentFan()
            self.alarms.append(Alarm(AlarmType.Critical, "Co2 is too high, starting Tentfan, if its not going down check the tent and the sensor"))
        
        elif ruleset.upper_threshold != -1 and ruleset.upper_threshold < currentCo2.value:
            logging.info("Co2 is getting too high, starting Tentfan")
            self.actionsService.start_tentFan()
            self.alarms.append(Alarm(AlarmType.Info, "Co2 is getting too high, starting Tentfan"))
        pass
    
    def process_waterlevel(self):
        pass
    
    def process_temperature(self):
        pass
