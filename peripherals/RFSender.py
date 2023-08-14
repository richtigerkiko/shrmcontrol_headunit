import logging

from rpi_rf import RFDevice


class RFSender:
    def __init__(self,  gpio:int, repeats:int = 10, pulseLength:int = None, protocol:int = None, txLength:int = None):
        self.rfDevice = RFDevice(gpio)
        self.pulseLength = pulseLength
        self.protocol = protocol
        self.repeats = repeats
        self.txLength = txLength
        self.rfDevice.enable_tx()
        self.rfDevice.tx_repeat = self.repeats
        logging.info("Initialised RF Sender on gpio: " + str(gpio))
        
    def sendCode(self, code:int):
        logging.info("Sending code to RFDevice: " + str(code))
        self.rfDevice.tx_code(code, tx_proto=self.protocol, tx_pulselength=self.pulseLength, tx_length=self.txLength)
    
    def __del__(self) -> None:
        self.rfDevice.cleanup()
        pass

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    rfSender = RFSender(25, pulseLength=305, protocol=1)
    rfSender.sendCode(4460884)