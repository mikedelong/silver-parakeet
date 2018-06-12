import json
import logging
import time

import pandas as pd

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

    data = pd.read_csv(input_file)
    logger.debug(data.columns.values)

    logger.debug('done')
    finish_time = time.time()
    elapsed_hours, elapsed_remainder = divmod(finish_time - start_time, 3600)
    elapsed_minutes, elapsed_seconds = divmod(elapsed_remainder, 60)
    logger.info("Time: {:0>2}:{:0>2}:{:05.2f}".format(int(elapsed_hours), int(elapsed_minutes), elapsed_seconds))
    console_handler.close()
    logger.removeHandler(console_handler)
