
import datetime
import json
import logging
import socket
import requests

from models.measurement import Measurement, MeasurementType
from models.request.PostMeasurementObj import PostMeasurementObj
from models.ruleset import FallbackRuleSet, RuleSet


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
        pass
    
    
    def sendMeasurements(self, measurements: list[Measurement]) -> None:
        pictureList = list(filter(lambda x: x.measurementType == MeasurementType.PICTURE, measurements))
        
        if len(pictureList) > 0:
            picture = pictureList[0]
            measurements.remove(picture)
            picturePath = self.sendPicture(picture.value)
        requestObj: PostMeasurementObj = PostMeasurementObj(measurements)
        
        try:
            jsonData = json.dumps(requestObj.__dict__, cls=API_Service.JsonParser)
            # save to file
            with open(f"./debug/{requestObj.timeStamp.isoformat()}.json", "w") as stream:
                stream.write(jsonData)
            r = requests.post(f"{self.url}/Sensor/UploadData", data=jsonData, headers={'Content-Type': 'application/json'}, timeout=5)
        except Exception as err:
            print("errorlol")
        pass



    def sendPicture(self, imagePath: str) -> str:
        try:
            files = {'file': open(imagePath, 'rb')}
            r = requests.post(f"{self.url}/Sensor/UploadImage", files=files, timeout=5)
            return r.text
        except:
            print("AAA")
            
    def getConfiguration(self) -> RuleSet:
        try:
            hostname = socket.gethostname()
            r = requests.get(f"{self.url}/Rules/GetActiveRuleSet?hostname={hostname}")
            if(r.status_code != 200):
                logging.error(f"Error while fetching ruleset: {r.status_code}")
                return FallbackRuleSet().ruleset
            return RuleSet.from_json(r.text)
        except Exception as err:
            logging.error(err)
            return FallbackRuleSet().ruleset

if __name__ == "__main__":
    api = API_Service("test", "https://shroomcontrol.warumhalbmast.de/api")
    api.getConfiguration()