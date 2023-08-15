import asyncio
import logging
import time
import pigpio
from peripherals.RFSender import RFSender
from peripherals.Relais import Relais

class ActionService:
    
    fogger_power_on_code = 4460881
    fogger_power_off_code = 4460884
    
    tentfan_power_on_code = 4457809
    tentfan_power_off_code = 4457812
    
    isHumidifierOn = False
    isHumidifierStarting = False
    isHumidifierStopping = False
    
    isTentFanOn = False
    
    isTentLightOn = False
    
    humidifierFanRelaisChannel = 1
    ledLightRelaisChannel = 2
    
    def __init__(self, rfSenderpio:int, pi):
        logging.info("Initialising Action Service")

        self.rfSender = RFSender(rfSenderpio, pulseLength=305, protocol=1)
        self.relais = Relais(pi, [23, 24])
        # On init, turn everything off
        self.stop_humidifier()
        self.stop_tentFan()
        self.stop_tentLight()
        pass
    
    async def start_humidifier(self):
        logging.info("Starting humidifier")
        if self.isHumidifierOn:
            logging.info("humidifier should already be running, resending plug code just in case")
            self.rfSender.sendCode(self.fogger_power_on_code)
        if self.isHumidifierStopping:
            logging.warning("Humidifier is currently still stopping, not starting")
            return
        else:
            self.isHumidifierStarting = True
            logging.debug("Starting humidfier fan")
            self.relais.on(self.humidifierFanRelaisChannel)
        
            # wait a minute for good airflow
            await asyncio.sleep(10)
            
            logging.debug(f"Sending code to turn on fogger: {self.fogger_power_on_code}")
            self.rfSender.sendCode(self.fogger_power_on_code)

            self.isHumidifierOn = True
            self.isHumidifierStarting = False
    
    async def stop_humidifier(self):
        logging.info("Stopping humidifier")
        if self.isHumidifierStarting:
            logging.warning("Humidifier is currently still starting, not stopping")
            return
        if self.isHumidifierOn == False:
            logging.info("Humidifier should already be off, resending plug code just in case")
            self.rfSender.sendCode(self.fogger_power_off_code)
        else:
            self.isHumidifierStopping = True
            
            logging.debug(f"Sending code to turn of fogger: {self.fogger_power_on_code}" )
            self.rfSender.sendCode(self.fogger_power_off_code)
            
            # wait a minute to exit humidity before turning of humidifer fan
            await asyncio.sleep(10)
            logging.debug("Stopping humidfier fan")
            self.relais.off(self.humidifierFanRelaisChannel)
            
            self.isHumidifierStopping = False
            self.isHumidifierOn = False
    
    def start_tentFan(self):
        logging.info("Starting Tentfan")
        self.rfSender.sendCode(self.tentfan_power_on_code)
        self.isTentFanOn = True
        pass
    
    def stop_tentFan(self):
        logging.info("Stopping Tentfan")
        self.rfSender.sendCode(self.tentfan_power_off_code)
        self.isTentFanOn = False
        pass
    
    def start_tentLight(self):
        logging.info("Starting Tentlight")
        self.relais.on(self.ledLightRelaisChannel)
        self.isTentLightOn = True
        pass
    
    def stop_tentLight(self):
        logging.info("Stopping Tentlight")
        self.relais.off(self.ledLightRelaisChannel)
        self.isTentLightOn = False
        pass
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Testrun")
    actionService = ActionService(25, pigpio.pi())
    actionService.start_tentLight()
    asyncio.run(actionService.start_humidifier())
    time.sleep(10)
    asyncio.run(actionService.stop_humidifier())
    time.sleep(3)
    actionService.start_tentFan()
    time.sleep(3)
    actionService.stop_tentFan()
    time.sleep(3)
    actionService.stop_tentLight()
    