from Application_logging import logger
from Data_Ingestion import Data_Loader
from Data_Preprocessing import preprocessing
from Data_Preprocessing import Clustering
from sklearn.model_selection import train_test_split
from Best_model_finder import Tuner
from File_Operations import file_methods


class trainModel:
    def __init__(self):
        self.log_writer = logger.App_Logger()
        self.file_object = open("Training_Logs/ModelTrainingLog.txt", 'a+')

    def trainingModel(self):
        self.log_writer.log(self.file_object, "Training process started")
        try:
            # Getting the data from the source
            data_getter = Data_Loader.Data_Getter(self.file_object, self.log_writer)
            data = data_getter.get_data()

            # starting data preprocessing
            preprocessor = preprocessing.Preprocessor(self.file_object, self.log_writer)
            data = preprocessor.remove_columns(data, ['Wafer'])

            # create separate features and labels
            X, Y = preprocessor.separate_label_feature(data, label_column='Output')

            # checking if missing values are present in dataset
            is_null = preprocessor.is_null_present(X)

            # replacing if missing values found
            if is_null:
                X = preprocessor.impute_missing_values(X)

            # checking if any column has standard deviation zero
            col_to_drop = preprocessor.get_columns_with_zero_std_deviation(X)
            # dropping the columns if any
            X = preprocessor.remove_columns(X, col_to_drop)

            """ Applying the clustering approach"""

            kMeans = Clustering.KMeansClustering(self.file_object, self.log_writer)
            n_of_clusters = kMeans.elbow_plot(X)

            X = kMeans.create_clusters(X, number_of_clusters=n_of_clusters)
            X['Labels'] = Y
            Y = X['Labels']
            list_of_clusters = X['Cluster'].unique()

            """parsing all the clusters and looking for the best ML algorithm to fit on individual cluster"""
            for i in list_of_clusters:
                # filter the data for one cluster
                cluster_data = X[X['Cluster'] == i]
                # Prepare the feature and Label columns
                cluster_features = cluster_data.drop(['Labels', 'Cluster'], axis=1)
                cluster_label = cluster_data['Labels']
                # splitting the data into training and test set for each cluster one by one
                x_train, x_test, y_train, y_test = train_test_split(cluster_features, cluster_label, test_size=1 / 3,
                                                                    random_state=355)
                model_finder = Tuner.Model_finder(self.file_object, self.log_writer)
                # getting the best model for each of the cluster

                best_model_name, best_model = model_finder.getBestModel(x_train, y_train, x_test, y_test)

                # saving best model
                file_op = file_methods.File_Operation(self.file_object, self.log_writer)
                save_model = file_op.save_model(best_model, best_model_name + str(i))

            self.log_writer.log(self.file_object, 'Successful End of Training')
            self.file_object.close()

        except Exception:
            # logging the unsuccessful Training
            self.log_writer.log(self.file_object, 'Unsuccessful End of Training')
            self.file_object.close()
            raise Exception
