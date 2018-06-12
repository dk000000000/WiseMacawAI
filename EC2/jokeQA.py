from module import module
import csv
import random
class jokeQA(module):
    def __init__(self):
        #make sure joke readin with no empty line
        super().__init__()
        self.jokelist = [e for e in csv.reader(open("data/jokeqa.csv",'r'), delimiter='|')]

    def response(self,text,context):
        if "joke_qa" not in context:
            context["joke_qa"]={}
            context["joke_qa"]["status"]=0
            context["joke_qa"]["past_id"]=[]

        responce = ""
        if context["joke_qa"]["status"]==0:
            responce = self.getquestion(context["joke_qa"])
            context["joke_qa"]["status"]=1
        else:
            responce = self.getanswer(context["joke_qa"])
            context["joke_qa"]["status"]=0
        return responce

    def getquestion(self,joke_qa):
        past_ids = joke_qa["past_id"]
        jokelist = self.jokelist
        index = random.choice([i for i in range(len(jokelist)) if i not in past_ids])
        past_ids.append(index)
        return jokelist[index][1]

    def getanswer(self,joke_qa):
        past_ids = joke_qa["past_id"]
        current_id = past_ids[len(past_ids)-1]
        jokelist = self.jokelist
        return jokelist[current_id][2]
