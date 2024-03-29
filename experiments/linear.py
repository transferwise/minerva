#!/usr/bin/env python
# coding: utf-8

from typing import Sequence
from pathlib import Path
import pandas as pd
import numpy as np

import minerva


pth = Path('./data/linear')
pth.mkdir(exist_ok=True, parents=True)


# Parameters for the synthetis of data
n = 50000
dx = 10
num_relevant = 2
dy = 1
feature_cols = [f'f{n}' for n in range(dx)]
float_features = feature_cols  # all features are continuous
cat_features = []  # none of the features is categorical
cat_feat_sizes = []
targets = [f'y{n}' for n in range(dy)]
train_size = int(.66 * n)
val_size = int(.15 * n)
test_size = n - train_size - val_size


# Metaparameters
num_samples = n
dimension_of_residual_block = 512
num_res_layers = 4
scaler = 2  # Scaler = 4 did the best so far, scaler=8 diverged
emb_dim = 1

# Batches and epochs
batch_size = scaler*2048


# No-regularisation train control
noreg_train_control = minerva.feature_selection.TrainControl(
    model_name='noreg_linear',
    data_path='data/',
    number_of_epochs=4000,
    number_of_segments=1,
    learning_rate=5e-6,
    reg_coef=.0,
    projection_init=.25,
    disable_projection=True,
)

# Selection train control
select_train_control = minerva.feature_selection.TrainControl(
    model_name='selection_linear',
    data_path='data/',
    number_of_epochs=4000,
    number_of_segments=2,
    learning_rate=1e-6,
    reg_coef=1e4,
    projection_init=None,
    disable_projection=False,
)

# Pack hyperparameters
selector_params = dict(
    cat_features=cat_features,
    float_features=float_features,
    targets=targets,
    dim1_max=dimension_of_residual_block,
    num_res_layers=num_res_layers,
    eps=.001,
    cat_feat_sizes=cat_feat_sizes,
    emb_dim=emb_dim,
)
logger_params = dict(
    name="linear"
)


def synthesize_data(
    n: int,
    dx: int,
    num_relevant: int,
    feat_sizes: Sequence[int],
    dy: int,
    train_size: int,
    val_size: int,
    test_size: int,
):
    x = np.random.uniform(size=(n, dx))
    expected = np.random.choice(dx, replace=False, size=num_relevant)
    y = (
        np.random.uniform(size=(1, dy, num_relevant)
                          ) @ np.expand_dims(x[:, expected], axis=2)
    )[:, :, 0]
    feature_cols = [f'f{n}' for n in range(dx)]
    target_cols = [f'y{n}' for n in range(dy)]
    expected_features = list(np.array(feature_cols)[expected])
    xdf = pd.DataFrame(
        x,
        columns=feature_cols
    )
    ydf = pd.DataFrame(
        y,
        columns=target_cols
    )
    data = pd.concat((xdf, ydf), axis=1)
    train_data = data.iloc[:train_size]
    val_data = data.iloc[train_size: train_size + val_size]
    test_data = data.iloc[train_size + val_size:]

    return expected_features, train_data, val_data, test_data


def main():

    # Synthesize the data
    expected_features, train_data, val_data, test_data = synthesize_data(
        n=n,
        dx=dx,
        num_relevant=num_relevant,
        feat_sizes=cat_feat_sizes,
        dy=dy,
        train_size=train_size,
        val_size=val_size,
        test_size=test_size,
    )

    # Run feature selection
    selected_features, selector = minerva.feature_selection.run(
        train_data=train_data,
        val_data=val_data,
        test_data=test_data,
        float_features=float_features,
        categorical_features=cat_features,
        targets=targets,
        selector_params=selector_params,
        logger_params=logger_params,
        noreg_train_control=noreg_train_control,
        select_train_control=select_train_control,
        batch_size=batch_size,
    )

    import pdb
    pdb.set_trace()

    # print results
    print(
        f'Normalised coefficients of the projection matrix:\n{selector.normalized_proj()}\n')
    print(f'Selected features:\n{selector.selected_feature_names()}\n')
    print(f'Expected features:\n{expected_features}\n')

    print(
        f'Mutual information on train dataset: {float(selector.train_mutual_information())}')
    print(
        f'Mutual information on val dataset: {float(selector.val_mutual_information())}')
    print(
        f'Mutual information on test dataset: {float(selector.test_mutual_information())}')


if __name__ == '__main__':
    main()
