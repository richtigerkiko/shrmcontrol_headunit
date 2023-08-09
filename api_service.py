
import json
import requests

from models.measurement import Measurement, MeasurementType


class API_Service:
    class DateTimeEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()
    
    def __init__(self, authKey: str, baseUrl:str = "http://192.168.183.142:5145/api") -> None:
        self.url = baseUrl
        # self.headers = {'Content-Type': 'application/json', 'authorization': authKey}
        # self.session = requests.Session()
        # self.session.headers.update(self.headers)
        pass
    
    
    def sendMeasurements(self, measurements: list[Measurement]) -> None:
        pictureList = list(filter(lambda x: x.measurement_type == MeasurementType.PICTURE, measurements))
        if len(pictureList) > 0:
            picture = pictureList[0]
            savedate = picture.timestamp
            measurements.remove(picture)
            picturePath = self.sendPicture(picture.value)
            measurements.append(Measurement(savedate, MeasurementType.PICTURE, picturePath, "path"))
        jsonData = []
        for measurement in measurements:
            jsonData.append(measurement.__dict__)
        self.session.post(f"{self.url}/measurements", json=jsonData)
        pass


    def sendPicture(self, imagePath: str) -> str:
        # self.session.headers = {'Content-Type: multipart/form-data'}
        # self.session.headers.update({'Content-Type: multipart/form-data'})
        # r = self.session.post(f"{self.url}/Sensor/UploadImage", files={'file': f})
        
        try:
            files = {'file': open(imagePath, 'rb')}
            r = requests.post(f"{self.url}/Sensor/UploadImage", files=files)
            return r.text
        except:
            print("AAA")
                

            
