import random


class DetectiveGame:
    def __init__(self):
        super().__init__()

        self.npclist = ["Spirit","Fortune Teller","Moderator","Trendsetter","Drunkard","Bartender","Doctor","Librarian"]

        self.npckeyword = [["spirit","soul","phantasm","vision","phantom","shade","sprite","wraith"],
                           ["fortune","teller","augur","clairvoyant","crystal","seer","medium","oracle","psychic","tarot"],
                           ["reddit","moderator","commentor"],
                           ["trendsetter","stylist"],
                           ["drunkard","alcoholic","boozer","drinker","alcohol"],
                           ["bartender","barkeep","barkeeper","tapster","barmaid","bar","tapper"],
                           ["p h d","doctor","fellow","teacher","assistant","lecturer","instructor"],
                           ["librarian","curator","cataloger","bibliognost","bibliosoph","bibliothecary"]]

        self.npcgender = ["man","woman","man","woman","man","woman","man","woman"]

        self.npclocation = ["western woods","western woods","southern square","southern square",
                            "eastern commons","eastern commons","northern university","northern university"]

        self.locations = ["western woods","southern square","eastern commons","northern university"]

        self.hints = {}


    def getthief(self):
        thief,hintlist = self.puzzle()
        return thief


    def getpuzzle(self):
        thief, hintlist = self.puzzle()
        return hintlist


    def puzzle(self,context):
        if any(self.hints):
            return self.hints["thief"], self.gethint()

        else:
            id = random.randint(0, 7)
            self.hints["thief"] = self.npclist[id]
            self.hints["thiefid"] = id
            self.hints["thieflocation"] = self.npclocation[id]
            self.hints["locationunused"] = [0,1,2,3]
            self.hints["locationunused"].pop(int(id/2))
            self.hints["gender"] = self.npcgender[id]
            self.hints["hintlist"] = []

            return self.hints["thief"], self.gethint()


    def getstronghint(self):
        responselist = []

        tmplist = []
        for npc in self.npclist:
            if npc != self.hints["thief"]:
                tmplist.append(npc)

        notguilty = random.randint(0,6)
        responselist.append(tmplist[notguilty]+" is definitely not the thief. ")
        tmplist.pop(notguilty)
        notguilty = random.randint(0,5)
        responselist.append("We are certain that "+tmplist[notguilty]+" is not the perpetrator")
        tmplist.pop(notguilty)
        notguilty = random.randint(0,4)
        responselist.append("No need to worry about "+tmplist[notguilty])
        tmplist.pop(notguilty)

        stronghint1 = "The thief is definitely in "+self.hints["thieflocation"]+". "
        stronghint2 = "The thief is a "+self.hints["gender"]+". "
        responselist.append(stronghint2)
        responselist.append(stronghint1)
        return responselist



    def getweakhint(self):
        responselist = []
        response1 = ["nothing happened in ",
                     "the thief should not be in ",
                     "people in "]
        response2 = [" last night. ",
                     " for sure. ",
                     " said they didn't see the perpetrator"]

        for index in range(0, 3):
            size = len(self.hints["locationunused"])
            loc = random.randint(0, size - 1)
            response = response1[index] + self.locations[loc] + response2[index]
            responselist.append(response)
            self.hints["locationunused"].pop(loc)

        return responselist



    def gethint(self):
        hintlist = []
        weaklist = self.getweakhint()
        stronglist = self.getstronghint()
        for hint in weaklist:
            hintlist.append(hint)
        for hint in stronglist:
            hintlist.append(hint)

        return hintlist



    def reset(self):
        id = random.randint(0, 7)
        self.hints["thief"] = self.npclist[id]
        self.hints["thiefid"] = id
        self.hints["thieflocation"] = self.npclocation[id]
        self.hints["locationunused"] = [0, 1, 2, 3]
        self.hints["locationunused"].pop(int(id / 2))
        self.hints["gender"] = self.npcgender[id]
        self.hints["hintlist"] = []
