import json
import logging
import time

import pandas as pd


def calculate_age(arg_row, arg_columns):
    arg_serial = arg_row[arg_columns[0]]
    arg_year = arg_row[arg_columns[1]]
    serial_year = arg_serial // 10000
    local_year = 2000 + serial_year if serial_year < 50 else 1900 + serial_year
    result = 2018 + arg_year - local_year
    return result


if __name__ == '__main__':
    start_time = time.time()

    formatter = logging.Formatter('%(asctime)s : %(name)s :: %(levelname)s : %(message)s')
    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    console_handler.setLevel(logging.DEBUG)
    logger.debug('started')

    settings = dict()
    with open('./settings.json', 'r') as json_fp:
        settings = json.load(json_fp)
        logger.debug('settings: %s' % settings)

    input_file = None
    if 'input_file' in settings.keys():
        input_file = settings['input_file']

    if input_file is None:
        logger.warning('input file not supplied; quitting')
        quit()

    columns_of_interest = None
    columns_of_interest_key = 'columns_of_interest'
    if columns_of_interest_key in settings.keys():
        columns_of_interest = settings[columns_of_interest_key]
    else:
        logger.warning('required setting %s not supplied. Quitting.' % columns_of_interest_key)
        quit()

    all_data = pd.read_csv(input_file, usecols=columns_of_interest)
    logger.debug(all_data.columns.values)
    logger.debug(all_data.shape)
    year = columns_of_interest[2]
    serial = columns_of_interest[0]

    data = all_data[all_data[year] == 1]
    logger.debug(data.shape)
    data['Age'] = data.apply(lambda row: calculate_age(row, (serial, year)), axis=1)
    logger.debug(data.shape)
    logger.debug(data.head(10))
    logger.debug('done')
    finish_time = time.time()
    elapsed_hours, elapsed_remainder = divmod(finish_time - start_time, 3600)
    elapsed_minutes, elapsed_seconds = divmod(elapsed_remainder, 60)
    logger.info("Time: {:0>2}:{:0>2}:{:05.2f}".format(int(elapsed_hours), int(elapsed_minutes), elapsed_seconds))
    console_handler.close()
    logger.removeHandler(console_handler)
