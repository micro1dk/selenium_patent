import requests

TOKEN = "xoxb-2001561769222-2020540739878-tPCZH1bKHGInYEnR7mW0cP78"

class Slack:
    @staticmethod
    def chat(channel, message):
        response = requests.post("https://slack.com/api/chat.postMessage",
            headers={"Authorization": "Bearer "+ TOKEN},
            data={"channel": channel,"text": message}
        )
 