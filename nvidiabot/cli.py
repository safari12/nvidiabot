import click
import json
import os
import logging

from apscheduler.schedulers.background import BlockingScheduler

from nvidiabot.strategy.gagpu import GAGPU


@click.command()
@click.option('--config', '-c', help='path to config json file')
def app(config):
    setup_logging()

    path = os.path.expanduser(config)
    config_file = read_json_file(path)

    scheduler = BlockingScheduler()

    strategies = [
        GAGPU()
    ]

    for s in strategies:
        s.set_config(config_file['strategy'][s.config_key])
        duration = config_file['strategy'][s.config_key]['duration']
        scheduler.add_job(s.run, 'interval', **duration)

    scheduler.start()


def setup_logging():
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s'
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger('nvidiabot')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)


def read_json_file(path):
    with open(path) as f:
        return json.load(f)
