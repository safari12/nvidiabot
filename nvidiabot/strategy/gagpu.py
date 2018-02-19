import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from bs4 import BeautifulSoup
from selenium import webdriver

from nvidiabot.strategy import BaseStrategy


class GAGPU(BaseStrategy):

    def __init__(self):
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
            duration='random times every hour with 1200 seconds of jitter',
            config_key='gagpu'
        )

        self.emails = None
        self.logger = logging.getLogger('nvidiabot')

    def run(self):
        self.logger.info('Checking if Nvidia GPUs are in stock')
        gpus = self.get_gpus_from_website()
        available_gpus = self.get_available_gpus(gpus)

        if len(available_gpus) > 0:
            self.logger.info('Nvidia GPUs are in stock!, notifying users')
            self.send_email(available_gpus)
        else:
            self.logger.info('Nvidia GPUs are not in stock :(')

    def set_config(self, config):
        self.emails = config['emails']

    def send_email(self, available_gpus):
        from_addr = 'cryptoinfo69@gmail.com'
        username = os.environ['NVB_SMTP_USERNAME']
        password = os.environ['NVB_SMTP_PASSWORD']

        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Nvidia Bot'
        msg['From'] = from_addr
        msg['To'] = ", ".join(self.emails)

        text = ""

        for gpu in available_gpus:
            text += "%s is available now!\n" % gpu['name']

        text += 'Link to source: \n'
        text += 'https://www.nvidia.com/en-us/geforce/products/10series/geforce-store/'

        msg.attach(MIMEText(text, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)
        server.sendmail(
            from_addr=from_addr,
            to_addrs=self.emails,
            msg=msg.as_string()
        )
        server.quit()

    @staticmethod
    def get_available_gpus(gpus):
        available_gpus = []

        for gpu in gpus:
            status = gpu['status'].lower()

            if 'notify' not in status and 'cart' in status:
                available_gpus.append(gpu)

        return available_gpus

    @staticmethod
    def get_gpus_from_website():
        url = 'https://www.nvidia.com/en-us/geforce/products/10series/geforce-store/'

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')

        client = webdriver.Chrome(chrome_options=options)
        client.get(url)

        soap = BeautifulSoup(client.page_source, 'html.parser')
        gpu_section_div = soap.find('div', attrs={
            'id': 'section-2'
        })

        gpu_info_divs = gpu_section_div.div.find_all('div', recursive=False)

        gpus = []

        for d in gpu_info_divs:
            name_tag = d.find(class_='product-heading1')
            button_tag = d.find(class_='cta-preorder mobile-top')

            if not button_tag:
                button_tag = d.find(class_='varient-button-wrapper')

            gpu_name = name_tag.text.strip()
            gpu_btn_msg = button_tag.a.div.text.strip()

            gpus.append({
                'name': gpu_name,
                'status': gpu_btn_msg
            })

        client.close()

        return gpus
