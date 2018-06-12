from module import module
from chat import chatbot
class chitchat(module):
    def __init__(self):
        super().__init__()
        self.chatbot = chatbot()
    def response(self,text,context):
        response = self.chatbot.response(text)
        return response
