
from ast import List
import requests

from models.measurement import Measurement, MeasurementType


class API_Service:
    class DateTimeEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()
    
    def __init__(self, authKey: str, baseUrl:str = "http://localhost:5145/api") -> None:
        self.url = baseUrl
        self.headers = {'Content-Type': 'application/json', 'authorization': authKey}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        pass
    
    
    def sendMeasurements(self, measurements: list[Measurement]) -> None:
        if list(filter(lambda x: x.measurement_type == MeasurementType.PICTURE, measurements)) < 0:
            picture = list(filter(lambda x: x.measurement_type == MeasurementType.PICTURE, measurements))[0]
            savedate = picture.timestamp
            measurements.remove(picture)
            picturePath = self.sendPicture(picture.value)
            measurements.append(Measurement(savedate, MeasurementType.PICTURE, picturePath, "path"))
        json = []
        for measurement in measurements:
            json.append(measurement.__dict__)
        self.session.post(f"{self.url}/measurements", json=json)
        pass


    def sendPicture(self, imagePath: str) -> str:
        with open(imagePath, 'rb') as f:
            r = self.session.post(f"{self.url}/Sensor/UploadImage", files={'file': f})
            return r.text
