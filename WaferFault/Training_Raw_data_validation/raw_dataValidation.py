from datetime import datetime
import os
from os import listdir
import re
import json
import shutil
import pandas as pd
from Application_logging.logger import App_Logger


class Raw_Data_validation:

    # this class should be used to handle all the raw training data!!
    def __init__(self, path):
        self.Batch_Directory = path
        self.schema_path = 'schema_training.json'
        self.logger = App_Logger()

    def valuesFromSchema(self):
        """
         Description: This method extracts all the relevant information from the pre-defined "Schema" file.
                        Output: LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, Number of Columns
                        On Failure: Raise ValueError,KeyError,Exception
        """
        try:
            with open(self.schema_path, 'r') as f:
                dic = json.load(f)
                f.close()
                pattern = dic['SampleFileName']
                LengthOfDateStampInFile = dic['LengthOfDateStampInFile']
                LengthOfTimeStampInFile = dic['LengthOfTimeStampInFile']
                NumberOfColumns = dic['NumberOfColumns']
                Column_Name = dic['ColName']

                file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
                message = "LengthOfDateStampInFile:: %s" % LengthOfDateStampInFile + "\t" + "LengthOfTimeStampInFile:: %s" % LengthOfTimeStampInFile + "\t" + "Numberofcolumns :: %s" % NumberOfColumns + "\n"
                self.logger.log(file, message)
                file.close()

        except ValueError:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file, "ValueError:Value not found inside schema_training.json")
            file.close()
            raise ValueError

        except KeyError:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file, "KeyError :incorrect key passed")
            file.close()
            raise KeyError

        except Exception as e:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file, str(e))
            file.close()
            raise e

        return LengthOfDateStampInFile, LengthOfTimeStampInFile, NumberOfColumns, Column_Name

    def manualRegexCreation(self):
        """
        Description: This method contains a manually defined regex based on the "FileName" given in "Schema" file.
                                            This Regex is used to validate the filename of the training data.
        """

        """
        
         Description : A regex (short for regular expression) is a sequence of characters that forms a search pattern, 
        primarily used for string searching, matching, and manipulation. In Python, regular expressions are implemented through the re module, which allows for advanced string matching using patterns.
        
        """

        regex = r'^wafer_\d{8}_\d{6}\.csv$'
        return regex

    def createDirectoryForGoodBadRawData(self):

        """
         Description: This method creates directories to store the Good Data and Bad Data
                                                    after validating the training data.

        """
        try:
            # This line creates a file path for the "Good_Raw" folder inside a parent folder called
            # Training_Raw_files_validated.
            path = os.path.join("Training_Raw_files_validated/", "Good_Raw/")
            if not os.path.isdir(path):
                os.makedirs(path)
            path = os.path.join("Training_Raw_files_validated/", "Bad_Raw")
            if not os.path.isdir(path):
                os.makedirs(path)
        except OSError as ex:
            file = open("Training_Logs/GeneralLog.txt", 'a+')
            self.logger.log(file, f"Error while creating directory:{str(ex)}")
            file.close()
            raise OSError

    def deleteExistingGoodDataTrainingFolder(self):
        """
         Description: This method deletes the directory made  to store the Good Data
                       after loading the data in the table. Once the good files are
                        loaded in the DB,deleting the directory ensures space optimization.

        """

        try:
            path = "Training_Raw_files_validated/"
            # This checks if the Good_Raw/ directory exists inside the Training_Raw_files_validated/ directory.
            # os.path.isdir() returns True if the directory exists, otherwise False.
            if os.path.isdir(path + 'Good_Raw/'):
                shutil.rmtree(path + 'Good_Raw/')
                """
                shutil.rmtree(path + 'Good_Raw/') will only delete the Good_Raw/ directory and all its contents (files and subdirectories, if any) 
                within the Training_Raw_files_validated folder
                """
                file = open("Training_Logs/GeneralLog.txt", "a+")
                self.logger.log(file, "GoodRaw directory deleted successfully!!")
                file.close()
        except OSError as e:
            file = open("Training_Logs/GeneralLog.txt", "a+")
            self.logger.log(file, f"Error while deleting good_raw files{str(e)}")
            file.close()
            raise OSError

    def deleteExistingBadDataTrainingFolder(self):
        try:
            path = "Training_Raw_files_validated/"
            if os.path.isdir(path + "Bad_Raw/"):
                shutil.rmtree(path + "Bad_Raw/")
                file = open("Training_Logs/GeneralLog.txt", "a+")
                self.logger.log(file, "Bad raw files deleted successfully!!")
                file.close()
        except OSError as e:
            file = open("Training_Logs/GeneralLog.txt", "a+")
            self.logger.log(file, f"Error while deleting bad files{str(e)}")
            file.close()
            raise OSError

    def moveBadFilesToArchiveBad(self):
        """
         Description: This method deletes the directory made  to store the Bad Data
                                                          after moving the data in an archive folder. We archive the bad
                                                          files to send them back to the client for invalid data issue.

        """
        now = datetime.now()
        # datetime.now() retrieves the current local date and time from the system clock.
        date = now.date()
        time = now.strftime("%H%M%S")
        try:
            src = "Training_Raw_files_validated/Bad_Raw/"
            if os.path.isdir(src):
                # This code checks whether the Bad_Raw/ directory exists within the Training_Raw_files_validated/
                # directory.
                path = "Training_Archive_Bad_Data"
                if not os.path.isdir(path):
                    os.makedirs(path)
                dest = "Training_Archive_Bad_Data/BadData_" + str(date) + "_" + str(time)
                if not os.path.isdir(dest):
                    os.makedirs(dest)
                files = os.listdir(src)
                for f in files:
                    if f not in os.listdir(dest):
                        shutil.move(src + f, dest)
                file = open("Training_Logs/GeneralLog.txt", "a+")
                self.logger.log(file, "Bad files moved to archive")
                path = "Training_Raw_files_validated/"
                if os.path.isdir(path + 'Bad_Raw/'):
                    shutil.rmtree(path + 'Bad_Raw/')
                self.logger.log(file, "BAd Raw data deleted successfully !!")
                file.close()

        except Exception as e:
            file = open("Training_Logs/GeneralLog.txt", "a+")
            self.logger.log(file, f"Error Occurred{str(e)}")
            file.close()
            raise e

    def RawDataNameValidation(self, regex, LengthOfDateStampInFile, LengthOfTimeStampInFile):
        """
        Description: This function validates the name of the training csv files as per given name in the schema!
                                 Regex pattern is used to do the validation.If name format do not match the file is moved
                                 to Bad Raw Data folder else in Good raw data.

        """
        self.deleteExistingGoodDataTrainingFolder()
        self.deleteExistingBadDataTrainingFolder()
        self.createDirectoryForGoodBadRawData()
        files_to_be_validated = [f for f in listdir(self.Batch_Directory)]
        try:
            f = open("Training_Logs/nameValidationLog.txt", 'a+')
            for filename in files_to_be_validated:
                if re.match(regex, filename):
                    splitAt = re.split('.csv', filename)
                    splitAt = (re.split('_', splitAt[0]))
                    if len(splitAt[1]) == LengthOfDateStampInFile:
                        if len(splitAt[2]) == LengthOfTimeStampInFile:
                            shutil.copy("Training_Batch_Files/" + filename, "Training_Raw_files_validated/Good_Raw/")
                            self.logger.log(f, f"Valid File name!! {filename} moved to GoodRawFolder")

                        else:
                            shutil.copy("Training_Batch_Files/" + filename, "Training_Raw_files_validated/Bad_Raw/")
                            self.logger.log(f, f"Wrong File name!! {filename} moved to BadRawFolder")
                    else:
                        shutil.copy("Training_Batch_Files/" + filename, "Training_Raw_files_validated/Bad_Raw/")
                        self.logger.log(f, f"Wrong File name!! {filename} moved to BadRawFolder")
                else:
                    shutil.copy("Training_Batch_Files/" + filename, "Training_Raw_files_validated/Bad_Raw/")
                    self.logger.log(f, f"Wrong File name!! {filename} moved to BadRawFolder")
            f.close()

        except Exception as e:
            f = open("Training_Logs/nameValidationLog.txt", 'a+')
            self.logger.log(f, f"Error Occurred \n {str(e)}")
            f.close()
            raise e

    def validateColumnLength(self, NumberOfColumns):
        try:
            f = open("Training_Logs/columnValidation.txt", 'a+')
            self.logger.log(f, "Column length validation Started")
            for file in listdir('Training_Raw_files_validated/Good_Raw/'):
                csv = pd.read_csv("Training_Raw_files_validated/Good_Raw/" + file)
                if csv.shape[1] == NumberOfColumns:
                    pass
                else:
                    shutil.move("Training_Raw_files_validated/Good_Raw/" + file,
                                "Training_Raw_files_validated/Bad_Raw/")
                    self.logger.log(f, f"Invalid Column Length of{file} , moved to bad folder")
            self.logger.log(f, "Column Length Validation Completed")
        except OSError:
            f = open("Training_Logs/columnValidation.txt", 'a+')
            self.logger.log(f, f"Error Occurred while moving the file::%s " % OSError)
            f.close()
            raise OSError
        except Exception as e:
            f = open("Training_Logs/columnValidation.txt", 'a+')
            self.logger.log(f, f"Error Occurred \n {str(e)}")
            f.close()
            raise e
        f.close()

    def ValidateMissingValuesInWholeColumn(self):
        """
        Description: This function validates if any column in the csv file has all values missing.
                                               If all the values are missing, the file is not suitable for processing.
                                               SUch files are moved to bad raw data.
        """
        try:
            f = open("Training_Logs/missingValueInColumn.txt", 'a+')
            self.logger.log(f, "Missing Values validation Started!!")

            for file in listdir('Training_Raw_files_validated/Good_Raw/'):
                df = pd.read_csv("Training_Raw_files_validated/Good_Raw/" + file)
                count = 0
                for columns in df:
                    # len(df[columns])will give length of each column including null values
                    # df[columns].count() will give non-null values in each column
                    if (len(df[columns]) - df[columns].count()) == len(df[columns]):
                        count += 1
                        shutil.move("Training_Raw_files_validated/Good_Raw/" + file,
                                    "Training_Raw_files_validated/Bad_Raw/")
                        self.logger.log(f, f"Invalid Column Length for the {file},moved to bad raw folder")
                        break
                if count == 0:
                    df.rename(columns={"Unnamed:0": "Wafer"}, inplace=True)
                    df.to_csv("Training_Raw_files_validated/Good_Raw/" + file, index=False, header=True)
        except OSError:
            f = open("Training_Logs/missingValueInColumn.txt", 'a+')
            self.logger.log(f, "Error Occurred while moving the file::%s" % OSError)
            f.close()
            raise OSError
        except Exception as e:
            f = open("Training_Logs/missingValueInColumn.txt", 'a+')
            self.logger.log(f, f"Error occurred \n {str(e)}")
            f.close()
            raise e
        f.close()
