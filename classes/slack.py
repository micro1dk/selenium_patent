import requests

TOKEN = "xoxb-2001561769222-2014505104628-YwFCbhsysY94LhZJhCgSDIEV"

class Slack:
    @staticmethod
    def chat(channel, message):
        response = requests.post("https://slack.com/api/chat.postMessage",
            headers={"Authorization": "Bearer "+ TOKEN},
            data={"channel": channel,"text": message}
        )
 