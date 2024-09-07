import argparse
import os
import logging.config
from datetime import datetime, timedelta
import time
import schedule
from download import download_day_file, download_batch_day_file
from helpers.dates import get_earliest_date, get_date_diff
from helpers.dates import business_days_count

#Load configuration of logger
logging.config.fileConfig('utils/logging.cfg', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def validate_time(execution_time: str):
    try:
        datetime.strptime(execution_time, "%H:%M")
        return True
    except ValueError:
        return False

def validate_date(date: str, name: str):
    try:
        if date is None:
            return None

        datetime.strptime(date, '%Y%m%d')

        earliest_date = get_earliest_date()
        today = datetime.today().strftime('%Y%m%d')

        if get_date_diff(earliest_date, date) < 0:
            print(f'ERROR: {name} - {date} out of range. Date must be on or after {earliest_date}.')
            exit()
        if get_date_diff(date, today) <= 0:
            print(f'ERROR: {name} - {date} out of range. Date must be before {datetime.today().date()} in the format YYYYMMDD.')
            exit()

        return date

    except ValueError:
        print(f'ERROR: Invalid {name}, must be in YYYYMMDD format (passed \'{date}\')')
        exit()

if __name__ == '__main__':
    today = datetime.today().strftime('%Y%m%d')
    default_start_date = get_earliest_date()
    default_end_date = (datetime.now() - timedelta(1)).strftime('%Y%m%d')

    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=str, help='Specify output directory', default='~/output')
    parser.add_argument('-batch', action='store_true', help='Batch download from start date to end date')
    parser.add_argument('--start-date', type=str, help='Specify start date in the format YYYYMMDD',
                        default=default_start_date)
    parser.add_argument('--end-date', type=str, help='Specify end date in the format YYYYMMDD',
                        default=default_end_date)
    parser.add_argument('--date', type=str, nargs='*',
                        help='Specify zero or more dates in the format YYYYMMDD', default=None)
    parser.add_argument('-daily', action='store_true', help='Run the daily task scheduler')
    parser.add_argument('--exec-at', type=str, help='Specify the daily execution time in HH:MM format', default='17:00')

    args = parser.parse_args()

    dates = [validate_date(date, 'date') for date in args.date] if args.date else None
    output_dir = os.path.expanduser(args.output)  # Expand ~ to user home directory
    batch = args.batch
    daily = args.daily
    exec_at = args.exec_at

    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logger.info(f"Created output directory: {output_dir}")
    # Process dates
    if batch:
        start_date = validate_date(args.start_date, 'start date')
        end_date = validate_date(args.end_date, 'end date')

        total_business_days = business_days_count(start_date, end_date)
        if total_business_days < 0:
            logger.error("Start date must be before or equal to end date.")
            exit()
        if total_business_days > 100:
            logger.info(f"About {total_business_days} files will be downloaded. It will take a long time to complete.")
            user_input = input("Continue? (y/n): ").strip().lower()
            if user_input == 'y':
                logger.info("User confirmed to continue.")
                download_batch_day_file(start_date, end_date, output_dir)
            elif user_input == 'n':
                logger.info("User chose not to continue. Exiting...")
                exit()
            else:
                logger.info("Invalid input. Exiting...")
                exit()
            logger.info(f"Starting batch download from {start_date} to {end_date}")
        else:
            download_batch_day_file(start_date, end_date, output_dir)
    elif dates:
        for date in dates:
            logger.info(f"Downloading files for date: {date}")
            download_day_file(date, output_dir)
    if daily:
        if validate_time(exec_at):
            date = (datetime.now() - timedelta(1)).strftime('%Y%m%d')
            logger.info(f"Scheduling task to run daily at {exec_at}")
            schedule.every().day.at(exec_at).do(lambda: download_day_file(date))
            while True:
                schedule.run_pending()
                time.sleep(1)
        else:
            logger.error("Invalid --exec-at time format.")
            exit(1)
