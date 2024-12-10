from Training_Raw_data_validation.raw_dataValidation import Raw_Data_validation
from Application_logging import logger
from DataTransform_Training.DataTransformation import dataTransform
from TrainingData_and_Database.dbconn_ import dbOperation
from datetime import datetime


class train_data_validation:
    def __init__(self, path):
        self.raw_data = Raw_Data_validation(path)
        self.log_writer = logger.App_Logger()
        self.file_object = open("Training_Logs/Training_Main_log.txt", 'a+')
        self.dataTransform = dataTransform()
        self.dbOperation = dbOperation()

    def train_validation(self):
        try:
            self.log_writer.log(self.file_object, 'Start of validation on files!!')
            # extracting information from schema
            LengthOfDateStamp, LengthOfTimeStamp, number_columns, col_name = self.raw_data.valuesFromSchema()
            # extracting the regex defined to validate
            regex = self.raw_data.manualRegexCreation()
            # validating file name
            self.raw_data.RawDataNameValidation(regex, LengthOfDateStamp, LengthOfTimeStamp)
            # validating column length
            self.raw_data.validateColumnLength(number_columns)
            # validating if any column has all values missing
            self.raw_data.ValidateMissingValuesInWholeColumn()
            self.log_writer.log(self.file_object, "Raw data Validation Completed")
            self.log_writer.log(self.file_object, "Starting data transformation!!")
            # replacing blank in csv file with NULL values
            self.dataTransform.replaceMissing_withNull()
            self.log_writer.log(self.file_object, "DataTransformationCompleted")
            self.log_writer.log(self.file_object, "Creating Training Database on basis of given schema")
            # creating database with given name, if present open the connection
            self.dbOperation.createTableDb('Training', col_name)
            self.log_writer.log(self.file_object, "table creation completed")
            self.log_writer.log(self.file_object, "Insertion of data into table started")

            # inserting csv files into the table
            self.dbOperation.insertIntoTableGoodData('Training')
            self.log_writer.log(self.file_object, "insertion into table completed")
            self.log_writer.log(self.file_object, "DEleting good data folder")

            # delete the good data folder after loading files in table
            self.raw_data.deleteExistingGoodDataTrainingFolder()
            self.log_writer.log(self.file_object, "Good_Data folder deleted!!!")
            self.log_writer.log(self.file_object, "Moving bad files to Archive and deleting Bad_Data folder!!!")
            # Move the bad files to archive folder
            self.raw_data.moveBadFilesToArchiveBad()
            self.log_writer.log(self.file_object, "Bad files moved to archive!! Bad folder Deleted!!")
            self.log_writer.log(self.file_object, "Validation Operation completed!!")
            self.log_writer.log(self.file_object, "Extracting csv file from table")
            # export data in table to csvfile
            self.dbOperation.selectingDataFromTableIntoCsv('Training')
            self.file_object.close()
        except Exception as e:
            raise e
