
import datetime
import json
import requests

from models.measurement import Measurement, MeasurementType
from models.request.PostMeasurementObj import PostMeasurementObj


class API_Service:
    class JsonParser(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()
            if isinstance(obj, MeasurementType):
                return int(obj)
            if isinstance(obj, Measurement):
                return obj.__dict__
            else: 
                print(obj)
    
    def __init__(self, authKey: str, baseUrl:str = "http://192.168.183.142:5145/api") -> None:
        self.url = baseUrl
        # self.headers = {'Content-Type': 'application/json', 'authorization': authKey}
        # self.session = requests.Session()
        # self.session.headers.update(self.headers)
        pass
    
    
    def sendMeasurements(self, measurements: list[Measurement]) -> None:
        pictureList = list(filter(lambda x: x.measurementType == MeasurementType.PICTURE, measurements))
        
        if len(pictureList) > 0:
            picture = pictureList[0]
            savedate = picture.timeStamp
            measurements.remove(picture)
            picturePath = self.sendPicture(picture.value)
            measurements.append(Measurement(savedate, MeasurementType.PICTURE, picturePath, "path"))
        
        requestObj: PostMeasurementObj = PostMeasurementObj(measurements)
        
        try:
            jsonData = json.dumps(requestObj.__dict__, cls=API_Service.JsonParser)
            r = requests.post(f"{self.url}/Sensor/UploadData", json=jsonData)
        except Exception as err:
            print("errorlol")
        pass



    def sendPicture(self, imagePath: str) -> str:
        try:
            files = {'file': open(imagePath, 'rb')}
            r = requests.post(f"{self.url}/Sensor/UploadImage", files=files)
            return r.text
        except:
            print("AAA")

