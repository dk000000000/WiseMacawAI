from module import module
class start(module):
    def __init__(self):
        super().__init__()
    def response(self,text,context):
        t = [True if e in text.lower() else False for e in self.testcodes]
        testcode = t.index(True) if True in t else -1
        if testcode>=0:
            context["hold"] = True
            context["flow"]=[testcode,100]
            response = "In test code module, you are testing "+self.testcodes[testcode]+"say back to change other function, "
        else:
            response = " I can tell you about news articles and trending tweets I've heard, answer your questions, hear your horoscope, or show you what's happening on my message board. "
            response += " If we're in the middle of something, say back at any time to do something else. "
            response += " And if you're curious about what else I can do, just say, help. "
            context["flow"][1]+=1
        return response
    def intro(self,text,context):
        response = "Hi! This is an Alexa Prize socialbot. "
        #response += ""
        response += " I can tell you about news articles and trending tweets I've heard, answer your questions, hear your horoscope, or show you what's happening on my message board. "
        response += " If we're in the middle of something, say back at any time to do something else. "
        response += " And if you're curious about what else I can do, just say, help. "
        return response
