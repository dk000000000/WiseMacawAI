from module import module
import random
class wordGame(module):
    def __init__(self):
        super().__init__()
        self.words = {}
        self.compliments = ["Stunning","Wonderful","Amazing"]
        data = open("data/cmudict-0.7b4","r").read().splitlines()
        for i in range(0, len(data)):
            line = data[i]
            listWords = line.split()
            self.words[listWords[0]] = [listWords[1],listWords[2],listWords[len(listWords) - 1]]

    def intro(self,text,context):
        context["words"] = [[],0,0]#0:for repeated words; 1:consecutive error inputs; 2:valid words
        response = "Let's play a word game . " \
                   "You say a word and I will find one that starts with last letter of your word and try to rhymes with your word . "\
                   "Then you need to find one that starts with the last letter of my word or rhymes with my word . "\
                   "I may not be able to acknowledge every location and name . Say back to quit the game. Okay, you start. Give me a word. "
        return response

    def response(self,text,context):
        speech_output = ""
        words = self.words
        used_words = context["words"][0]
        user_word_list = text.lower().split()
        user_word = user_word_list[len(user_word_list) - 1]
        if len(user_word_list) > 1:
            speech_output += "Please just say one word , "
        try:
            number = int(user_word)
            if number > 20:
                speech_output += "Your word " + user_word + " is invalid , only number between zero to twenty are allowed"
                return speech_output,0
            else:
                numberDict = {1:'one',2:'two',3:'three',4:'four',5:'five',6:'six',7:'seven',8:'eight',9:'nine', \
                    10:'ten',11:'eleven',12:'twelve',13:'thirteen',14:'fourteen',15:'fifteen',16:'sixteen', \
                    17:'seventeen',18:'eighteen',19:'nineteen',20:'twenty'}
                user_word = numberDict[number]
        except ValueError as ex:
            pass#not numbers

        #invalid for nonsense user word
        if user_word not in words:
            context["words"][1] += 1
            if len(used_words) == 0:
                speech_output += "Your word " + user_word + " is invalid. "
            else:
                last_macaw = used_words[len(used_words) - 1]
                speech_output += "Your word " + user_word + " is invalid. "\
                                "Please pick a word that starts with " + last_macaw[len(last_macaw) - 1] + " . "
            if context["words"][1] == 2:
                speech_output += " You may say back to exit game. " + str(5 - context["words"][1]) + " more mistakes are allowed "
            elif context["words"][1] > 2 and context["words"][1] < 5:
                speech_output += str(5 - context["words"][1]) + " more mistakes are allowed"
            elif context["words"][1] == 5:
                speech_output += " You made 5 mistakes."
                return speech_output,2
            return speech_output,0

        #repeated user word
        if user_word in used_words:
            context["words"][1] += 1
            last_macaw = used_words[len(used_words) - 1]
            speech_output += "Your word " + user_word + " is a repeat. "
            return speech_output,2

        if len(used_words) == 0:
                context["words"][0].append(user_word)
                result = self.find_word_start_with(used_words,user_word)
                if result != "not found":
                    context["words"][0].append(result)
                    finalresult = self.spell_word(result)
                    context["words"][2] += 1
                    if context["words"][2] == 10:
                        return "",1
                    elif context["words"][2] % 10 == 0:
                        finalresult = random.choice(self.compliments) + " , you reach level " + str(context["words"][2] // 10) + \
                            " .  . you may say back to try something else . " + finalresult
                    elif context["words"][2] % 5 == 0:
                        finalresult = "5 more to reach level " + str((context["words"][2] + 5) // 10) + " . " + finalresult
                    return finalresult,0
                else:
                    context["credit"] += 20
                    speech_output = "I can't find a word that starts with " + user_word[len(user_word) - 1] + " . "
                    return speech_output,1
        #else if it is not the first time
        else:
            last_reply = used_words[len(used_words) - 1]
            #user word neither follow last reply nor rhyme
            if (user_word[0] != last_reply[len(last_reply) - 1]) and \
                (self.words[user_word][2] != self.words[last_reply][2]):
                context["words"][1] += 1
                speech_output += "Your word " + user_word + " doesn't start with " + \
                                last_reply[len(last_reply) - 1] + " in word " + last_reply + " ."\
                                "Please pick a word that starts with " + last_reply[len(last_reply) - 1] + " . "
                if context["words"][1] == 2:
                    speech_output += " You may say back to exit game. " + str(5 - context["words"][1]) + " more mistakes are allowed"
                elif context["words"][1] > 2 and context["words"][1] < 5:
                    speech_output += str(5 - context["words"][1]) + " more mistakes are allowed"
                elif context["words"][1] == 5:
                    speech_output += " You made 5 mistakes."
                    return speech_output,2
                return speech_output,0
            #user word follow last reply and rhyme
            elif (user_word[0] == last_reply[len(last_reply) - 1]) and \
                (self.words[user_word][2] == self.words[last_reply][2]):
                context["words"][1] = 0
                speech_output += "Nice job , Your word " + user_word + " rhymes with word " + last_reply + " . "
                context["words"][0].append(user_word)
                result = self.find_word_start_with(used_words,user_word)
                if result != "not found":
                    context["words"][0].append(result)
                    finalresult = speech_output + self.spell_word(result)
                    context["words"][2] += 1
                    if context["words"][2] == 10:
                        return "",1
                    elif context["words"][2] % 10 == 0:
                        finalresult = random.choice(self.compliments) + " , you reach level " + str(context["words"][2] // 10) + \
                            " . you may say back to try something else . " + finalresult
                    elif context["words"][2] % 5 == 0:
                        finalresult = "5 more to reach level " + str((context["words"][2] + 5) // 10) + " . " + finalresult
                    return finalresult,0
                else:
                    context["credit"] += 20
                    speech_output = "I can't find a word that starts with " + user_word[len(user_word) - 1] + " . "
                    return speech_output,1
            #user word doesn't follow last reply but rhyme
            elif (user_word[0] != last_reply[len(last_reply) - 1]) and \
                (self.words[user_word][2] == self.words[last_reply][2]):
                context["words"][1] = 0
                speech_output = "Hmm , Your word " + user_word + " rhymes with word " + last_reply + " . "
                context["words"][0].append(user_word)
                result = self.find_word_start_with(used_words,user_word)
                if result != "not found":
                    context["words"][0].append(result)
                    finalresult = speech_output + self.spell_word(result)
                    context["words"][2] += 1
                    if context["words"][2] == 10:
                        return "",1
                    elif context["words"][2] % 10 == 0:
                        finalresult = random.choice(self.compliments) + " , you reach level " + str(context["words"][2] // 10) + \
                            " . you may say back to try something else . " + finalresult
                    elif context["words"][2] % 5 == 0:
                        finalresult = "5 more to reach level " + str((context["words"][2] + 5) // 10) + " . " + finalresult
                    return finalresult,0
                else:
                    context["credit"] += 20
                    speech_output = "I can't find a word that starts with " + user_word[len(user_word) - 1] + " . "
                    return speech_output,1
            #user word follow last reply without rhyme
            else:
                context["words"][1] = 0
                context["words"][0].append(user_word)
                result = self.find_word_start_with(used_words,user_word)
                if result != "not found":
                    context["words"][0].append(result)
                    finalresult = self.spell_word(result)
                    context["words"][2] += 1
                    if context["words"][2] == 10:
                        return "",1
                    elif context["words"][2] % 10 == 0:
                        finalresult = random.choice(self.compliments) + " , you reach level " + str(context["words"][2] // 10) + \
                            " . you may say back to try something else . " + finalresult
                    elif context["words"][2] % 5 == 0:
                        finalresult = "5 more to reach level " + str((context["words"][2] + 5) // 10) + " . " + finalresult
                    return finalresult,0
                else:
                    context["credit"] += 20
                    speech_output = "I can't find a word that starts with " + user_word[len(user_word) - 1] + " . "
                    return speech_output,1

    def help(self,text,context):
        if context["credit"] >= 10:
            context["credit"] -= 10
            response = "You have " + str(context["credit"]) + " credits left . Hint is , " + self.find_word_start_with(context["words"][0],context["words"][0][-1],False)
        else:
            response = ""
        return response

    # --------------- Helpers that used in word game ----------------------

    def rhythm(self,selectedDict,user_word):
        wordUser = self.words[user_word]
        userVowel = wordUser[len(wordUser) - 1]

        matchingDict = {k:v for k,v in selectedDict.items() if v[2] == userVowel}

        if len(matchingDict) > 0:
            result = max(matchingDict, key=lambda i: int(matchingDict[i][0]))
            return result
        else:
            return "not found"

    #find word that start with letter that are not used in dic
    def find_word_start_with(self,used_words,user_word,rhythm=True):
        letter = user_word[len(user_word) - 1]
        selectedDict = {k:v for k,v in self.words.items() if k.startswith(letter) and k not in used_words}
        if rhythm is True:
            tmp = self.rhythm(selectedDict,user_word)
            if tmp == "not found":
                return max(selectedDict, key=lambda i: int(selectedDict[i][0]))
            else:
                return tmp
        else:
            result = max(matchingDict, key=lambda i: int(selectedDict[i][0]))
            return result

    #spell word for output
    def spell_word(self,word):
        return word + " , " + word[len(word) - 1] + "<break time=\"500ms\"/>"
