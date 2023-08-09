import base64
import os
from picamera2 import Picamera2
import datetime

class Camera:
    def __init__(self, pictureDir: str, width: int = 800, height: int = 600) -> None:
        if not os.path.exists(pictureDir):
            raise FileNotFoundError(f"The path '{pictureDir}' does not exist.")
        self.pictureDir = pictureDir
        self.widht = width
        self.height = height
        self.cam = Picamera2()
        self.captureconfig = self.cam.create_still_configuration(display=None)
        self.cam.configure(self.captureconfig)
        self.cam.start()
    
    def takePicture(self) -> str:
        datestr = datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
        filename = f"{self.pictureDir}/{datestr}.jpg"
        self.cam.capture_file(filename)
        return filename

    # Generates Base64 string and removes the file afterwards
    def takePictureToBase64(self) -> str:
        filename = self.takePicture()
        encoded_string = ""
        try:
            with open(filename, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('ascii')
                os.remove(filename)
        except Exception as e:
            print("Error while encoding picture to base64", e)

        return encoded_string
    
    
if __name__ == "__main__":
    cam = Camera("./debugpics")
    print(cam.cam.camera_controls)
    cam.takePicture()
    cam.takePictureToBase64()
    cam.cam.stop()
    cam.cam.close()