FROM ubuntu:16.04

# Install dependencies
RUN apt-get -y update && \
    apt-get -y install \
        python3 \
        python3-pip \
        curl \
        wget \
        unzip

# Install Chrome
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get -y update && \
    apt-get -y install \
        google-chrome-stable

# Install ChromeDriver
RUN wget -N http://chromedriver.storage.googleapis.com/2.35/chromedriver_linux64.zip -P ~/
RUN unzip ~/chromedriver_linux64.zip -d ~/ && \
    rm ~/chromedriver_linux64.zip && \
    mv -f ~/chromedriver /usr/local/bin/chromedriver && \
    chown root:root /usr/local/bin/chromedriver && \
    chmod 0755 /usr/local/bin/chromedriver

# Copy Source
COPY . ./nvidiabot
WORKDIR ./nvidiabot

# Install Bot
RUN python3 setup.py install

# Fix Click Python3 ASCII Codes
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

ENTRYPOINT ["nvidiabot", "-c", "./config/config.json"]
