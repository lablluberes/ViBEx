##############################################
#
# This file contains Missforest and IterativeImputer (MICE) imputation function
#
##############################################
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from missforest import MissForest
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.linear_model import LogisticRegression
import random

def imputate_missforest(data):
    """
        imputate_missforest - imputates vales based on ML MissForest

        data: binarization dataset
    """
    random.seed(42)
    
    # read data
    data = pd.DataFrame(data)

    all_nan_columns = data.isnull().all()

    if np.array(all_nan_columns).any():
        print("data has column with all nan")
        return data.to_dict('records')


    # replace undecided with nans
    data = data.replace('?', np.nan)

    # get the genes 
    categorical = list(data.columns)

    #print(categorical)

    # verify if there are nan values (if not then dont need to imputate)
    columns = data.columns[data.isnull().any()].tolist() 

    if columns == []:
        return data.to_dict('records')


    # Initialize the missForest model
    imputer = MissForest(categorical=categorical)

    # fit and transform dataset
    df_imputed = imputer.fit_transform(data)

    # organize dataset
    df_imputed = df_imputed[categorical]

    # return imputation
    return df_imputed.to_dict('records')


def imputate_mice_logictic(data):

    """
        imputate_mice_logictic - imputates vales based on IterativeImputer (MICE)

        data: binarization dataset
    """

    # read data
    data = pd.DataFrame(data)

    all_nan_columns = data.isnull().all()

    if np.array(all_nan_columns).any():
        print("data has column with all nan")
        return data.to_dict('records')

    # replace undecided with nans
    data = data.replace('?', np.nan)

    # verify if there are nan values (if not then dont need to imputate)
    columns = data.columns[data.isnull().any()].tolist() 

    if columns == []:
        return data.to_dict('records')


    imputer = IterativeImputer(estimator=LogisticRegression(), max_iter=10, random_state=0)

    data_imputed = imputer.fit_transform(data)
    data_imputed = pd.DataFrame(data_imputed, columns=data.columns, index=data.index)
    df = data_imputed.round(0).astype('Int64')

    return df.to_dict('records')



