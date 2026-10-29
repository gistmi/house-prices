import pandas as pd

NONE_COLS = ['PoolQC', 'MiscFeature', 'Alley', 'Fence', 'FireplaceQu',
             'GarageType', 'GarageFinish', 'GarageQual', 'GarageCond',
             'BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1',
             'BsmtFinType2', 'MasVnrType']

ZERO_COLS = ['MasVnrArea', 'GarageYrBlt', 'BsmtFinSF1', 'BsmtFinSF2',
             'BsmtUnfSF', 'TotalBsmtSF', 'BsmtFullBath', 'BsmtHalfBath',
             'GarageCars', 'GarageArea']


def fit_fill_values(train):
    """Learn fill values from the training data only."""
    return {
        'lot_by_nbhd': train.groupby('Neighborhood')['LotFrontage'].median(),
        'lot_overall': train['LotFrontage'].median(),
        'modes': train.select_dtypes(include='object').mode().iloc[0],
        'medians': train.select_dtypes(include='number').median(),
    }


def clean(df, fv):
    """Fill missing values in df using the values learned by fit_fill_values."""
    df = df.copy()
    for col in NONE_COLS:
        df[col] = df[col].fillna('None')
    for col in ZERO_COLS:
        df[col] = df[col].fillna(0)
    df['LotFrontage'] = df['LotFrontage'].fillna(df['Neighborhood'].map(fv['lot_by_nbhd']))
    df['LotFrontage'] = df['LotFrontage'].fillna(fv['lot_overall'])
    df = df.fillna(fv['modes'])
    df = df.fillna(fv['medians'])
    return df