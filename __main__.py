# Data Aquisition

# Configuration Download

# Data Processing with rule engine exection

# Send Image, Sensors and Alarms to API

import time
from api_service import API_Service
from data_aquisition_service import DataAquisition


def main():
    # Init stuff
    dataAquisition = DataAquisition(nocam=False)
    apiService = API_Service("kibble") # kibble is the dev env auth key
    
    # Run
    while True:
        dataAquisition.run()
        apiService.sendMeasurements(dataAquisition.measurements)
        time.sleep(5)
    
if __name__ == '__main__':
    main()