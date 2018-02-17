from bs4 import BeautifulSoup
from urllib.request import urlopen

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

        self.are_gpus_in_stock()

    def are_gpus_in_stock(self):
        nvidia_url = 'https://www.nvidia.com/en-us/geforce/products/10series/geforce-store/'
        nvidia_html = urlopen(nvidia_url)

        nvidia_soap = BeautifulSoup(nvidia_html, 'html.parser')

        nvidia_section_box = nvidia_soap.find('div', attrs={
            'id': 'section-2'
        })

        nvidia_product_divs = nvidia_section_box.div.find_all('div', recursive=False)

        for d in nvidia_product_divs:
            product_name = d.h2.text.strip()

            print(d.div)

        # for product_col in nvidia_section_box.div.children:
        #     print(product_col['class'])

        # nvidia_section_cols = nvidia_section_box.div.find_next_siblings('div')
        #
        # print(len(nvidia_section_cols))

        # print(nvidia_section_cols[0].find(attrs={
        #     'class': 'product-heading1'
        # }).text.strip())

        # print(nvidia_section_cols[0].h2)

        # for nvs_col in nvidia_section_cols:
        #     print(nvs_col['class'])
