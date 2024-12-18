from datetime import datetime
from os import listdir
import pandas
from WaferFault.Application_logging.logger  import App_Logger


class dataTransformPredict:
    def __init__(self):
        self.goodDataPath = "Prediction_Raw_Files_Validated/Good_Raw"
        self.logger = App_Logger()


    def replaceMissingWithNull(self):
        try:
            log_file = open("Prediction_Logs/dataTransformationLog.txt",'a+')
            onlyFiles = [f for f in listdir(self.goodDataPath)]
            for file in onlyFiles:
                csv = pandas.read_csv(self.goodDataPath+"/"+file)
                csv.fillna('NULL',inplace = True)
                csv['Wafer'] = csv['Wafer'].str[6:]
                csv.to_csv(self.goodDataPath+"/"+file , index = False,header=True)
                self.logger.log(log_file, " %s: File Transformed successfully!!" % file)
        except Exception as e:
            self.logger.log(log_file , "Data Transformation failed because:: %s" % e)
            log_file.close()
            raise e
        log_file.close()

