import numpy as np 
import pandas as pd 

from pandas.api.types import CategoricalDtype

# Function to save dataframes into the same Excel book.
# Using an Excel writer object from pandas.
def save_table_to_sheet(df:pd.DataFrame, path:str, sheet_name:str):
    """This function saves a pandas DataFramte to the given
    `sheet_name` inside the excel book `path`."""

    with pd.ExcelWriter(path=path, mode='a', if_sheet_exists='overlay') as writer:
        df.to_excel(
            excel_writer=writer,
            sheet_name=sheet_name,
            float_format='%.2f'
        )

    return None

# Function to create AAAA, Month label and Day of the Week label from
# a pandas DataFrame with a datetime column column.
def labeled_split_date(dataframe:pd.DataFrame, 
                       date_column:str,
                       labeled_month:bool = False,
                       labeled_day:bool = False
                       ):
    """Returns the DataFrame with labeled columns for the
    month and day of the week in spanish. (Language behaviour should
    be modfied in case of needing labels in english)"""
    df = dataframe.copy()

    # Year AAAA column
    df['Año'] = df[date_column].apply(lambda x: x.year)


    # Month label column
    month_labels = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
         'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    
    # Creating ordered category
    cat_months = CategoricalDtype(categories=month_labels)

    df['Mes'] = (
        df[date_column].apply(lambda x: x.month)
    )
    if labeled_month:
        # mapper dict to create labels
        month_mapper = {(n+1): mes for (n,mes) in enumerate(month_labels)}
        df['Mes'] = df['Mes'].map(month_mapper).astype(cat_months)


    # Day of the Week column
    day_labels = ['Lunes', 'Martes', 'Miercoles', 'Jueves',
            'Viernes', 'Sábado', 'Domingo']
    
    # Creating ordered category
    cat_days = CategoricalDtype(categories=day_labels)

    df['Dia_semana'] = (
        df[date_column].apply(lambda x: x.day_of_week)
    )
    if labeled_day:
        day_mapper = {(n): dia for (n,dia) in enumerate(day_labels)}
        df['Dia_semana'] = df['Dia_semana'].map(day_mapper).astype(cat_days)
    

    return df