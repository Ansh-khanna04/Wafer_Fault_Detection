from flask import Flask, request, render_template
from flask import Response
import os
from flask_cors import CORS, cross_origin
import json
from wsgiref import simple_server
from training_data_validation_insertion import train_data_validation
from trainingModel import trainModel
from prediction_validation_insertion import pred_validation
from predictFromModel import Prediction
import flask_monitoringdashboard as dashboard

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)


# @app.route("/", methods=['GET'])
# @cross_origin()
# def home_page():
#     return render_template('index.html')


@app.route("/train", methods=['POST'])
@cross_origin()
def trainRoute():
    try:
        if request.json['folderPath'] is not None:
            path = request.json['folderPath']
            # object initialization
            train_obj = train_data_validation(path)
            # calling the training_validation function
            train_obj.train_validation()
            trainModelobj = trainModel()
            trainModelobj.trainingModel()
    except ValueError:

        return Response("Error Occurred! %s" % ValueError)

    except KeyError:

        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:

        return Response("Error Occurred! %s" % e)
    return Response("Training successful!!")


@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRouteClient():
        try:
            # Log incoming request data
            print(f"Received Request: {request.data}")

            if request.json is not None and 'filepath' in request.json:
                path = request.json['filepath']
                print(f"Filepath from JSON: {path}")
                pred_val = pred_validation(path)
                pred_val.prediction_validation()
                pred = Prediction(path)
                path, json_predictions = pred.predictionFromModel()
                return Response(
                    f"Prediction file created at !!{str(path)} and few of the predictions are {str(json.loads(json_predictions))} ")
            elif request.form is not None:
                path = request.form['filepath']
                pred_val = pred_validation(path)
                pred_val.prediction_validation()
                pred = Prediction(path)
                path, json_predictions = pred.predictionFromModel()
                return Response(
                    f"Prediction file created at !!{str(path)} and few of the predictions are {str(json.loads(json_predictions))} ")
            else:
                print('Nothing matched')
        except ValueError:
            return Response("Error Occurred! %s" % ValueError)
        except KeyError:
            return Response("Error Occurred! %s" % KeyError)
        except Exception as e:
            return Response("Error Occurred! %s" % e)


port = int(os.getenv("PORT", 5000))
if __name__ == "__main__":
    host = '0.0.0.0'
    httpd = simple_server.make_server(host, port, app)
    httpd.serve_forever()
