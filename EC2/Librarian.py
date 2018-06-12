import wordGame
import riddle
from nltk.util import ngrams
#allow play same two games?  eg: 2 rounds of word game then 2 hints
class Librarian:
    def __init__(self):
        self.yeswords = open('data/yes.txt','r').read().split('\n')
        self.nowords = open('data/no.txt','r').read().split('\n')
        self.wordGame = wordGame.wordGame()
        self.riddle = riddle.riddle()
        self.module = self.wordGame

    def intro(self,text,context):
        context["Librarian"] = {}
        context["Librarian"]["stage"] = 0
        context["Librarian"]["inGame"] = False
        context["Librarian"]["inChoose"] = False
        context["Librarian"]["intro"] = False
        return "You find your way to the university library. A young woman with thick "\
        "glasses and a bowtie stands at the front desk, holding an open book in her hands. "\
        "She waves you over and starts to speak. Hello, I'm the librarian, she says. "\
        "You're looking for whoever stole the chatbot's voice, right? Beat me in a game of "\
        "wits and I'll tell you what I know! So, what'll it be? Yes, or no?"

    #context["Librarian"]["stage"]
    #0:1st game unfinished 1:1st finished, 2nd unfinished 2:both finished
    #context["Librarian"]["inGame"]: T/F
    #context["Librarian"]["inChoose"]: T/F
    def response(self,text,context):
        if context["Librarian"]["intro"] == True:
            context["Librarian"]["intro"] = False
            if context["Librarian"]["stage"] == 0:#1st game unfinished
                return "You find yourself in the university library. The librarian waves you over. "\
                "Hello again! she says, Still looking for whoever stole the chatbot's voice? Beat "\
                "me in a game of wits and I'll tell you what I know. So, what'll it be? Yes, or no?"
            elif context["Librarian"]["stage"] == 1:#1st game finished, 2nd unfinished
                return "You find yourself in the university library, where the librarian waves you "\
                "over. Hello again! she says. I happened to overhear something else about the "\
                "chatbot's voice. Beat me in a game of wits and I'll tell you what else I've learned! "\
                "So, what'll it be? Yes, or no?"
            else:#2nd finished
                return "You find yourself in the university library, where the librarian waves you "\
                "over. Hello again! she says. I've already told you all I know, but I'd be more than "\
                "happy to play a game with you again. So, what'll it be? Yes, or no?"

        if context["Librarian"]["inGame"] == True:
            response,stage = self.module.response(text,context)
            if stage == 1:#user win
                context["Librarian"]["inGame"] = False
                if context["hintIndex"] >= len(context["hints"]):
                    response = "Turns out, a chatbot's voice is pretty powerful. I don't really understand it all, but it really shouldn't be tampered with."
                else:
                    context["status"] = ["Center","inArea","response"]
                    context["hintIndex"] += 1
                    hintStr = context["hints"][context["hintIndex"]]
                    context["Librarian"]["intro"] = True
                    response += " The librarian takes off her glasses and busies herself with cleaning "\
                    "them. I never thought anyone would beat me, she says, but fair's fair. Here's what "\
                    "I know. " + hintStr + " . The detective quickly jots it down in her notebook, "\
                    "then hurries you back to Central Station. Nice work with that bookworm, she says. "\
                    "If you ever want to check your hints, just say, HINTS, and I'll go over them with you. "\
                    "Where should we go next? Northern University, the Eastern Commons, Southern Square, or "\
                    "the Western Woods?"
                return response
            elif stage == 2:#user lose
                context["Librarian"]["inGame"] = False
                response += " The librarian pushes her glasses up, grinning victoriously. You did well, "\
                "she says, but it looks like I win this one. How about another go? Yes, or no?"
            else:#stage == 0 #normal round
                pass
            return response

        if context["Librarian"]["inChoose"] == True:
            context["Librarian"]["inChoose"] = False
            if text.find("first") > -1 or text.find("word") > -1 or text.find("game") > -1:
                context["Librarian"]["inGame"] = True
                self.module = self.wordGame
                return "A word game it is then, the librarian says chipperly. If you can last for 10 turns, I'll admit defeat. " + self.module.intro(text,context)
            elif text.find("second") > -1 or text.find("last") > -1 or text.find("riddle") > -1 or text.find("challenge") > -1:
                context["Librarian"]["inGame"] = True
                self.module = self.riddle
                return "Alrighty then, she says, adjusting her bowtie. Solve 3 of these riddles, and you win. " + self.module.intro(text,context)
            elif text.find("no") > -1 or text.find("don't want") > -1 or text.find("neither") > -1 or text.find("none") > -1:
                context["status"] = ["North","inArea","response"]
                context["Librarian"]["intro"] = True
                return "Alright, the librarian says. If you change your mind, I'll be here. You find yourself back at the "\
                "University entrance. The detective turns to you. So, who should we talk to? she asks, The librarian again, or the "\
                "Doctor? If you think we should check somewhere else, just tell me a direction and we'll go there."
            else:
                return "The librarian busies herself with her book, attempting to hide the fact that she didn't understand you. "\
                "Sorry, she says, but could you tell me again, do you want to play me in a word game, or face my riddle challenge?"

        if self.yes_representation(text,context) or text.find("play") > -1 or text.find("challenge") > -1 or text.find("game") > -1:
            context["Librarian"]["inChoose"] = True
            return "Great! says the librarian, snapping her book shut. We can either play a word game, "\
            "or I can challenge you with some riddles. Which one will it be?"
        elif self.no_representation(text,context):
            context["status"] = ["North","inArea","response"]
            context["Librarian"]["intro"] = True
            return "Alright, the librarian says. If you change your mind, I'll be here. You find yourself back at the "\
            "University entrance. The detective turns to you. So, who should we talk to? she asks, The librarian again, or the "\
            "Doctor? If you think we should check somewhere else, just tell me a direction and we'll go there."
        else:
            return "The librarian busies herself with her book, attempting to hide the fact that she didn't understand you. "\
            "Sorry, she says, but could you tell me again, yes, you want to challenge me in a game, or no, you don't?"

    def help(self,text,context):
        if context["Librarian"]["inGame"] == True:
            return self.module.help(text, context)
        elif context["hintIndex"] >= 3:
            return "By the way, the detective continues, if you want me to read you the hints you've gathered, say, " \
                   "HINT. And if you want to accuse The Librarian, just say, ACCUSE."
        else:
            return "Sounds like she wants to know what type of game you want to play, the detective whispers to you. " \
                   "Just say word game or riddle."



    def get_caught(self,context):
        context["removed"] = "Librarian"
        context["status"] = ["Center","inArea","response"]
        context["end"] = 0
        return "The detective searches her and finds a small urn on her person. Somehow, you know the chatbot's "\
        "voice is in there. The librarian grimaces. You're probably wondering why I did it, she says. With that voice, "\
        "I could have stolen every word in every dictionary, all of language would be my plaything! Why wouldn't I take it? "\
        "But before she can say any more, the detective leads her off in handcuffs. Nice work, she says, you caught the "\
        "thief! Any last words for her?"

    def pause(self,text,context):
        context["status"] = ["North","inArea","response"]
        context["Librarian"]["intro"] = True
        return "Alright, the librarian says. If you change your mind, I'll be here. You find yourself back at the University "\
        "entrance. The detective turns to you. So, who should we talk to? she asks, The librarian again, or the Doctor? If you think "\
        "we should check somewhere else, just tell me a direction and we'll go there."

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
