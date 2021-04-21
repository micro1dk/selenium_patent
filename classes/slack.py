from slacker import Slacker

TOKEN = "xoxb-1810135889392-1792675447012-wm28PTf2qAI1EUy2goa9lTic"
SLACK = Slacker(TOKEN) 

class Slack:
    @staticmethod
    def chat(channel, message):
        SLACK.chat.post_message(f'#{channel}', message)