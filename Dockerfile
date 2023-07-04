FROM prefecthq/prefect:2-python3.11


#COPY scraper.py /app/


COPY requirements.txt .




#COPY links.txt /opt/prefect/data/links.txt
#COPY flows /opt/prefect/flows
#Uncomment above two lines if you want to have the flows and data in docker container
 

RUN apt-get -y update
RUN apt-get -y install wget 
RUN apt-get -y install gnupg


RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
# Updating apt to see and install Google Chrome

#RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#RUN apt install ./google-chrome-stable_current_amd64.deb

RUN apt-get install -y google-chrome-stable
RUN apt-get install -yqq unzip
# Download the Chrome Driver
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
# Unzip the Chrome Driver into /usr/local/bin directory
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
# Set display port as an environment variable
ENV DISPLAY=:99


RUN pip3 install -r requirements.txt
