import board
from nltk.util import ngrams

class messageBoard:
    def __init__(self):
        self.yeswords = open('data/yes.txt','r').read().split('\n')
        self.nowords = open('data/no.txt','r').read().split('\n')
        self.module = board.board()

    def intro(self,text,context):
        context["messageBoard"] = {}
        context["messageBoard"]["counter"] = 0
        context["messageBoard"]["inModule"] = False
        context["messageBoard"]["intro"] = False
        return "You make your way to a public bulletin in the center of the station. "\
        "There, people are pinning up or reading messages for anyone to read. Want to "\
        "take a look?, the detective asks, yes, or no?"

    #context["messageBoard"]["stage"]
    #0:never visited 1:return messageBoard 2:survived night 3: caught intruder
    #context["messageBoard"]["inGame"]: T/F
    def response(self,text,context):
        if context["messageBoard"]["intro"] == True:
            context["messageBoard"]["intro"] = False
            return "You find yourself back at the public bulletin. Want to "\
            "take a look?, the detective asks, yes, or no?"
        if context["messageBoard"]["inModule"] == True:
            return self.module.response(text,context)

        if self.yes_representation(text,context) or text.find("look") > -1:
            context["messageBoard"]["inModule"] = True
            if context["messageBoard"]["counter"] == 0:
                return "The detective pushes her way through the crowd to the boards. Let's start looking, she says, "\
                "oh, and when you're done here, just say, go back. " + self.module.intro(text,context)
            else:#context["messageBoard"]["stage"] == 3
                return "The detective pushes her way through the crowd to the boards. Let's start looking, she says, "\
                "oh, and when you're done here, just say, go back. " + self.module.response(text,context)
        elif self.no_representation(text,context):
            context["messageBoard"]["inModule"] = False
            context["status"] = ["Center","inArea","response"]
            context["messageBoard"]["intro"] = True
            return "Alright, says the detective, let's make our way back. You head back to central station proper. In "\
            "the middle of the station is the chatbot, sitting on a bench and twiddling her thumbs worriedly. Next to "\
            "her is a community message board, which the detective points out. We probably won't find any useful info "\
            "there, she says, but we can always check it if you'd like. Otherwise, we can go NORTH, SOUTH, EAST, or "\
            "WEST from here."
        else:
            context["messageBoard"]["inModule"] = False
            return "Hmm, says the detective, distracted by the crowds. Sorry, say again? Do you want to take a look? Yes, or no?"

    def help(self,text,context):
        if context["messageBoard"]["inModule"] == False:
            help_text = "Crowd's pretty loud, huh? the detective says. I'm asking if you want to look at the message boards. Just say yes or no."
        else:
            help_text = self.module.help(text,context)
        return help_text

    def get_caught(self,context):
        raise Exception("get_caught() shall not be called for messageBoard")

    def pause(self,text,context):
        context["status"] = ["Center","inArea","response"]
        context["messageBoard"]["intro"] = True
        return "Alright, says the detective, let's make our way back. You head back to central station proper. In the "\
        "middle of the station is the chatbot, sitting on a bench and twiddling her thumbs worriedly. Next to her is a "\
        "community message board, which the detective points out. We probably won't find any useful info there, she says, "\
        "but we can always check it if you'd like. Otherwise, we can go NORTH, SOUTH, EAST, or WEST from here."

    def repeat(self,text,context):
        return "<prosody rate=\"x-slow\"> " + context["Conversation"][-2]["text"] + "</prosody> "

#===========================================================================
#                       helper functions
#===========================================================================

    def no_representation(self, text, context):
        text = text.lower()
        if (text == "how are you"):
            if (context["intent"] == "AMAZON.NoIntent"):
                return True
            else:
                return False
        if True in [tuple(b.lower().split()) in list(ngrams(text.lower().split(),len(b.lower().split()))) for b in self.nowords]:
            return True
        return False

    def yes_representation(self, text, context):
        text = text.lower()
        if (text == "how are you"):
            if (context["intent"] == "AMAZON.YesIntent"):
                return True
            else:
                return False
        if True in [tuple(b.lower().split()) in list(ngrams(text.lower().split(),len(b.lower().split()))) for b in self.yeswords] :
            return True
        return False
