import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer


class Preprocessor:
    # This class shall  be used to clean and transform the data before training.
    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object

    def remove_columns(self, data, columns):
        """
        Description: This method removes the given columns from a pandas dataframe.
                Output: A pandas DataFrame after removing the specified columns.

        """
        self.logger_object.log(self.file_object, "Entered the remove_column method of the preprocessor class")
        self.data = data
        self.columns = columns
        try:
            self.useful_data = self.data.drop(labels=self.columns, axis=1)
            self.logger_object.log(self.file_object,
                                   'Column removal Successful.Exited the remove_columns method of the Preprocessor class')
            return self.useful_data
        except Exception as e:
            self.logger_object.log(self.file_object, f"Exception occurred \n {str(e)}")
            self.logger_object.log(self.file_object, "Column Removal Unsuccessful")

    def separate_label_feature(self, data, label_column):
        self.logger_object.log(self.file_object, 'ENtered into separate label feature')
        try:
            self.X = data.drop(labels=label_column, axis=1)
            self.Y = data[label_column]
            self.logger_object.log(self.file_object,
                                   'Label Separation Successful. Exited the separate_label_feature method of the Preprocessor class')
            return self.X, self.Y
        except Exception as e:
            self.logger_object.log(self.file_object, f'Exception occurred in separate label method\n{str(e)}')
            self.logger_object.log(self.file_object, 'Label Separation Unsuccessful.')
            raise e

    def is_null_present(self, data):
        # checks whether null values are present in my dataset or not
        self.logger_object.log(self.file_object, 'Entered the is_null_present method of the Preprocessor class')
        self.null_present = False
        try:
            self.null_count = data.isna().sum()
            for i in self.null_count:
                if i > 0:
                    self.null_present = True
                    break
            if (self.null_present):
                dataframe_for_null = pd.DataFrame()
                dataframe_for_null['columns'] = data.columns
                # df.isna().sum()  counts the number of missing values for each column, returning a pandas Series.
                # np.asarray() converts the pandas Series into a NumPy array.
                dataframe_for_null['missing_value_counts'] = np.asarray(data.isna().sum())
                dataframe_for_null.to_csv('preprocessing_data/null_values.csv', index=False)
            self.logger_object.log(self.file_object, 'Finding missing values is a success')
            return self.null_present

        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in is_null_present method of the Preprocessor class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'Finding missing values failed. Exited the is_null_present method of the Preprocessor class')
            raise e

    def impute_missing_values(self, data):
        self.logger_object.log(self.file_object, 'Entered the impute_missing_values method of the Preprocessor class')

        try:
            # Identify non-numeric columns
            numeric_data = data.select_dtypes(include=[np.number])
            non_numeric_columns = data.select_dtypes(exclude=[np.number]).columns

            if not non_numeric_columns.empty:
                self.logger_object.log(self.file_object, f'Non-numeric columns dropped: {list(non_numeric_columns)}')

            # Perform imputation only on numeric data
            imputer = KNNImputer(n_neighbors=3, weights='uniform', missing_values=np.nan)
            imputed_array = imputer.fit_transform(numeric_data)
            imputed_data = pd.DataFrame(imputed_array, columns=numeric_data.columns)

            # Combine the imputed numeric data with the non-numeric data
            final_data = pd.concat([imputed_data, data[non_numeric_columns]], axis=1)

            self.logger_object.log(self.file_object, 'Imputed missing values successfully')
            return final_data

        except Exception as e:
            self.logger_object.log(self.file_object,
                                   f'Exception occurred in impute_missing_values, Error message: {str(e)}')
            self.logger_object.log(self.file_object,
                                   'Imputing missing values failed. Exited the impute_missing_values method of the Preprocessor class')
            raise e

    def get_columns_with_zero_std_deviation(self, data):
        self.logger_object.log(self.file_object,
                               'Entered the get_columns_with_zero_std_deviation method of the Preprocessor class')

        try:
            # Get the standard deviation for each column
            std_devs = data.std()  # This will return a Series with the standard deviation of each numeric column
            col_to_drop = std_devs[std_devs == 0].index.tolist()  # Get the columns with std = 0

            self.logger_object.log(self.file_object, f'Columns with zero standard deviation: {col_to_drop}')
            return col_to_drop

        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occurred in get_columns_with_zero_std_deviation method of the Preprocessor class. Exception message: ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'Column search for Standard Deviation of Zero Failed. Exited the get_columns_with_zero_std_deviation method of the Preprocessor class')
            raise Exception(e)

