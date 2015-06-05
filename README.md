# datarobot
DataRobot data science excercise

#Data source
The data for this excercise was acquired from Kaggle (https://www.kaggle.com/c/facebook-recruiting-iv-human-or-bot/data). The competition organized by Facebook required competitors to use the provided data to determine whether an auction bid originated from a human or a robot

The original training file was processed to create the train and test files used for this excercise.

#File Descriptions
train.csv : used to create predictive model using Google Prediction API.

Columns: 
1. outcome - class variable (1 for robot, 0 for human)
2. bidder_id - unique identifier of bidder
3. payment_account - account used to make payments
4. address - origin of bid
         
test.csv : used to test the predictive model created using Google Prediction API.

Columns: same as those of train.csv

example_predictions.csv : sample output after running prediction.py.

Columns: 
1. predicted_outcome - outcome predicted by prediction model
2. actual_outcome - actual outcome from test file for given row
3. bidder_id - unique identifier of bidder
4. payment_account - account used to make payments
5. address - origin of bid

client_secrets.json : contains client ID and client secrets used for OAuth authentication with Google API

prediction.py : python script to generate predictions from model.

#Script
#prediction.py
Use this python script to get predictions built previously using the Google Prediction API. The script uses the test.csv file to generate predicted outcomes for each line using the bidder_id, payment_account and address columns. 

The resulting file created after running this script is 'predictions.csv' which contains the predicted_outcome, actual_outcome, bidder_id, payment_account and address columns. The example_predictions.csv file included in this folder gives an example output of one run of prediction.py.

#How to run
1. Open client_secrets.json and put in appropriate values for client_id and client_secret. Save the file.
2. Install Google API for python dependencies using the following link:
   https://developers.google.com/api-client-library/python/start/installation
3. In the command line or terminal, change your working directory to that containing prediction.py and accompanying files.
4. Run the following command:
   python prediction.py datarobotassignment/train.csv datarobotmodel 773026801896

When the script runs successfully, predictions.csv would be created in the folder. Open this file to view the results of the predictions.
