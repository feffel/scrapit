FROM python:3.6
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    apt-utils \
    sqlite3 \ 
    wget \
    unzip \ 
    libnss3 \ 
    libgconf-2-4

RUN wget -O chrome.zip https://chromedriver.storage.googleapis.com/2.38/chromedriver_linux64.zip
RUN unzip chrome.zip -d /bin/ && rm chrome.zip 
RUN wget -O chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install gdebi -y
RUN gdebi chrome.deb -n && rm chrome.deb

COPY requirments.txt /requirments.txt
RUN pip install --upgrade pip
RUN pip install -r requirments.txt --user

COPY /start-dev.sh /start-dev.sh
RUN sed -i 's/\r//' /start-dev.sh
RUN chmod +x /start-dev.sh

RUN mkdir /app
WORKDIR /app
ADD . /app/