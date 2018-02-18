import smtplib
import os

from bs4 import BeautifulSoup
from selenium import webdriver
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from nvidiabot.strategy import BaseStrategy


def is_gpu_available(gpu):
    status = gpu['status'].lower()

    return \
        'notify' not in status and \
        'cart' in status


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

        gpus = self.get_gpus_from_website()

        self.send_email([{
            'name': '1070'
        }, {
            'name': '1080'
        }, {
            'name': '1060'
        }])

        for gpu in gpus:
            if is_gpu_available(gpu):
                print('GPU is available')

        print('done')

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
    def get_gpus_from_website():
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
