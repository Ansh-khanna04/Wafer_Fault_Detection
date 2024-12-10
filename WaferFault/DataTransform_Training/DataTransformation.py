from WaferFault.Application_logging.logger import App_Logger
import os
import pandas as pd


class dataTransform:

    #  This class shall be used for transforming the Good Raw Training Data before loading it in Database!!.
    def __init__(self):
        self.goodDataPath = "Training_Raw_files_validated/Good_Raw"
        self.logger = App_Logger()

    def replaceMissing_withNull(self):
        """
        Description: This method replaces the missing values in columns with "NULL" to
                                                        store in the table. We are using substring in the first column to
                                                        keep only "Integer" data for ease up the loading.
                                                        This column is anyways going to be removed during training.
        """
        log_f = open("Training_Logs/dataTransformLog.txt", 'a+')
        try:
            files = [f for f in os.listdir(self.goodDataPath)]
            for file in files:
                df = pd.read_csv(self.goodDataPath + "/" + file)
                if 'Wafer' in df.columns:
                    df.fillna('NULL', inplace=True)
                    df['Wafer'] = df['Wafer'].str[6:]
                    df.to_csv(self.goodDataPath + "/" + file, index=False, header=True)
                    self.logger.log(log_f, f"{file}transformed successfully")
                else:
                    self.logger.log(log_f, f"'{file}' does not contain the 'Wafer' column. Available columns: {list(df.columns)}")
        except Exception as e:
            self.logger.log(log_f, f"Data Transformation Failed because \n {str(e)}")
            log_f.close()
            raise e
        log_f.close()
