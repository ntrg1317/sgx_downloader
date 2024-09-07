# SGX Download Project

## Overview

The SGX Download Project is designed to download financial data files from a specified URL. The project allows for batch downloads over a range of dates or individual downloads for specific dates. It also includes functionality to schedule daily downloads.

## Features

- **Batch Download**: Download files for a range of dates.
- **Single/Multiple Date Download**: Download files for specific dates.
- **Daily Scheduler**: Automatically run daily downloads at a specified time.
- **Configurable Output Directory**: Set the directory where files will be saved.
- **Logging**: Detailed logging for tracking and debugging.

## Requirements

- Python 3.8 or later
- Required Python libraries: `configparser`, `logging`, `schedule`

## Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd data_mini_test
   ```

2. **Create and activate a virtual environment** (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install required packages**:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Configuration Files**:
   - `utils/project.cfg`: Contains configuration parameters for the project.
   - `utils/logging.cfg`: Contains configuration for logging.

2. **Logging Configuration**: Update `utils/logging.cfg` to configure log settings and output destinations.

## Usage

### Command-Line Interface

The main script `main.py` can be executed with various options. The general syntax is:

```bash
python3 src/main.py [options]
```

### Options

- `--output`: Specify the output directory where files will be saved (default: `~/output`).
- `-batch`: Perform a batch download from the specified start date to the end date.
- `--start-date`: Specify the start date for batch download in the format YYYYMMDD.
- `--end-date`: Specify the end date for batch download in the format YYYYMMDD.
- `--date`: Specify one or more specific dates for individual downloads in the format YYYYMMDD.
- `-daily`: Schedule the task to run daily.
- `--exec-at`: Specify the daily execution time in HH:MM format.

### Examples

- **Batch Download**:
  ```bash
  python3 main.py -batch --start-date 20230901 --end-date 20230910
  ```

- **Single Date Download**:
  ```bash
  python3 main.py --date 20230901
  ```

- **Multiple Date Download**:
  ```bash
  python3 main.py --date 20230901 20230902 20230905
  ```

- **Daily Scheduler**:
  ```bash
  python3 main.py -daily --exec-at 17:00
  ```
## Contact

For questions or comments, please reach out to [TrangNguyen](mailto:trangnt1317@gmail.com).

---