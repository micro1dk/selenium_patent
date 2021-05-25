import requests

TOKEN = "xoxb-2001561769222-2046544931922-uE7xgKwKjuXdXbdeusOD4U46"

class Slack:
    @staticmethod
    def chat(channel, message):
        response = requests.post("https://slack.com/api/chat.postMessage",
            headers={"Authorization": "Bearer "+ TOKEN},
            data={"channel": channel,"text": message}
        )
 