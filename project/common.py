from datetime import datetime
import os
import csv

LOG_FILE = "log.log"

def log_text(text:str):
    """Appends text to log file"""
    out = datetime.now().isoformat() + ": \n" + text + "\n"
    open(LOG_FILE, 'a').writelines(out)

def export_log(row, header):

    # Write to Csv
    py_dir = os.path.realpath(__file__)
    csv_dir = py_dir.replace(".py", "_log.csv")
    file_exists = os.path.isfile(csv_dir)

    f = open(csv_dir, 'a')

    writer = csv.writer(f, delimiter=";", lineterminator='\n')
    if not file_exists:
        writer.writerow(header)
    writer.writerow(row)