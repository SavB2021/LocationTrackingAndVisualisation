# Location Tracking and Visualisation

This is a simple Python 3 Flask app which accepts coordinate data in the form of an xlsx or csv file and return a graph tracking the orute along with a moving speed graph.

## Requirements
Python 3 installed


## To run the App, input the following commands in the terminal
* Activate your virtual python environment either by using the pipenv shell command or with source env/bin/activate (please enrue that you are in the package root directory _/LocationCaptureAndVisualisation_)
* Install requirement from requirement.txt file with pip install -r requirements.txt
* Run export FLASK_APP=locationTrack 
* Run export FLASK_ENV=development
* To initialise the app run flask run
* Once the app has started up go to http://127.0.0.1:5000/upload and follow the prompts


#### Note:
* A test data file has been included with the repository (route_df.csv), it contains location data for a route on the west coast of the United States
* Also included is a file called binarySearch.py which includes a short algorithm to return the next smallest number, given an array and an integer