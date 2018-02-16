from nvidiabot.strategy import BaseStrategy


class GAGPU(BaseStrategy):

    def __init__(self, config):
        super().__init__(
            name='get available gpu',
            description='notify users by email if nvidia gpus are in stock',
            sources=[
                'nvidia website'
            ],
            params=[{
                'email': [
                    'list, seperated by comma',
                    'require'
                ]
            }],
            duration='random times every hour with 1200 seconds of jitter'
        )

        self.emails = config['emails']

    def run(self):
        print("Emails " + ', '.join(self.emails))
