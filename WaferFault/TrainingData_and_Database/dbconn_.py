import sqlite3
from os import listdir
import os
import csv
from WaferFault.Application_logging.logger import App_Logger
import shutil


class dbOperation:
    def __init__(self):
        self.path = 'Training_Database/'
        self.goodFilePath = "Training_Raw_files_validated/Good_Raw"
        self.badFilePath = "Training_Raw_files_validated/Bad_Raw/"
        self.logger = App_Logger()

    def dataBaseConnection(self, DatabaseName):

        #   Description: This method creates the database with the given name and
        #   if Database already exists then opens the connection to the DB.
        try:
            """
            sqlite3.connect() If the database file already exists at the specified location, it will connect to the existing database.
            If the database file does not exist, it will create a new database file with the specified name and then connect to it.
            """

            conn = sqlite3.connect(self.path + DatabaseName + '.db')
            file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, f"Opened{DatabaseName}database successfully")
            file.close()
        except ConnectionError:
            file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, f"Error while connecting to database\n{ConnectionError}")
            file.close()
            raise ConnectionError
        return conn

    def createTableDb(self, DatabaseName, column_names):
        try:
            conn = self.dataBaseConnection(DatabaseName)
            cursor = conn.cursor()
            # The query is checking if a table called 'Good_Raw_Data' exists in the database. In SQLite,
            # sqlite_master is a system table that holds metadata about the database, including information about all
            # the tables, indexes, triggers, and views in the database. So the query says, "Count how many entries in
            # sqlite_master are of type 'table' and have the name 'Good_Raw_Data'."
            cursor.execute("SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = 'Good_Raw_Data' ")
            # cursor.fetchone(): This retrieves the first row from the result set returned by the SQL query. Since
            # you're counting entries, there will be only one row with one value (the count).
            if cursor.fetchone()[0] == 1:
                conn.close()
                file = open("Training_Logs/DbTableCreateLog.txt", 'a+')
                self.logger.log(file, "Tables created successfully!!")
                file.close()

                file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
                self.logger.log(file, f"Database{DatabaseName} closed successfully")
                file.close()
            else:
                for key in column_names.keys():
                    d_type = column_names[key]

                    try:
                        conn.execute(
                            'ALTER TABLE Good_Raw_Data ADD COLUMN "{column_name}" {datatype}'.format(column_name=key,
                                                                                                     datatype=d_type))
                    except:
                        conn.execute('CREATE TABLE Good_Raw_Data ({column_name} {dataType})'.format(column_name=key,
                                                                                                    dataType=d_type))

                conn.close()

                file = open("Training_Logs/DbTableCreateLog.txt", 'a+')
                self.logger.log(file, "Tables created successfully!!")
                file.close()

                file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
                self.logger.log(file, "Closed %s database successfully" % DatabaseName)
                file.close()
        except Exception as e:
            file = open("Training_Logs/DbTableCreateLog.txt", 'a+')
            self.logger.log(file, f"Error Occurred while creating table \n {str(e)}")
            file.close()
            conn.close()
            file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, f"{DatabaseName} database closed successfully!!")
            file.close()
            raise e

    def insertIntoTableGoodData(self, Database):

        conn = None
        log_f = open("Training_Logs/DbInsertLog.txt", 'a+')
        try:
            conn = self.dataBaseConnection(Database)
            goodFilePath = self.goodFilePath
            badFilePath = self.badFilePath
            files = [f for f in listdir(goodFilePath)]

            for file in files:
                try:
                    with open(goodFilePath + '/' + file, "r") as f:
                        reader = csv.reader(f, delimiter=",")  # Using comma as the correct delimiter
                        header = next(reader)  # Skip header

                        # Get the number of columns in the database table
                        cursor = conn.cursor()
                        cursor.execute("PRAGMA table_info(Good_Raw_Data)")
                        table_columns = cursor.fetchall()
                        column_count = len(table_columns)

                        self.logger.log(log_f,
                                        f"Inserting data from {file} with {len(header)} columns. Table has {column_count} columns.")

                        # Validate that the CSV column count matches the database column count
                        if len(header) != column_count:
                            raise ValueError(
                                f"Column count mismatch! CSV has {len(header)} columns, but the database table has {column_count} columns.")

                        for row in reader:
                            try:
                                # Insert data using parameterized queries
                                placeholders = ', '.join(['?'] * len(row))  # Create placeholders for each value
                                query = f'INSERT INTO Good_Raw_Data VALUES ({placeholders})'
                                conn.execute(query, row)  # Safely insert values
                                conn.commit()

                                self.logger.log(log_f, f"Row inserted successfully: {row}")
                            except Exception as e:
                                conn.rollback()
                                self.logger.log(log_f, f"Error while inserting row: {row} - {str(e)}")
                                raise e  # Re-raise the exception to handle it in the outer try

                except Exception as e:
                    if conn:
                        conn.rollback()  # Rollback if there's an error with the file
                    self.logger.log(log_f, f"Error while inserting data from file: {file} - {str(e)}")
                    shutil.move(goodFilePath + '/' + file, badFilePath)  # Move file to Bad_Raw folder
                    self.logger.log(log_f, f"File moved to Bad_Raw folder: {file}")

        except Exception as e:
            self.logger.log(log_f, f"General error: {str(e)}")
        finally:
            if conn:
                conn.close()  # Close the connection if it was established
            log_f.close()  # Ensure the log file is closed after processing all files
        """
         Description: This method inserts the Good data files from the Good_Raw folder into the
                                            above created table.

        """


    def selectingDataFromTableIntoCsv(self, Database):
        """\
        Description: This method exports the data in GoodData table as a CSV file. in a given location.
                                            above created
                                            """
        self.fileFromDb = "Training_FileFromDB/"
        self.fileName = "InputFile.csv"
        log_f = open("Training_Logs/ExportToCsv.txt", 'a+')
        try:
            conn = self.dataBaseConnection(Database)
            sqlSelect = "SELECT * FROM Good_Raw_Data"
            cur = conn.cursor()
            cur.execute(sqlSelect)
            results = cur.fetchall()
            # get the headers of the csv file
            headers = [i[0] for i in cur.description]

            # Make the csv output directory
            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)

            # opening csv file for writing
            csvFile = csv.writer(open(self.fileFromDb + self.fileName, 'w', newline=''), delimiter=',',
                                 lineterminator='\r\n', quoting=csv.QUOTE_ALL, escapechar='\\')

            # ADD headers and data
            csvFile.writerow(headers)
            csvFile.writerows(results)

            self.logger.log(log_f, "File exported successfully")
            log_f.close()

        except Exception as e:
            self.logger.log(log_f, f"File exporting failed \n {str(e)} ")
            log_f.close()
