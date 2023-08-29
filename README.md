# MINERVA

### MINE-based feature selection
Minerva is a feature selection tool 
based on 
neural estimation of mutual information 
between
features 
and 
targets.


## Installation
### Install from source
Checkout the repository and navigate to the root directory. Then, 

```
$ poetry install
```

### Run tests
After installation you can run the uni tests by doing:
```
$ poetry run pytest
```

## Run experiments

1. Estimate mutual information between to normal random variables at different level of correlation:
```
$ poetry run python experiments/normalsmile.py
```
Tensorboard logs will be available at `tb_logs/normalsmile/`
The same experiment can be run through the notebook `notebooks/normalsmile.ipynb`.



2. Feature selection in a linear trasnformation setting:
```
$ poetry run python experiments/linear.py
```
Tensorboard logs will be available at `tb_logs/linear/`
The same experiment can be run through the notebook `notebooks/linear.ipynb`.
