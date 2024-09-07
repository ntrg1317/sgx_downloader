import configparser
import logging.config
import os
import urllib.request
from datetime import timedelta, datetime
from helpers.dates import format_date, get_id_by_date

#Load configuration of project
config = configparser.ConfigParser()
config.read('utils/project.cfg')

#Load configuration of logging
logging.config.fileConfig('utils/logging.cfg', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

#Get params from configuration
url = config['LINKS']['DOWNLOAD_URL']
filenames=["WEBPXTICK_DT.zip", "TickData_structure.dat", "TC.txt", "TC_structure.dat"]

def create_file_path(path, output_dir):
    full_path = os.path.join(output_dir, path)
    if len(path):
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
    return full_path


def download_file(date: str, id :int, filename: str, output_dir):
    """
    :param filename:
    :type filename:
    :param id:
    :type id:
    :param date:
    :type date:
    :return:
    :rtype:
    """
    folder = f"SGXFILES_{date}/"
    download_url = f"{url}/{id}/{filename}"
    with urllib.request.urlopen(download_url) as response:
        content_disposition = response.headers.get('Content-Disposition')

        if content_disposition is None:
            raise Exception (f"Error downloading file {filename} of {date}")

        dl_filename = content_disposition.split('filename=')[1].strip('"')
        save_path = create_file_path(folder, output_dir) + dl_filename

        if os.path.exists(save_path):
            raise Exception(f"File {filename} already exists")
        else:
            urllib.request.urlretrieve(download_url, save_path)

def download_day_file(date: str, output_dir):
    exist_files = []
    index = get_id_by_date(date)
    if index is None:
        logger.info(f"No data files for date {date}")
    else:
        for filename in filenames:
            try:
                download_file(date, index, filename, output_dir)
            except Exception as e:
                if 'already exists' in str(e):
                    exist_files.append(filename)
                else:
                    logger.error(e)
        logger.info(f"Finished downloading all files for date {date}")

def download_batch_day_file(start_date: str, end_date: str, output_dir):
    formatted_start_date = format_date(start_date)
    formatted_end_date = format_date(end_date)

    curr_date = formatted_start_date
    while curr_date <= formatted_end_date:
        date = curr_date.strftime('%Y%m%d')
        try:
            download_day_file(date, output_dir)
        except ValueError as e:
            logger.error(f"Error while downloading files for {date}: {e}")
        curr_date += timedelta(days=1)