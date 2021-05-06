import requests

TOKEN = "xoxb-2001561769222-2020540739878-acskLMIsw8DOOEXLe3CCFWfE"

class Slack:
    @staticmethod
    def chat(channel, message):
        response = requests.post("https://slack.com/api/chat.postMessage",
            headers={"Authorization": "Bearer "+ TOKEN},
            data={"channel": channel,"text": message}
        )
 