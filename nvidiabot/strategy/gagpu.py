from bs4 import BeautifulSoup
from selenium import webdriver

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
        url = 'https://www.nvidia.com/en-us/geforce/products/10series/geforce-store/'

        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        client = webdriver.Chrome(chrome_options=options)
        client.get(url)

        soap = BeautifulSoup(client.page_source, 'html.parser')
        gpu_section_div = soap.find('div', attrs={
            'id': 'section-2'
        })

        gpu_info_divs = gpu_section_div.div.find_all('div', recursive=False)

        for d in gpu_info_divs:
            name_tag = d.find(class_='product-heading1')
            button_tag = d.find(class_='cta-preorder mobile-top')

            if not button_tag:
                button_tag = d.find(class_='varient-button-wrapper')

            gpu_name = name_tag.text.strip()
            gpu_btn_msg = button_tag.a.div.text.strip()

            print(gpu_name)
            print(gpu_btn_msg)

        client.close()
