import argparse
import os
import sys
import joblib
import numpy as np
from sklearn.linear_model import SGDRegressor

def train_model(x_train, y_train, model_path):
    x_train_data = np.load(x_train)
    y_train_data = np.load(y_train)
# type of model
    model = SGDRegressor(verbose=1)
    model.fit(x_train_data, y_train_data)
# packaging model into a file we can use later
    joblib.dump(model, os.path.join(model_path,'model.joblib'))


if __name__ == '__main__':
# accepting the file paths to the training data, from the pipeline.py
    print(sys.argv)
    print(os.listdir("/home/jovyan"))
    parser = argparse.ArgumentParser()
    parser.add_argument('--x_train')
    parser.add_argument('--y_train')
    parser.add_argument('--model_path')
    args = parser.parse_args()
    train_model(args.x_train, args.y_train, args.model_path)
