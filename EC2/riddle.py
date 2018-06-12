from module import module
import csv
import random
class riddle(module):
    def __init__(self):
        super().__init__()
        self.riddlelist = [e for e in csv.reader(open("data/riddle.csv", encoding="utf8"), delimiter='|')]


    def help(self, text, context):
        nextlist = ["Let's try a new one.",
                    "I've got another one.",
                    "",
                    "",
                    "",
                    ""]

        response = ""
        response += "Ok, the answer is . " + self.getanswer(context["riddle"]) + " . "
        response += nextlist[random.randint(0, len(nextlist) - 1)]
        response += self.getriddle(context["riddle"])
        context["riddle"]["chance"] = 1
        context["riddle"]["status"] = 1
        

        return response, 0


    def response(self, text, context):
        response = ""

        tryagainlist = ["Try again.",
                        "Think again.",
                        "Try another one."]

        nextlist = ["Let's try a new one . ",
                    "I've got another one . ",
                    ""]


        if context["riddle"]["try"]>=8:
            context["status"] = ["Center", "inArea", "response"]
            return "", 2


        if context["riddle"]["correct"]>=2:
            context["status"] = ["Center", "inArea", "response"]
            return "", 1



        if context["riddle"]["status"]==0:
            response += self.getriddle(context["riddle"])
            context["riddle"]["status"]=1
            


        elif context["riddle"]["status"]==1:
            userwordlist = text.lower().split()

            TorF = False

            #current_id = riddle["past_id"][len(past_ids)-1]
            for userword in userwordlist:

                if userword=="why" or userword=="what" or userword=="help" or userword=="don't":
                    return self.help(text, context)


                temp_id = context["riddle"]["current_id"]
                for answerlist in self.riddlelist[temp_id][2:]:
                    if userword == answerlist:
                        TorF = True
            if TorF==True:
                responselist = ["That's the right answer!",
                                "Right! ",
                                "True, is this too easy?",
                                "correct! "]
                responseID = random.randint(0,len(responselist)-1)
                response += responselist[responseID]
                response += " . "
                response += nextlist[random.randint(0,len(nextlist)-1)]
                response += self.getriddle(context["riddle"])
                context["riddle"]["correct"] += 1
                context["riddle"]["chance"] = 1
                context["riddle"]["status"]=1
                
            else:
                if context["riddle"]["chance"] > 0:
                    context["riddle"]["chance"] -= 1
                    response = tryagainlist[random.randint(0,len(tryagainlist)-1)]
                    context["riddle"]["status"]=1
                    
                else:
                    response += "Ok, the answer is . "+self.getanswer(context["riddle"])+" . "
                    response += nextlist[random.randint(0,len(nextlist)-1)]
                    response += self.getriddle(context["riddle"])
                    context["riddle"]["chance"] = 1
                    context["riddle"]["status"]=1
                    


        return response, 0




    def intro(self, text, context):
        response = ""
        context["riddle"] = {}
        context["riddle"]["status"] = 1
        context["riddle"]["current_id"] = -1
        context["riddle"]["chance"] = 1
        context["riddle"]["past_id"] = []
        context["riddle"]["try"] = 0
        context["riddle"]["correct"] = 0
        

        response += " Answers will be just one word. If you are stuck, say help, and if you want to do something else, say back . "
        response += self.getriddle(context["riddle"])

        return response



    def getriddle(self, riddle):
        past_ids = riddle["past_id"]
        riddlelist = self.riddlelist
        index = random.choice([i for i in range(len(riddlelist)) if i not in past_ids])
        past_ids.append(index)
        riddle["current_id"] = index
        riddle["try"]+=1
        return riddlelist[index][1]



    def getanswer(self, riddle):
        past_ids = riddle["past_id"]
        current_id = past_ids[len(past_ids)-1]
        riddlelist = self.riddlelist
        tempResponse = riddlelist[current_id][2]
        tempResponse += " . "+riddlelist[current_id][0]
        return tempResponse
