from module import module
import csv
from nltk.util import ngrams
import random
from datetime import datetime


class horoscope(module):
    def __init__(self):
        super().__init__()
        self.horoscopelist = [e for e in csv.reader(open("data/horoscope2016.csv"), delimiter='|')]
        self.yeswords = open('data/yes.txt', 'r').read().split('\n')[:-1]
        self.nowords = open('data/no.txt', 'r').read().split('\n')[:-1]


    def response(self, text, context):
        response = ""

        #print(self.horoscopelist[1])

        if context["horoscope"]["status"]==0:
            signlist = ["aries","taurus","gemini","cancer","leo","virgo","libra","scorpio","sagittarius","capricorn",
                        "aquarius","pisces"]
            userwordlist = text.lower().split()
            TorF = False
            for userword in userwordlist:
                if TorF == True:
                    break
                for tempsign in signlist:
                    if tempsign == userword:
                        TorF = True
                        context["horoscope"]["sign"] = tempsign
                        break

            if TorF == True:
                response = "Your sign is " + context["horoscope"]["sign"] + ", is that correct?"
                context["horoscope"]["status"] = 1
                return response, False

            else:
                if context["horoscope"]["signtry"]>0:
                    context["horoscope"]["signtry"] -= 1
                    response = "Sorry, could you say that again? "
                    context["horoscope"]["status"] = 0
                else:
                    response = "I'm not sure. If you want to do something else, say back. If not, lets find out your sign. I need to know when were you born. Could you tell me which month were you born in? "
                    context["horoscope"]["status"] = 3


        elif context["horoscope"]["status"]==1:
            userwordlist = text.lower().split()
            rightExist = False
            for userword in userwordlist:
                if userword == "right":
                    rightExist = True

            if (self.yes_representation(text, context) or rightExist):
                signlist = ["aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", "scorpio", "sagittarius",
                            "capricorn", "aquarius", "pisces"]

                for index in range (0, 12):
                    if signlist[index] == context["horoscope"]["sign"]:
                        context["horoscope"]["sign"] = str(index+1)

                for templine in self.horoscopelist:
                    now = datetime.now()
                    if (templine[0]=="2016" and templine[1]==str(now.month) and templine[2]==str(now.day) and templine[3]==context["horoscope"]["sign"]):
                        response = templine[4]
                        context["horoscope"]["text"] = response
                        context["horoscope"]["matches"].append(templine[5])
                        context["horoscope"]["matches"].append(templine[6])
                        context["horoscope"]["matches"].append(templine[7])
                        context["horoscope"]["ratings"].append(templine[8])
                        context["horoscope"]["ratings"].append(templine[9])
                        context["horoscope"]["ratings"].append(templine[10])
                        context["horoscope"]["ratings"].append(templine[11])
                        break

                response += " . Would you like to know your matches, star ratings or both? If you don't want to hear these, just say back."
                context["horoscope"]["status"] = 2
                return response, False

            elif (self.no_representation(text,context)):
                if context["horoscope"]["signtry"]>0:
                    response = "Could you tell me your sign again? Or say help and lets find out your sign"
                    context["horoscope"]["signtry"] -= 1
                    context["horoscope"]["status"] = 1
                else:
                    context["horoscope"]["status"] = 3
                    response = "Let's find out your sign, tell me which month were you born in? "

            else:
                context["horoscope"]["status"] = 3
                response = "If you are not interested in horoscope, say back. If you don't know your sign, I can find out your sign, just tell me in which month were you born . "

        elif context["horoscope"]["status"]==2:
            userwordlist = text.lower().split()
            matchesword = ["matches","match","mattress"]
            ratingsword = ["ratings","rating","star","stars"]
            bothword = ["both","all","everything","sure","ok","yes"]
            TorF = False
            for userword in userwordlist:
                if userword in bothword or self.yes_representation(text, context):
                    response = self.getBoth(text, context)
                    TorF = True
                    break

                elif userword in matchesword:
                    response = self.getMatches(text, context)
                    TorF = True
                    break

                elif userword in ratingsword:
                    response = self.getMatches(text, context)
                    TorF = True
                    break

            if TorF == False:
                context["status"] = ["Center", "inArea", "response"]
                return "I see, she says, a bit disappointed. If you change your mind, I'll still be here. With that, you take " \
                       "your leave. You find yourself back at the edge of the western woods. The detective turns to you. So, " \
                       "who should we talk to? she asks, The Fortune Teller, or The Spirit? If you think we should check " \
                       "somewhere else, just tell me a direction and we'll go there.", False

            else:
                context["status"] = ["Center", "inArea", "response"]
                return response, True


        elif context["horoscope"]["status"]==3:
            monthlist = ["january", "february", "march", "april", "may", "june", "july", "august", "september",
                         "october",
                         "november", "december"]
            userwordlist = text.lower().split()
            TorF = False
            for userword in userwordlist:
                if userword in monthlist:
                    for index in range(0, 12):
                        if userword == monthlist[index]:
                            context["horoscope"]["month"] = monthlist[index]
                            context["horoscope"]["monthint"] = index+1
                            break

                    TorF = True
                    break
            response = "and which day in this month were you born? "
            context["horoscope"]["status"] = 4


            if TorF == False:
                if context["horoscope"]["monthtry"] > 0:
                    response = "What's that? Can you tell me the month you were born again? "
                    context["horoscope"]["monthtry"] -= 1
                    context["horoscope"]["status"] = 3
                else:
                    response = "and which day in this month were you born? "
                    context["horoscope"]["month"] = monthlist[random.randint(0, 11)]
                    context["horoscope"]["status"] = 4


        elif context["horoscope"]["status"]==4:
            daylist = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th",
                       "11th", "12th", "13th", "14th", "15th", "16th", "17th", "18th", "19th", "20th",
                       "21st", "22nd", "23rd", "24th", "25th", "26th", "27th", "28th", "29th", "30th", "31st"]

            daylist2 = ["first","second","third","fourth","fifth","sixth","seventh","eighth","ninth","tenth",
                        "eleventh","twelfth","thirteenth","fourteenth","fifteenth","sixteenth","seventeenth",
                        "eighteenth","nineteenth","twentieth","twenty-first","twenty-second","twenty-third",
                        "twenty-fourth","twenty-fifth","twenty-sixth","twenty-seventh","twenty-eighth",
                        "twenty-ninth","thirtieth","thirty-first"]

            daylist3 = ["1","2","3","4","5","6","7","8","9","10",
                        "11","12","13","14","15","16","17","18","19","20",
                        "21","22","23","24","25","26","27","28","29","30","31"]

            daylist4 = ["one","two","three","four","five","six","seven","eight","nine","ten",
                        "eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen","twenty",
                        "twenty-one","twenty-two","twenty-three","twenty-four","twenty-five","twenty-six ","twenty-seven",
                        "twenty-eight","twenty-nine","thirty","thirty-one"]

            userwordlist = text.lower().split()
            TorF = False
            for userword in userwordlist:
                if TorF == True:
                    break
                if userword in daylist:
                    for index in range(0, 31):
                        if userword == daylist[index]:
                            context["horoscope"]["day"] = daylist[index]
                            context["horoscope"]["dayint"] = index + 1
                            TorF = True
                            break

                if userword in daylist2:
                    for index in range(0, 31):
                        if userword == daylist2[index]:
                            context["horoscope"]["day"] = daylist[index]
                            context["horoscope"]["dayint"] = index + 1
                            TorF = True
                            break

                if userword in daylist3:
                    for index in range(0, 31):
                        if userword == daylist3[index]:
                            context["horoscope"]["day"] = daylist[index]
                            context["horoscope"]["dayint"] = index + 1
                            TorF = True
                            break

                if userword in daylist4:
                    for index in range(0, 31):
                        if userword == daylist4[index]:
                            context["horoscope"]["day"] = daylist[index]
                            context["horoscope"]["dayint"] = index + 1
                            TorF = True
                            break


            if TorF == False:
                if context["horoscope"]["daytry"]>0:
                    context["horoscope"]["status"] = 4
                    context["horoscope"]["daytry"] -= 1
                    return "I'm not sure what you said, please tell me your a date between first and thirty-first", False
                else:
                    context["horoscope"]["day"] = daylist2[0]
                    context["horoscope"]["dayint"] = 1
                    context["horoscope"]["random"] = True


            month = context["horoscope"]["month"]
            day = context["horoscope"]["dayint"]

            if month == "january":
                if day >= 20 and day <= 31:
                    context["horoscope"]["sign"] = "aquarius"
                else:
                    context["horoscope"]["sign"] = "capricorn"

            elif month == "february":
                if day >=18 and day <= 31:
                    context["horoscope"]["sign"] = "pisces"
                else:
                    context["horoscope"]["sign"] = "aquarius"

            elif month == "march":
                if day >= 21 and day <= 31:
                    context["horoscope"]["sign"] = "aries"
                else:
                    context["horoscope"]["sign"] = "pisces"

            elif month == "april":
                if day >= 20 and day <= 31:
                    context["horoscope"]["sign"] = "taurus"
                else:
                    context["horoscope"]["sign"] = "aries"

            elif month == "may":
                if day >=21 and day <= 31:
                    context["horoscope"]["sign"] = "gemini"
                else:
                    context["horoscope"]["sign"] = "taurus"

            elif month == "june":
                if day >= 21 and day <= 31:
                    context["horoscope"]["sign"] = "cancer"
                else:
                    context["horoscope"]["sign"] = "gemini"

            elif month == "july":
                if day >= 23 and day <= 31:
                    context["horoscope"]["sign"] = "leo"
                else:
                    context["horoscope"]["sign"] = "cancer"

            elif month == "august":
                if day >= 23 and day <= 31:
                    context["horoscope"]["sign"] = "virgo"
                else:
                    context["horoscope"]["sign"] = "leo"

            elif month == "september":
                if day >= 23 and day <= 31:
                    context["horoscope"]["sign"] = "libra"
                else:
                    context["horoscope"]["sign"] = "virgo"

            elif month == "october":
                if day >= 23 and day <= 31:
                    context["horoscope"]["sign"] = "scorpio"
                else:
                    context["horoscope"]["sign"] = "libra"

            elif month == "november":
                if day >= 22 and day <= 31:
                    context["horoscope"]["sign"] = "sagittarius"
                else:
                    context["horoscope"]["sign"] = "scorpio"

            elif month == "december":
                if day >= 22 and day <= 31:
                    context["horoscope"]["sign"] = "capricorn"
                else:
                    context["horoscope"]["sign"] = "sagittarius"


            response = ""

            if context["horoscope"]["random"] == False:
                response += "If your birthday is on "+context["horoscope"]["month"]+" the "+context["horoscope"]["day"]+\
                           " then your sign should be " + context["horoscope"]["sign"]+", here is your horoscope for today . "

            signlist = ["aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", "scorpio", "sagittarius",
                        "capricorn", "aquarius", "pisces"]

            for index in range(0, 12):
                if signlist[index] == context["horoscope"]["sign"]:
                    context["horoscope"]["sign"] = str(index + 1)

            for templine in self.horoscopelist:
                now = datetime.now()
                if (templine[0] == "2016" and templine[1] == str(now.month) and templine[2] == str(now.day) and
                            templine[3] == context["horoscope"]["sign"]):
                    text = templine[4]
                    response += text
                    context["horoscope"]["text"] = text
                    context["horoscope"]["matches"].append(templine[5])
                    context["horoscope"]["matches"].append(templine[6])
                    context["horoscope"]["matches"].append(templine[7])
                    context["horoscope"]["ratings"].append(templine[8])
                    context["horoscope"]["ratings"].append(templine[9])
                    context["horoscope"]["ratings"].append(templine[10])
                    context["horoscope"]["ratings"].append(templine[11])
                    break

            response += " . Would you like to know your matches, star ratings or both? If you don't want to hear these, say back."

            context["horoscope"]["status"] = 2


        return response, False



    def getMatches(self, text, context):
        matcheslist = context["horoscope"]["matches"]

        text = "For love, "+matcheslist[0]+\
               " . In terms of friendship, you match with "+matcheslist[1]+\
               " . And the match for career today is "+matcheslist[2]+" . "

        return text



    def getRatings(self, text, context):
        ratingslist = context["horoscope"]["ratings"]

        text = "Today's ratings are . "+ratingslist[0]+\
               " for love. "+ratingslist[1]+\
               " for mood. "+ratingslist[2]+\
               " for money and "+ratingslist[3]+\
               " for career . "

        return text



    def getBoth(self, text, context):
        matcheslist = context["horoscope"]["matches"]
        ratingslist = context["horoscope"]["ratings"]

        textM = "For love, " + matcheslist[0] + \
               " . In terms of friendship, you match with " + matcheslist[1] + \
               " . And the match for career today is " + matcheslist[2] + " . "

        textR = "Today's ratings are . " + ratingslist[0] + \
               " for love. " + ratingslist[1] + \
               " for mood. " + ratingslist[2] + \
               " for money and " + ratingslist[3] + \
               " for career . "

        text = textM+"And "+textR

        return text



    def intro(self, text, context):
        response = ""
        context["horoscope"] = {}
        context["horoscope"]["status"] = 0
        context["horoscope"]["random"] = False
        context["horoscope"]["signtry"] = 1
        context["horoscope"]["monthtry"] = 1
        context["horoscope"]["daytry"] = 1
        context["horoscope"]["sign"] = ""
        context["horoscope"]["signint"] = -1
        context["horoscope"]["text"] = ""
        context["horoscope"]["matches"] = list()
        context["horoscope"]["ratings"] = list()
        context["horoscope"]["month"] = ""
        context["horoscope"]["day"] = ""
        context["horoscope"]["dayint"] = -1
        response += " . Tell me what is your sign. If you want to figure out your sign, just say help. Say back to leave . "

        return response



    def help(self, text, context):
        response = ""
        response += "To find out your horoscope sign, I need to know when were you born. Could you tell me which month were you born in?  "
        context["horoscope"]["status"] = 3

        return response



    def yes_representation(self, text, context):
        text = text.lower()
        if (text == "how are you"):
            if (context["intent"] == "AMAZON.YesIntent"):
                return True
            else:
                return False
        if True in [tuple(b.lower().split()) in list(ngrams(text.lower().split(), len(b.lower().split()))) for b in
                    self.yeswords]:
            return True
        return False



    def no_representation(self, text, context):
        text = text.lower()
        if (text == "how are you"):
            if (context["intent"] == "AMAZON.NoIntent"):
                return True
            else:
                return False
        if True in [tuple(b.lower().split()) in list(ngrams(text.lower().split(), len(b.lower().split()))) for b in
                    self.nowords]:
            return True
        return False
