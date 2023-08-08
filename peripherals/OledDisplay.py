import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont, ImageDraw, Image


class OledDisplay:
    font = ImageFont.truetype('DejaVuSans.ttf', 12)
    
    def __init__(self, i2cAddr: int = 0x3C, port: int = 1) -> None:
        serial = i2c(port= port, address=i2cAddr)
        self.device = ssd1306(serial)
        pass
    
    def drawSensorReads(self, sensorReads) -> None:
        with canvas(self.device) as draw:
            draw.text((3,5),  f"Humid: {sensorReads.humidity} %", font= self.font, fill= "white")
            draw.text((3,17), f" Temp: {sensorReads.temperature} °C", font= self.font, fill= "white")
            draw.text((3,30), f"  Co2: {sensorReads.co2} ppm", font= self.font, fill= "white")
            
    def drawTest(self) -> None:
        with canvas(self.device) as draw:
            draw.text((3,5),  f"Just Testing", font= self.font, fill= "white")
            draw.ellipse(xy= [(3, 5), (3, 30)], fill= "white")
            
            
if __name__ == '__main__':
        display = OledDisplay()
        display.drawTest()
        time.sleep(5)