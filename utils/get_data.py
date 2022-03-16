import pandas as pd

def get_data():
    """Gets summary data from S3
    Returns:
        - df (pandas.DataFrame): Dataframe containing the sumamry stats
        """
    # read summary stats from S3

    data = pd.read_parquet(r"https://fundmapper.s3.eu-central-1.amazonaws.com/05-FinalTables/summary_stats.parquet")

    return data

def format_data(df):
    """Formats the data so JS can handle it
    Args:
        - df (pandas.core.DataFrame): table containing raw data

    Returns:
        - data (dict): dictionary containing the data and associated colors
        """


    data = df

    # Get a fitting date format
    data['date'] = pd.to_datetime(data['date'], format='%Y%m', errors='coerce')

    # convert to billions
    data['sum_amount'] = data['sum_amount'] / 10 ** 9

    data['color'] = data['investmenttypedomain'].map(
        {'Government/Agency': "#D29DC0",
         'Other Tax Exempt Fund': "#E7DCCA",
         'Prime': "#9CCBC0",
         'Single State Fund': "#E6C9C5",
         'Treasury': "#92A0CF",
         'Other': "#C2D6C4",
         }
    )
    # fill missing data
    data['mean_yield'].fillna(-99, inplace=True)

    # put in list of records
    data = data.to_dict('records')

    return data
