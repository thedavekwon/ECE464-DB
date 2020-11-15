## NoSQL (MongoDB) project with Webscraper

## Installation
```
git clone https://github.com/thedavekwon/ECE464-DB.git
cd ECE464-DB/hw2
# Create your own venv if you prefer venv
pip install -r requirements.txt
```

## Configuration
```
# Acquire Reddit Key and mongo server and provide following information as config-sample.ini
[REDDIT]
client_id = 
client_secret = 
user_agent = 
subreddit_list_path = 
num_process = 

[MONGO]
host = 
port = 
```


## Usage
```
# Get Top 1000 Subreddit List from http://redditlist.com
# Configure subreddit list path in config/config.ini
python src/scraper.py --gen -c config/config.ini

# Run Scraper
python src/scraper.py -c config/config.ini

# Run Client
python src/client.py -c config/config.ini

# Test Client
pytest test/test_client.py
```
