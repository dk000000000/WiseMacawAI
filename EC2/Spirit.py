import textAdventure
import ghostAdventure
from nltk.util import ngrams

class Spirit:
    def __init__(self):
        self.yeswords = open('data/yes.txt','r').read().split('\n')
        self.nowords = open('data/no.txt','r').read().split('\n')
        self.textAdventure = textAdventure.textAdventure()
        self.ghostAdventure = ghostAdventure.ghostAdventure()
        self.module = self.textAdventure

    def intro(self,text,context):
        context["Spirit"] = {}
        context["Spirit"]["stage"] = 0
        context["Spirit"]["inGame"] = False
        context["Spirit"]["intro"] = False
        return "You find yourself outside an abandoned house. The shimmering form "\
        "of an old man with thin grey hair appears before you. I am the spirit, "\
        "he says. You seek the one that stole the chatbot's voice, yes? Enter the "\
        "house and survive until morning, and I shall tell you what I have learned. "\
        "Have you the courage? Yes, or no?"

    #context["Spirit"]["stage"]
    #0:never visited 1:return to spirit 2:survived night 3: caught intruder
    #context["Spirit"]["inGame"]: T/F
    def response(self, text, context):
        if context["Spirit"]["intro"] == True:
            context["Spirit"]["intro"] = False
            if context["Spirit"]["stage"] == 0 or context["Spirit"]["stage"] == 1:
                return "You find yourself outside the Spirit's abandoned house. You have "\
                "returned, the Spirit says, calling out to you on the wind. Enter the house "\
                "and survive until morning, and I shall tell you what I have learned. He says. "\
                "Have you the courage? Yes, or no?"
            elif context["Spirit"]["stage"] == 2:
                return "You find yourself outside the Spirit's abandoned house. You have "\
                "survived my house, the Spirit says, but can you defend it as I have? Enter "\
                "the house and find the intruder, and I shall share with you more of my knowledge. "\
                "Have you the courage? Yes, or no?"
            else:#context["Spirit"]["stage"] == 3
                return "You find yourself outside the Spirit's abandoned house. You have "\
                "returned, the Spirit says, Yet I have no more knowledge to share with you. "\
                "Do you seek to test yourself in the house once more? Yes, or no?"

        if context["Spirit"]["inGame"] == True:
            response,stage = self.module.response(text,context)
            if stage == 1:#death
                context["Spirit"]["inGame"] = False
                #context["status"] = ["West","inArea","response"]
                response += " Your eyes snap open, and you find yourself outside the house. You "\
                "hear the spirit's voice on the wind. You have failed this night, it says, but it "\
                "is not your last. Do you wish to spend another night? Yes, or no?"
            elif stage == 2 or text == "yes fk me":#survived
                context["Spirit"]["stage"] = 2
                context["Spirit"]["inGame"] = False
                if context["hintIndex"] >= len(context["hints"]):
                    response = "Turns out, a chatbot's voice is pretty powerful. I don't really understand it all, but it really shouldn't be tampered with."
                else:
                    context["status"] = ["Center","inArea","response"]
                    context["hintIndex"] += 1
                    hintStr = context["hints"][context["hintIndex"]]
                    context["Spirit"]["intro"] = True
                    response += " You finally emerge outside the house. The spirit wails and appears "\
                    "before you. You have survived, he says, and so my knowledge is yours. Though I "\
                    "have more to share if you return. " + hintStr + " . The detective quickly "\
                    "jots it down, then hurries you back to Central Station. You dealt with that "\
                    "specter well, she says. Where should we go next? Northern University, the Eastern "\
                    "Commons, Southern Square, or the Western Woods?"
                return response
            elif stage == 3:#failed to catch intruder
                #context["Spirit"]["stage"] = 2
                context["Spirit"]["inGame"] = False
                #context["status"] = ["West","inArea","response"]
                response += " Your eyes snap open, and you find yourself outside the house. You "\
                "hear the spirit's voice on the wind. You have failed this night, it says, but it "\
                "is not your last. Do you wish to spend another night? Yes, or no?"
            elif stage == 4:#caught the intruder
                context["Spirit"]["stage"] = 3
                context["Spirit"]["inGame"] = False
                if context["hintIndex"] >= len(context["hints"]):
                    response = "Turns out, a chatbot's voice is pretty powerful. I don't really understand it all, but it really shouldn't be tampered with."
                else:
                    context["status"] = ["Center","inArea","response"]
                    context["hintIndex"] += 1
                    hintStr = context["hints"][context["hintIndex"]]
                    context["Spirit"]["intro"] = True
                    response += " You drift your way outside the house, returning to your human form. "\
                    "The spirit wails and appears before you, a translucent, shimmering specter. You "\
                    "have found the intruder, it says, and so the rest of my knowledge is yours. "\
                    + hintStr + " . The detective quickly jots it down, then hurries you back "\
                    "to Central Station. Well done again, she says. Where should we go next? Northern "\
                    "University, the Eastern Commons, Southern Square, or the Western Woods?"
                return response
            elif stage == 5:#tutorial
                context["Spirit"]["inGame"] = False
                response += " Your eyes snap open, and you find yourself outside the house. You "\
                "hear the spirit's voice on the wind. You have tryed this morning, it says, but the "\
                "real part is at night. Do you wish to spend another night? Yes, or no?"
            else:#stage == 0 normal in game
                pass
            return response
             
        if self.yes_representation(text,context):
            if context["Spirit"]["stage"] == 0:
                context["Spirit"]["stage"] = 1
                context["Spirit"]["inGame"] = True
                self.textAdventure.intro("",context)
                self.module = self.textAdventure
                return "The spirit wails on the winds, and you somehow appear inside the house. "\
                "A shallow sound comes from far away . Do you want to survey the area ? Or skip to night time"
            elif context["Spirit"]["stage"] == 1:
                context["Spirit"]["inGame"] = True
                self.textAdventure.intro("",context)
                self.module = self.textAdventure
                return "The spirit wails on the winds, and you somehow appear inside the house. "\
                "A shallow sound comes from far away . Do you want to survey the area ? Or skip to night time"
            elif context["Spirit"]["stage"] == 2:
                context["Spirit"]["inGame"] = True
                self.ghostAdventure.intro("",context)
                self.module = self.ghostAdventure
                return "The spirit wails on the winds, and you somehow appear inside the house "\
                "as a dark, shadowy spectre. You wake up by the noise somewhere , you may "\
                "say hide to find available hiding spots able to be checked , or say door , "\
                "to find out which door leads to which room . You don't know what is behind each door"
            else:#context["Spirit"]["stage"] == 3
                context["Spirit"]["inGame"] = True
                self.textAdventure.intro("",context)
                self.module = self.textAdventure
                return "The spirit wails on the winds, and you somehow appear inside the house. "\
                "A shallow sound comes from far away . Do you want to survey the area ? Or skip to night time"
        elif self.no_representation(text,context):
            context["status"] = ["West","inArea","response"]
            context["Spirit"]["intro"] = True
            return "Return when you wish to try again, says the spirit, before its voice fades into the darkness "\
            "around you. You find yourself back at the edge of the western woods. The detective turns to you. So, "\
            "who should we talk to? she asks, The Fortune Teller, or The Spirit again? If you think we should check "\
            "somewhere else, just tell me a direction and we'll go there."
        else:
            return "The spirit moans in confusion. Do you wish to test your courage in my house? he asks. Yes, or no?"

    def help(self,text,context):
        if context["Spirit"]["inGame"] == True:
            return self.module.help(text,context)
        else:
            help_text = "Well, I'm not too well versed on ghosts, the detective whispers, But the spirit just "\
            "invited you to brave his house. I think he just wants you to say yes or no."
        if context["hintIndex"] >= 2:
            help_text += "By the way, the detective continues, if you want me to read you the hints you've gathered, "\
            "say, HINT. And if you want to accuse The Spirit, just say, ACCUSE."
        return help_text

    def get_caught(self,context):
        context["removed"] = "Spirit"
        context["status"] = ["Center","inArea","response"]
        context["end"] = 0
        return "The detective passes a hand through the spirit, and a small urn emerges in her hand. Somehow, "\
        "you know the chatbot's voice is in there. The spirit wails loudly. You don't even know why I took it, do you?"\
        " he asks. With that voice, I could have forced anyone out of their body to replace them. I could have finally "\
        "come back to life! The detective points a vacuum menacingly at the spirit and leads it away. Nice work, she "\
        "says, you caught the thief! Any last words for him?"

    def pause(self,text,context):
        context["status"] = ["West","inArea","response"]
        context["Spirit"]["intro"] = True
        return "Return when you wish to try again, says the spirit, before its voice fades into the "\
        "darkness around you. You find yourself back at the edge of the western woods. The detective turns "\
        "to you. So, who should we talk to? she asks, The Fortune Teller, or The Spirit again? If you think we "\
        "should check somewhere else, just tell me a direction and we'll go there."

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
