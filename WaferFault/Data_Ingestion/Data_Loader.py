import pandas as pd


class Data_Getter:
    # This class shall  be used for obtaining the data from the source for training.
    def __init__(self, file_object, logger_object):
        self.training_file = 'Training_FileFromDB/InputFile.csv'
        self.file_object = file_object
        self.logger_object = logger_object

    def get_data(self):
        """\
         Description: This method reads the data from source.
        Output: A pandas DataFrame.
        """
        self.logger_object.log(self.file_object, "ENtered the get data method of data getter class")
        try:
            self.data = pd.read_csv(self.training_file)
            self.logger_object.log(self.file_object,
                                   'Data Load Successful.Exited the get_data method of the Data_Getter class')
            return self.data
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occurred in get_data method of the Data_Getter class. Exception message: ' + str(e))
            self.logger_object.log(self.file_object,
                                   'Data Load Unsuccessful.Exited the get_data method of the Data_Getter class')
            raise Exception()
