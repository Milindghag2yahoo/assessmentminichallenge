import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
import sys
import json


def load_data(learner_file, learner_workspace):
    y_learner = pd.read_csv(learner_file)
    y_actual = pd.read_csv(learner_workspace + 'actual.csv')
    return y_learner,y_actual

def validate_submission(y_learner,y_actual):
    error = 0
    msg = "No error"
    if(list(y_learner.columns) != list(y_actual.columns)):
        msg = "The column names of the submission file do not match the submission format."
        error = 1

    if(y_learner.shape[0] != y_actual.shape[0]):
        msg = "The submission file should contain {} records".format(y_actual.shape[0])
        error = 1

    if(y_learner.shape[1] != y_actual.shape[1]):
        msg = "The submission file should contain {} columns".format(y_actual.shape[1])
        error = 1

    return error,msg

def score_submission(y_learner,y_actual):
	mse = mean_squared_error(y_learner.num_orders, y_actual.num_orders) 

	if mse<6500:
		projected_points = 1
	elif (mse>6500) and (mse<10000):
		projected_points = 0.75
	elif mse>10000:
		projected_points = 0

	return mse,projected_points
if __name__ == "__main__":
    learner_file = sys.argv[1]
    learner_workspace = sys.argv[2]
    y_learner,y_actual = load_data(learner_file, learner_workspace)
    err,msg = validate_submission(y_learner,y_actual)
    if(err == 1):
        result = json.dumps({'error_msg':msg})
        print(result, end='')
    else:
    	raw_score,projected_points = score_submission(y_learner,y_actual)
    	result = json.dumps({'raw_score': raw_score,'multiplier':projected_points})
    	print(result, end='')