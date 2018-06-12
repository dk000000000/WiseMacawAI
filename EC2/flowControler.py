import numpy
class flowControler:
    def __init__(self):
        self.moduleNames = ["word game",
                            "reddit news",
                            "twitter news",
                            "twitter trend",
                          "ask question",
                          "joke",
                          "chitchat",
                          "chat",
                          "text adventure",
                          "ghost adventure",
                          "horoscope",
                          "riddle game",
                          "message board",
                          "search",
                          "startModule",
                          ]
        self.turns = [ 8,10,10, 10, 1, 2,2,2,10,10, 6,10,5,1,1]
        self.count = [10,20,20,20, 0,20,0,0,20,20,20,20,10,0,0]

    def AssignFlow(self,context,response):
        context["flow"][1]-=1
        if context["hold"] and context["flow"][1]==0:
            context["flow"][1]+=1

        if context["flow"][1]<=0:
            context["hold"]=False
            k = list(self.count)
            k[context["flow"][0]]=0
            notAssign = ["ask question", "chitchat","chat","search"]
            for i in notAssign:
                k[self.moduleNames.index(i)]=0
            context["flow"][0]=int(numpy.random.choice(len(self.moduleNames), 1, p=[float(e)/sum(k) for e in k]))
            context["flow"][1]=self.turns[context["flow"][0]]
            context["randomAssign"]=True
        return response

    def flowChange(self,Request,context,user_input):
        flag = False
        response = ""

        if "intent" in Request and Request["intent"]["name"]=="AMAZON.PauseIntent":
            context["pause"]=True
        elif "intent" in Request and Request["intent"]["name"]=="AMAZON.HelpIntent":
            context["help"]=True
        elif "intent" in Request and Request["intent"]["name"]=="AMAZON.RepeatIntent":
            context["repeat"]=True
        elif "intent" in Request and Request["intent"]["name"]=="ID":
            flag = True
            response = "Sorry, Amazon does not allow me to talk about that."
        elif "intent" in Request and Request["intent"]["name"]=="AmazonCommand":
            flag = True
            response = "Sorry, I'm not capable doing that. I'm just a social bot, not Alexa."
        if context["hold"] == False or context["randomAssign"]:
            context["randomAssign"]=False
            # Only change to other module based on intent if current module is not requesting a hold
            if "intent" in Request and Request["intent"]["name"]=="text adventure":
                flow_changed = True
                self.changeflow("text adventure",context)
            elif "intent" in Request and Request["intent"]["name"]=="twitter trend":
                flow_changed = True
                self.changeflow("twitter trend",context)
            elif "intent" in Request and Request["intent"]["name"]=="message board":
                flow_changed = True
                self.changeflow("message board",context)
            elif "intent" in Request and Request["intent"]["name"]=="word game":
                flow_changed = True
                self.changeflow("word game",context)
            elif "intent" in Request and Request["intent"]["name"]=="riddle game":
                flow_changed = True
                self.changeflow("riddle game",context)
            elif "intent" in Request and Request["intent"]["name"]=="horoscope":
                flow_changed = True
                self.changeflow("horoscope",context)
            elif "intent" in Request and Request["intent"]["name"]=="Joke":
                flow_changed = True
                self.changeflow("joke",context)
            elif "intent" in Request and (Request["intent"]["name"]=="reddit news" or Request["intent"]["name"]=="Interest"):
                #flow_changed = True
                self.changeflow("reddit news",context)
            elif "intent" in Request and Request["intent"]["name"]=="Assertive" and len(user_input.split())>2:
                if "ask" in user_input or "ask question" in user_input:
                    flow_changed = True
                    context["help"]=True
                flow_changed = True
                self.changeflow("ask question",context)
            elif "intent" in Request and (Request["intent"]["name"]=="SmallTalk"):
                flow_changed = True
                self.changeflow("chat",context)
        return response,flag

    def changeflow(self,moduleName,context,turn = None):
        context["flow"]=[self.moduleNames.index(moduleName),self.turns[self.moduleNames.index(moduleName)] if not turn else turn]

    # Chooses a module to suggest to the user.
    # Obeys probabilities as in AssignFlow.
    # Returns the text for the suggestion.
    def MakeSuggestion(self, context):
        k = list(self.moduleNames)
        # Don't choose whatever module we just came from.
        k[context["flow"][0]]=0
        # Don't choose any of the modules that can't be randomly assigned in AssignFlow
        notAssign = ["word game", "ask question","chitchat","chat","search"]
        for i in notAssign:
            k[self.moduleNames.index(i)]=0
        # Choose a module code from amongst the viable modules.
        random_code = int(numpy.random.choice(len(self.moduleNames), 1, p=[float(e)/sum(k) for e in k]))

        # Use different text for each suggestion
        suggestion_text = " . Hey, wanna do something interesting? "
        if random_code == self.moduleNames.index("word game"):
            suggestion_text += " Try saying, let's play a word game. "
        elif random_code == self.moduleNames.index("news"):
            suggestion_text += " Try saying, let's hear some news. "
        elif random_code == self.moduleNames.index("joke"):
            suggestion_text += " Try saying, tell me a joke. "
        elif random_code == self.moduleNames.index("text adventure"):
            suggestion_text += " Try saying, let's have an text adventure. "
        elif random_code == self.moduleNames.index("twitter trend"):
            suggestion_text += " Try saying, let's hear some tweets. "
        elif random_code == self.moduleNames.index("message board"):
            suggestion_text += " Try saying, let's listen to the message boards. "
        else:
            # By default, suggest news.
            suggestion_text += " Try saying, tell me some news. "
        return suggestion_text
