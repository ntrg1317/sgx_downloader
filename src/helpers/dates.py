import configparser
import logging.config
import re
import urllib.request
from datetime import datetime
import numpy as np
import pandas as pd

#Load configuration of project
config = configparser.ConfigParser()
config.read('utils/project.cfg')

#Load logging configuration
logging.config.fileConfig('utils/logging.cfg', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

#Get params from configuration
download_url = config['LINKS']['DOWNLOAD_URL']

date_table = pd.read_csv(f"data/date_index.csv")

def get_earliest_date() -> str:
    earliest_date = date_table['date'].min()
    earliest_date_str = str(earliest_date)

    return earliest_date_str

def get_id_by_date(date: str):
    """
    :param date: Date in format YYYYMMDD
    :type date: str
    :return: index of date
    :rtype: int
    """
    last_date = str(date_table["date"].iloc[-1])
    last_id = date_table["index"].iloc[-1]

    # If date is after last date then calculate the index else find index in date table
    index = get_id_from_date_table(date)
    if index == 0:
        index = last_id + business_days_count(last_date, date)
        actual_date = get_date_by_id(index)
        if actual_date == date:
            new_row = pd.DataFrame({"index": [index], "date": [date]})
            new_date_table = (pd.concat([date_table, new_row], ignore_index=True)
                              .sort_values(by='index')
                              .reset_index(drop=True))
            new_date_table.to_csv("data/date_index.csv", index=False)
            return index
        else:
            return None
    else:
        return index

def get_date_by_id(id: int):
    url = f"{download_url}/{id}/WEBPXTICK_DT.zip"
    with urllib.request.urlopen(url) as response:
        content_disposition = response.headers.get('Content-Disposition')

        if content_disposition is None:
            return None

        filename = content_disposition.split('filename=')[1].strip('"')

        digits = re.search(r'\d+', filename)
        if digits is not None:
            return digits.group()

        return None

def business_days_count(start_date: str, end_date: str) -> int:
    """
    :param start_date: Date in format YYYYMMDD
    :type start_date: str
    :param end_date: Date in format YYYYMMDD
    :type end_date: str
    :return: Number of business days between start_date and end_date
    :rtype: int
    """
    # Convert string dates to datetime objects
    start_date = format_date(start_date)
    end_date = format_date(end_date)

    # Calculate the number of business days
    return np.busday_count(start_date, end_date)

def get_date_diff(start_date: str, end_date: str) -> int:
    """
    :param start_date: Date in format YYYYMMDD
    :type start_date: str
    :param end_date: Date in format YYYYMMDD
    :type end_date: str
    :return: Number of days between start_date and end_date
    :rtype: int
    """
    start_date = format_date(start_date)
    end_date = format_date(end_date)

    return (end_date - start_date).days

def format_date(date: str) -> datetime.date:
    try:
        return datetime.strptime(date, '%Y%m%d').date()
    except ValueError as e:
        raise e

def get_id_from_date_table(date: str) -> int:
    if not date_table.loc[date_table['date'] == int(date)].empty:
        return date_table.loc[date_table['date'] == int(date), 'index'].iloc[0]
    else:
        return 0
