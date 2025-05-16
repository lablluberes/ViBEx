import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from missforest import MissForest

def imputate_missforest(data):

    data = pd.DataFrame(data)

    data = data.replace('?', np.nan)

    categorical = list(data.columns)

    print(categorical)

    columns = data.columns[data.isnull().any()].tolist() 

    if columns == []:
        return data.to_dict('records')


    # Initialize the missForest model
    imputer = MissForest(categorical=categorical)

    df_imputed = imputer.fit_transform(data)

    df_imputed = df_imputed[categorical]

    return df_imputed.to_dict('records')



