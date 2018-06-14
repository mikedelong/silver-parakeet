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
    c0, c1, c2, c3, c4, c5 = columns_of_interest

    rename_columns = None
    rename_columns_key = 'rename_columns'
    if rename_columns_key in settings.keys():
        rename_columns = settings[rename_columns_key]
    else:
        logger.warning('required setting %s not supplied. Quitting.' % rename_columns_key)
        quit()
    r0, r1 = rename_columns

    all_data = pd.read_csv(input_file, usecols=columns_of_interest)
    logger.debug(all_data.columns.values)
    logger.debug(all_data.shape)

    years = sorted(all_data[c5].unique())
    logger.debug('years: %s' % str(years))
    colormap = cm.viridis
    color_count = 3
    revived = list()
    for year in years:
        data = all_data[all_data[c5] == year]
        logger.debug('year data shape: %s' % str(data.shape))
        uniques = sorted(data[c3].unique())
        logger.debug('unique blocks: %s' % uniques)
        revived_items = data[data[c1] > 1][c0].values
        revived.extend(revived_items)

        color_list = [colors.rgb2hex(colormap(item)) for item in np.linspace(0, 0.9, color_count)]
        axes = plt.gca()
        mapper = {c2: r1, c4: r0}
        for index, item in enumerate(uniques):
            color = color_list[0 if item < 40 else 1]
            data_to_plot = data[data[c3] == item]
            data_to_plot.rename(mapper, axis='columns', inplace=True)
            life_remaining = data_to_plot[(data_to_plot[r0] > 0) & (~data_to_plot[c0].isin(revived))]
            logger.debug('life remaining shape: %s' % str(life_remaining.shape))
            life_remaining.plot(kind='scatter', x=r1, y=r0, ax=axes, c=color)
            no_life_remaining = data_to_plot[(data_to_plot[r0] == 0) & (~data_to_plot[c0].isin(revived))]
            logger.debug('no life remaining shape: %s' % str(no_life_remaining.shape))
            if len(no_life_remaining) > 0:
                no_life_remaining.plot(kind='scatter', x=r1, y=r0, ax=axes, c='r')
            new_life = data_to_plot[data_to_plot[c0].isin(revived)]
            if len(new_life) > 0:
                new_life.plot(kind='scatter', x=r1, y=r0, ax=axes, c=color_list[2])

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
