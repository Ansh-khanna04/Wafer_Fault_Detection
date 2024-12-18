import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import KneeLocator
from WaferFault.File_Operations.file_methods import File_Operation
from WaferFault.Application_logging.logger import App_Logger


class KMeansClustering:
    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object

    def elbow_plot(self, data):
        """
        Description: This method saves the plot to decide the optimum number of clusters to the file.
                        Output: A picture saved to the directory

        """
        self.logger_object.log(self.file_object, 'Entered the elbow plot method of KmeansClustering Class')
        wcss = []
        try:
            for i in range(1, 11):
                kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
                kmeans.fit(data)
                wcss.append(kmeans.inertia_)
            plt.plot(range(1, 11), wcss)
            plt.title('The Elbow Method')
            plt.xlabel('Number of Clusters')
            plt.ylabel('WCSS')
            plt.savefig('preprocessing_data/K-Means_Elbow.PNG')

            self.kn = KneeLocator(range(1, 11), wcss, curve='convex', direction='decreasing')
            self.logger_object.log(self.file_object, f'The optimum number of clusters is:{str(self.kn.knee)}')
            return self.kn.knee

        except Exception as e:
            self.logger_object.log(self.file_object,
                                   f'Exception occured in elbow_plot method of the KMeansClustering class. Exception message:{str(e)}')
            self.logger_object.log(self.file_object, 'Finding the number of clusters failed.')
            raise Exception()

    def create_clusters(self, data, number_of_clusters):
        """
         Description: Create a new dataframe consisting of the cluster information.
                                Output: A dataframe with cluster column

        """
        self.logger_object.log(self.file_object, 'Entered the create_clusters method of the KMeansClustering class')
        self.data = data
        try:
            self.kmeans = KMeans(n_clusters=number_of_clusters, init='k-means++', random_state=42)
            # dividing data into clusters
            self.y_kmeans = self.kmeans.fit_predict(data)
            self.file_op = File_Operation(self.file_object, self.logger_object)
            # saving the KMeans model to directory
            self.save_model = self.file_op.save_model(self.kmeans, 'KMeans')
            self.data['Cluster'] = self.y_kmeans
            self.logger_object.log(self.file_object, f"successfully created {str(self.kn.knee)} clusters")
            return self.data
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occurred in create_clusters method of the KMeansClustering class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'Fitting the data to clusters failed. Exited the create_clusters method of the KMeansClustering class')
            raise Exception()
