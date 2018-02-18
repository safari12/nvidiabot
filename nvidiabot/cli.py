import click

from apscheduler.schedulers.background import BlockingScheduler

from nvidiabot.strategy.gagpu import GAGPU


@click.command()
def app():
    scheduler = BlockingScheduler()

    gagpu = GAGPU(
        config={
            'emails': [
                'rsafari.s@gmail.com',
                'safarimining12@gmail.com',
                'rezasafari@icloud.com'
            ]
        }
    )

    scheduler.add_job(gagpu.run, 'interval', seconds=10, jitter=5)

    scheduler.start()
