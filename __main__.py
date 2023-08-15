# Data Aquisition

# Configuration Download

# Data Processing with rule engine exection

# Send Image, Sensors and Alarms to API

import logging
import pigpio
import time
from api_service import API_Service
from data_aquisition_service import DataAquisition
from data_processing_service import DataProcesing


def main():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    # Init stuff
    pi = pigpio.pi()
    dataAquisition = DataAquisition(nocam=True)
    apiService = API_Service("kibble") # kibble is the dev env auth key
    dataprocessing = DataProcesing(pi)
    
    
    logging.debug("starting main loop")
    
    # Run
    while True:
        # get data
        dataAquisition.run()
        logging.info("Data Aquisition finished", dataAquisition.measurements)
        
        # process data
        dataprocessing.process(dataAquisition.measurements)
        logging.info("Data Processing finished")
        
        # Send Data
        # apiService.sendMeasurements(dataAquisition.measurements)
        time.sleep(5)
    
if __name__ == '__main__':
    main()