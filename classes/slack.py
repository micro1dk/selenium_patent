import requests

TOKEN = "xoxb-2001561769222-2046544931922-0zY8FyxaVEfCrOQNsaRCP2hn"

class Slack:
    @staticmethod
    def chat(channel, message):
        response = requests.post("https://slack.com/api/chat.postMessage",
            headers={"Authorization": "Bearer "+ TOKEN},
            data={"channel": channel,"text": message}
        )
 