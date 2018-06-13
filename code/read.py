import json
import logging
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import cm
from matplotlib import colors

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

    with open('./settings.json', 'r') as json_fp:
        settings = json.load(json_fp)
        logger.debug('settings: %s' % settings)

    input_file = None
    if 'input_file' in settings.keys():
        input_file = settings['input_file']
    else:
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
    c1 = columns_of_interest[1]
    c2 = columns_of_interest[2]
    c3 = columns_of_interest[3]
    c4 = columns_of_interest[4]

    years = sorted(all_data[c4].unique())
    logger.debug('years: %s' % str(years))
    colormap = cm.viridis
    for year in years:
        data = all_data[all_data[c4] == year]
        logger.debug('data shape: %s' % str(data.shape))
        uniques = sorted(data[c2].unique())
        logger.debug('unique blocks: %s' % uniques)
        color_list = [colors.rgb2hex(colormap(item)) for item in np.linspace(0, 0.9, len(uniques))]
        axes = plt.gca()
        for index, item in enumerate(uniques):
            color = color_list[index]
            data_to_plot = data[data[c2] == item]
            life_remaining = data_to_plot[data_to_plot[c3] > 0]
            no_life_remaining = data_to_plot[data_to_plot[c3] == 0]
            life_remaining.plot(kind='scatter', x=c1, y=c3, ax=axes, c=color)
            if len(no_life_remaining) > 0:
                no_life_remaining.plot(kind='scatter', x=c1, y=c3, ax=axes, c='r')

        output_filename = '../output/year{:02d}.png'.format(year)
        logger.debug('writing scatter plot to %s' % output_filename)
        plt.savefig(output_filename)
        plt.close()

    logger.debug('done')
    finish_time = time.time()
    elapsed_hours, elapsed_remainder = divmod(finish_time - start_time, 3600)
    elapsed_minutes, elapsed_seconds = divmod(elapsed_remainder, 60)
    logger.info("Time: {:0>2}:{:0>2}:{:05.2f}".format(int(elapsed_hours), int(elapsed_minutes), elapsed_seconds))
    console_handler.close()
    logger.removeHandler(console_handler)
