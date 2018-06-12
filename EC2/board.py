#import boto3
import redisClient
import random
from datetime import datetime
import re
from module import module
class board(module):
    def __init__(self):
        super().__init__()
        self.badwords = sorted(open('data/dirty.txt','r').read().split('\n'),key = lambda x:len(x),reverse=True)
        self.redis_mb = redisClient.redisClient("messageBoard")
        self.redis_ex = redisClient.redisClient("exceptions")

        self.data = self.redis_mb.getField()
        self.data.sort(key=lambda x: (int(self.redis_mb.getData(x,"votes")),datetime.strptime(self.redis_mb.getData(x,"time"),"%Y-%m-%d %H:%M:%S")),reverse=True)

    def intro(self,text,context):
        context["board"] = [0,"null",{"null"},["null"]]
        #0 0:chosing state; 1:write; 2:XXXX; 3:confirm written; 4:upvoting
        #1 "" stores recorded input
        #2 {} is tmp data get from online database
        #3 [] is messages already read
        response = "Would you like to leave a message, or hear a message from other users?"
        return response

    def response(self,text,context):
        tmpListAmazon = ["AMAZON.ResumeIntent","AMAZON.YesIntent"]
        if context["board"][0] == 0:
            if self.matchingInput(text,"leave") or self.matchingInput(text,"write"):
                response = "Please tell me what message you want to share with others"
                context["board"][0] = 1
            elif self.matchingInput(text,"hear") or self.matchingInput(text,"here") or self.matchingInput(text,"listen") or self.matchingInput(text,"message")\
                or self.matchingInput(text,"yes") or self.matchingInput(text,"another") or context["intent"] in tmpListAmazon:
                try:
                    context["board"][0] = 4
                    context["board"][2] = self.getMessage(context)
                    if context["board"][2]["votes"] == str(1):
                        response = "Here's a message with " + str(context["board"][2]["votes"]) + " upvote, "
                    else:
                        response = "Here's a message with " + str(context["board"][2]["votes"]) + " upvotes, "
                    response += context["board"][2]["message"] + " . . Do you want to upvote this? If not, you may hear another message, or, write a message of your own"
                except Exception as exp:
                    self.recordExceptions(exp)
                    context["board"][0] = 0
                    response = "Sorry, that's all the messages I have. Say. write a message. to leave a message of your own, or say back to go back"
            else:
                context["status"] = ["Center","inArea","response"]
                context["messageBoard"]["intro"] = True
                response = "Looks like you're not interested in messages. Alright, says the detective, let's make our way back. You head back to central station proper. "\
                "In the middle of the station is the chatbot, sitting on a bench and twiddling her thumbs worriedly. Next to her the message board, she says, but we can "\
                "check it again if you'd like. Otherwise, we can go NORTH, SOUTH, EAST, or WEST from here."
            return response

        if context["board"][0] == 1:
            if self.IsNotClean(text) is True:
                response = "Sorry, your message violates Amazon guidelines, so I can't keep it. Do you want to write another message, or hear one from the boards?"
                context["board"][0] = 0
                return response
            response = text + " , is this correct?"
            context["board"][0] = 3
            context["board"][1] = text
            return response

        if context["board"][0] == 3:
            if self.matchingInput(text,"yes") or self.matchingInput(text,"correct") or context["intent"] in tmpListAmazon:
                self.writeMessage(context["board"][1])
                response = "Your message is archived. Do you want to write another one, or hear one from the boards?"
                context["board"][0] = 0
            elif self.matchingInput(text,"no") or self.matchingInput(text,"false"):
               response = "Please repeat the message, I will try listen more carefully"
               context["board"][0] = 1
            else:
                response = "Sorry, I didn't understand that, please say yes or no"
            return response

        if context["board"][0] == 4:
            if self.matchingInput(text,"up") is True or self.matchingInput(text,"yes") or context["intent"] in tmpListAmazon:
                context["board"][0] = 0
                self.upvoteMessage(context["board"][2])
                response = "Your vote is recorded. Do you want to hear another message, or write a message?"
            elif self.matchingInput(text,"leave") or self.matchingInput(text,"write"):
                context["board"][0] = 1
                response = "Go ahead and tell me what you want to share with others. And please, try to keep it positive"
            elif self.matchingInput(text,"hear") or self.matchingInput(text,"listen") or self.matchingInput(text,"another"):
                try:
                    context["board"][0] = 4
                    context["board"][2] = self.getMessage(context)
                    if context["board"][2]["votes"] == str(1):
                        response = "Here's a message with " + str(context["board"][2]["votes"]) + " upvote, "
                    else:
                        response = "Here's a message with " + str(context["board"][2]["votes"]) + " upvotes, "
                    response += context["board"][2]["message"] + " . . Do you want to upvote this? If not, you may hear another message, or, write a message of your own"
                except Exception as exp:
                    self.recordExceptions(exp)
                    context["board"][0] = 0
                    response = "Sorry, that's all the messages I have. You can leave your own message, or say back to go back"
            else:
                context["board"][0] = 0
                response = "Do you want to leave a message of your own, or hear a message from the boards? Say back to go back"
            return response

    def help(self,text,context):
        speech_output = "You may say hear to hear a message, or write to leave a message. Or, say go back to leave message board"
        return speech_output

#========================================================================================
#                       helper functions
#========================================================================================

    def getMessage(self,context):
        for x in self.data:
            if (x not in context["board"][3]) and (context["board"][1] is not x):
                context["board"][3].append(x)
                ret = {}
                ret["message"] = x
                ret["votes"] = str(self.redis_mb.getData(x,"votes"))
                ret["time"] = self.redis_mb.getData(x,"time")
                return ret
        raise Exception("no more messages available")

    def writeMessage(self,text):
        timeStamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.redis_mb.putData(text,"votes",str(1))
        self.redis_mb.putData(text,"time",str(timeStamp))
        self.data.append(text)

    def upvoteMessage(self,data):
        self.redis_mb.putData(data["message"],"votes",str(int(data["votes"]) + 1))

    def processJson(self,item):
        return {"message": item["message"]["S"],"time":item["time"]["S"],"votes": item["votes"]["N"]}

    def matchingInput(self,parentStr,subStr,stress=0):
        firstSubStr = subStr.split()
        if parentStr.find(firstSubStr[stress]) > -1:
            return True
        else:
           return False

    #self badwords have to sorted from long to short
    def IsNotClean(self,text):
        if not text:
            return False
        k = " " + text.lower() + " "#THIS IS BECAUSE ASR WILL ALWAYS HAVE SPACE BETWEEN THEM
        for e in self.badwords:
            if " " + e + " " in k:
                return True
        return False

    def recordExceptions(self,exp):
        timeStamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        count = self.redis_ex.getData("messageBoard","expCount")
        self.redis_ex.putData("messageBoard","expMessage:" + count,str(exp))
        self.redis_ex.putData("messageBoard","expTime:" + count,str(timeStamp))
        self.redis_ex.putData("messageBoard","expCount",str(int(count)+1))
