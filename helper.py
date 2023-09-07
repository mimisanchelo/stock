import os
from dotenv import load_dotenv
load_dotenv()

headers = {
        "X-RapidAPI-Key": os.getenv('X-API-KEY'),
        "X-RapidAPI-Host": os.getenv('X-API-HOST')}