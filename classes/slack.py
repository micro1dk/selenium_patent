from slacker import Slacker

TOKEN = "xoxb-1810135889392-1792675447012-gBk2MXydPcyU04rxKRRPZnY5"
SLACK = Slacker(TOKEN)

class Slack:
    @staticmethod
    def chat(channel, message):
        SLACK.chat.post_message(f'#{channel}', message)