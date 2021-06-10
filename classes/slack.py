import requests
from dotenv import dotenv_values
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

config = dotenv_values('.env')

TOKEN = config['SLACK']

class Slack:
    @staticmethod
    def chat(channel, message):
        response = requests.post("https://slack.com/api/chat.postMessage",
            headers={"Authorization": "Bearer "+ TOKEN},
            data={"channel": channel,"text": message}
        )
 