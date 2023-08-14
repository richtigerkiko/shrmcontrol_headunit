import asyncio
import logging
import time
import pigpio
from peripherals.RFSender import RFSender
from peripherals.Relais import Relais

class ActionService:
    
    fogger_power_on_code = 4457809
    fogger_power_off_code = 4457812
    
    tentfan_power_on_code = 4460881
    tentfan_power_off_code = 4460884
    
    isHumidifierOn = False
    isHumidifierStarting = False
    isHumidifierStopping = False
    
    isTentFanOn = False
    isTentFanStarting = False
    isTentFanStopping = False
    
    humidifierFanRelaisChannel = 1
    ledLightRelaisChannel = 2
    
    def __init__(self, rfSenderpio:int, pigpio):
        logging.info("Initialising Action Service")

        self.rfSender = RFSender(rfSenderpio, pulseLength=305, protocol=1)
        self.relais = Relais(pigpio, [23, 24])
        # On init, turn everything off
        pass
    
    async def start_humidifier(self):
        logging.info("Starting humidifier")
        if self.isHumidifierStopping:
            logging.warning("Humidifier is currently still stopping, not starting")
            return
        self.isHumidifierStarting = True
        logging.debug("Starting humidfier fan")
        self.relais.on(self.humidifierFanRelaisChannel)
        
        # wait a minute for good airflow
        await asyncio.sleep(60)
        
        logging.debug("Sending code to turn on fogger: " + self.fogger_power_on_code)
        self.rfSender.sendCode(self.fogger_power_on_code)

        self.isHumidifierOn = True
        self.isHumidifierStopping = False
        pass
    
    async def stop_humidifier(self):
        logging.info("Stopping humidifier")
        if self.isHumidifierStarting:
            logging.warning("Humidifier is currently still starting, not stopping")
            return
        self.isHumidifierStopping = True
        
        logging.debug("Sending code to turn of fogger: " + self.fogger_power_on_code)
        self.rfSender.sendCode(self.fogger_power_on_code)
        
        # wait a minute to exit humidity before turning of humidifer fan
        await asyncio.sleep(60)
        logging.debug("Stopping humidfier fan")
        self.relais.off(self.humidifierFanRelaisChannel)
        
        self.isHumidifierStopping = False
        self.isHumidifierOn = False
        pass
    
    def start_tentFan(self):
        pass
    
    def stop_tentFan(self):
        pass
    
    def start_tentLight(self):
        pass
    
    def stop_tentLight(self):
        pass
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    actionService = ActionService(25, pigpio.pi())
    print(actionService.__dict__)
    asyncio.run(actionService.start_humidifier())
    print(actionService.__dict__)
    time.sleep(5)
    asyncio.run(actionService.stop_humidifier())
    print(actionService.__dict__)