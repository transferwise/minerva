#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from pathlib import Path
import pickle
import pandas as pd
import numpy as np
import torch
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

import tools
from data.benchmark_selection import ksg_selection, hsic_selection, boruta_selection


def main():
    xdf, ydf, float_features, cat_features = tools.load_transfer_data(
        'data/transfer3m.csv')
    X_train, X_test, y_train, y_test = train_test_split(
        xdf,
        ydf,
        test_size=0.3,
        random_state=40
    )
    print(f'X_train.shape: {X_train.shape}')
    print(f'X_test.shape: {X_test.shape}')
    print(f'y_train.shape: {y_train.shape}')
    print(f'y_test.shape: {y_test.shape}')
    # ### CatBoost parameters
    params = {
        "iterations": 150,
        "depth": 8,
        "verbose": 10,
        'random_state': 40,
        'verbose': False
    }

    # ## Accuracy of prediction based on all features
    model = CatBoostRegressor(**params)
    model.fit(X_train, y_train)
    train_predictions = model.predict(X_train)
    test_predictions = model.predict(X_test)
    r2_insample = r2_score(y_true=y_train, y_pred=train_predictions)
    r2_outsample = r2_score(y_true=y_test, y_pred=test_predictions)
    print(f'In-sample R2 score: {r2_insample}')
    print(f'Out-sample R2 score: {r2_outsample}')

    # ## Accuracy of prediction based on KSG selection
    X_train_ksg = X_train.loc[:, ksg_selection]
    X_test_ksg = X_test.loc[:, ksg_selection]
    model_ksg = CatBoostRegressor(**params)
    model_ksg.fit(X_train_ksg, y_train)
    train_predictions_ksg = model_ksg.predict(X_train_ksg)
    test_predictions_ksg = model_ksg.predict(X_test_ksg)
    r2_insample_ksg = r2_score(y_true=y_train, y_pred=train_predictions_ksg)
    r2_outsample_ksg = r2_score(y_true=y_test, y_pred=test_predictions_ksg)
    print(f'In-sample R2 score with KSG selection: {r2_insample_ksg}')
    print(f'Out-sample R2 score with KSG selection: {r2_outsample_ksg}')

    # ## Accuracy of prediction based on HSIC selection
    X_train_hsic = X_train.loc[:, hsic_selection]
    X_test_hsic = X_test.loc[:, hsic_selection]
    model_hsic = CatBoostRegressor(**params)
    model_hsic.fit(X_train_hsic, y_train)
    train_predictions_hsic = model_hsic.predict(X_train_hsic)
    test_predictions_hsic = model_hsic.predict(X_test_hsic)
    r2_insample_hsic = r2_score(y_true=y_train, y_pred=train_predictions_hsic)
    r2_outsample_hsic = r2_score(y_true=y_test, y_pred=test_predictions_hsic)
    print(f'In-sample R2 score: {r2_insample_hsic}')
    print(f'Out-sample R2 score: {r2_outsample_hsic}')

    # ## Accuracy of prediction based on boruta selection
    X_train_boruta = X_train.loc[:, boruta_selection]
    X_test_boruta = X_test.loc[:, boruta_selection]
    model_boruta = CatBoostRegressor(**params)
    model_boruta.fit(X_train_boruta, y_train)
    train_predictions_boruta = model_boruta.predict(X_train_boruta)
    test_predictions_boruta = model_boruta.predict(X_test_boruta)
    r2_insample_boruta = r2_score(
        y_true=y_train, y_pred=train_predictions_boruta)
    r2_outsample_boruta = r2_score(
        y_true=y_test, y_pred=test_predictions_boruta)
    print(f'In-sample R2 score: {r2_insample_boruta}')
    print(f'Out-sample R2 score: {r2_outsample_boruta}')


if __name__ == '__main__':
    main()