import logging
import logging.handlers
import os
import boto3
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

try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available!"
    # logger.info("Token not available!")
    # raise

def upload_log_to_s3(bucket_name, file_path):
    s3 = boto3.client('s3')
    file_name = os.path.basename(file_path)
    try:
        s3.upload_file(file_path, bucket_name, file_name)
        logger.info(f"Successfully uploaded {file_path} to bucket {bucket_name}.")
    except Exception as e:
        logger.error(f"Failed to upload {file_path} to bucket {bucket_name}: {e}")

if __name__ == "__main__":
    logger.info(f"Token value: {SOME_SECRET}")

    r = requests.get('https://weather.talkpython.fm/api/weather/?city=Berlin&country=DE')
    if r.status_code == 200:
        data = r.json()
        temperature = data["forecast"]["temp"]
        logger.info(f'Weather in Berlin: {temperature}')

    # Upload log file to S3
    BUCKET_NAME = "ec-class-data"
    LOG_FILE_PATH = "status.log"
    upload_log_to_s3(BUCKET_NAME, LOG_FILE_PATH)
