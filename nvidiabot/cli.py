import json
import logging
import os

import click
from apscheduler.schedulers.background import BlockingScheduler

from nvidiabot.strategy.gagpu import GAGPU


@click.command()
@click.option('--config', '-c', help='path to config json file')
def app(config):
    logger = setup_logger()

    logger.info('Welcome to Nvidia Bot')

    path = os.path.expanduser(config)
    config_file = read_json_file(path)

    logger.info('Adding strategies to job scheduler')

    scheduler = BlockingScheduler()

    strategies = [
        GAGPU()
    ]

    for s in strategies:
        s.set_config(config_file['strategy'][s.config_key])
        duration = config_file['strategy'][s.config_key]['duration']
        scheduler.add_job(s.run, 'interval', **duration)

    logger.info('Scheduler has started')

    scheduler.start()


def setup_logger():
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s'
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger('nvidiabot')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger


def read_json_file(path):
    with open(path) as f:
        return json.load(f)
