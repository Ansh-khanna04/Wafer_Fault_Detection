import pickle
import os
import shutil


class File_Operation:
    """
    This class shall be used to save the model after training
                and load the saved model for prediction.
    """

    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object
        self.model_directory = 'models/'

    def save_model(self, model, filename):
        self.logger_object.log(self.file_object, 'Entered the save model method')
        try:
            path = os.path.join(self.model_directory, filename)
            if os.path.isdir(path):
                shutil.rmtree(self.model_directory)
                os.makedirs(path)
            else:
                os.makedirs(path)
            with open(path + '/' + filename + '.sav', 'wb') as f:
                pickle.dump(model, f)
            self.logger_object.log(self.file_object, 'Model File' + filename + 'saved')
            return 'success'
        except Exception as e:
            self.logger_object.log(self.file_object, f'Exception occurred in save model method{str(e)}')
            self.logger_object.log(self.file_object, 'Model file' + filename + 'could not be saved')
            raise Exception()

    def load_model(self, fileName):
        """ loads the model file"""
        self.logger_object.log(self.file_object, 'Entered the load_model method of the File_Operation class')
        try:
            with open(self.model_directory + fileName + '/' + fileName + '.sav', 'rb') as f:
                self.logger_object.log(self.file_object,
                                       'Model File ' + fileName + 'loaded. Exited the load_model method of the Model_Finder '
                                                                  'class')
                return pickle.load(f)
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occurred in load_model method of the Model_Finder class. Exception '
                                   'message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'Model File ' + fileName + ' could not be saved. Exited the load_model method of the Model_Finder class')
            raise Exception()

    def find_correct_model_file(self, cluster_number):
        # Select the correct model based on cluster number
        self.logger_object.log(self.file_object, 'Entered the find_correct_model method')
        try:
            self.cluster_number = cluster_number
            self.folder_name = self.model_directory
            self.list_of_model_files = []
            self.list_of_files = os.listdir(self.folder_name)
            for self.file in self.list_of_files:
                try:
                    if self.file.index(str(self.cluster_number)) != -1:
                        self.model_name = self.file
                except:
                    continue
            self.model_name = self.model_name.split('.')[0]
            self.logger_object.log(self.file_object,
                                   'Exited the find_correct_model_file method of the Model_Finder class.')
            return self.model_name
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occurred in find_correct_model_file method of the Model_Finder class. '
                                   'Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'Exited the find_correct_model_file method of the Model_Finder class with Failure')
            raise Exception()
