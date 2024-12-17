# https://understandingdata.com/posts/install-google-chrome-selenium-ec2-aws/
sudo curl https://intoli.com/install-google-chrome.sh | bash
sudo mv /usr/bin/google-chrome-stable /usr/bin/google-chrome
google-chrome --version && which google-chrome

# https://selenium-python.readthedocs.io/installation.html
# https://sites.google.com/chromium.org/driver/downloads?authuser=0
# https://googlechromelabs.github.io/chrome-for-testing/
wget https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.139/linux64/chromedriver-linux64.zip
unzip chromedriver-linux64.zip && cd chromedriver-linux64
sudo mv chromedriver /usr/local/bin/
chromedriver --version && which chromedriver
