import configparser
import re
import urllib.request
import pandas as pd
import logging.config

#Load configuration of project
config = configparser.ConfigParser()
config.read('utils/project.cfg')

#Load logging configuration
logging.config.fileConfig('utils/logging.cfg')
logger = logging.getLogger(__name__)

download_url = config['LINKS']['DOWNLOAD_URL']

#Set up logging


def extract_digits(filename):
    """
    :param filename:
    :type filename:
    :return: date string get from file name
    :rtype:
    """
    # Use regex to find all digits in the filename
    digits = re.findall(r'\d+', filename)
    return ''.join(digits)


def crawl_date_table():
    """
    :return: a dataframe that contains index of date from 20040723 to 20240903
    :rtype:
    """
    data = []
    missing_date = []

    for index in range(1, 5761):
        url = f"{download_url}/{index}/WEBPXTICK_DT.zip"
        try:
            with urllib.request.urlopen(url) as response:
                content_disposition = response.headers.get('Content-Disposition')

                if content_disposition is None:
                    missing_date.append(index)
                    logger.info(f"No file found at index {index}. Skipping.")
                    continue

                filename = content_disposition.split('filename=')[1].strip('"')

                date_part = extract_digits(filename)

                data.append([index, date_part])
        except Exception as e:
            logger.error(e)
        else:
            logger.info(f"Crawling successful index of {date_part}.")

    # Create a DataFrame from the data list
    date_table = pd.DataFrame(data, columns=['index', 'date'])
    date_table.to_csv('data/date_index.csv', index=False)

    #Create a Dataframe of missing index date
    missing_date = pd.DataFrame(missing_date, columns=['index'])
    missing_date.to_csv('data/missing_index.csv', index=False)

crawl_date_table()
