import argparse
import joblib
import os
import numpy as np
from sklearn.metrics import mean_squared_error

def test_model(x_test, y_test, model, output_path):
    x_test_data = np.load(x_test)
    y_test_data = np.load(y_test)
    
    model = joblib.load(model)
    y_pred = model.predict(x_test_data)
    #tell you how close a regression line is to a set of points
    err = mean_squared_error(y_test_data, y_pred)
    
    with open(os.path.join(output_path,'output.txt'), 'a') as f:
        f.write(str(err))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--x_test')
    parser.add_argument('--y_test')
    parser.add_argument('--model')
    parser.add_argument('--output_path')
    args = parser.parse_args()
    test_model(args.x_test, args.y_test, args.model, args.output_path)
