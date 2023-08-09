# Data Aquisition

# Configuration Download

# Data Processing with rule engine exection

# Send Image, Sensors and Alarms to API

from api_service import API_Service
from data_aquisition_service import DataAquisition


def main():
    # Init stuff
    dataAquisition = DataAquisition(nocam=True)
    apiService = API_Service("kibble") # kibble is the dev env auth key
    
    # Run
    dataAquisition.run()
    apiService.sendMeasurements(dataAquisition.measurements)
    
if __name__ == '__main__':
    main()