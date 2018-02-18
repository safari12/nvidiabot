import click
import configparser
import os

from apscheduler.schedulers.background import BlockingScheduler

from nvidiabot.strategy.gagpu import GAGPU


@click.command()
@click.option('--config', '-c', help='path to config file')
def app(config_path):
    path = os.path.expanduser(config_path)
    config_parser = configparser.ConfigParser()

    config_file = config_parser.read(path)

    scheduler = BlockingScheduler()

    strategies = [
        GAGPU()
    ]

    for s in strategies:
        s.config = config_file[s.config_key]
        scheduler.add_job(s.run, 'interval', seconds=10, jitter=5)

    scheduler.start()
