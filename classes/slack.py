import requests

TOKEN = "xoxb-2001561769222-2046544931922-v3CQDFNNwxe1TTr77c6cXTF0"

class Slack:
    @staticmethod
    def chat(channel, message):
        response = requests.post("https://slack.com/api/chat.postMessage",
            headers={"Authorization": "Bearer "+ TOKEN},
            data={"channel": channel,"text": message}
        )
 