import logging
import logging.handlers
import requests

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

if __name__ == "__main__":

    r = requests.get('https://goweather.herokuapp.com/weather/austin')
    if r.status_code == 200:
        data = r.json()
        temperature = data['temperature']
        logger.info(f'Weather in Austin: {temperature}')

    
