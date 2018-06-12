import os

class intentDetect:
    def __init__(self):
        # Here's our list of intents names
        self.intents = ["AMAZON.PauseIntent"
                        , "AMAZON.HelpIntent"
                        , "AMAZON.RepeatIntent"
                        , "AMAZON.ResumeIntent"
                        , "AMAZON.YesIntent"
                        , "AMAZON.NoIntent"
                        ]
        # Make a dictionary with intent names as keys and list of intent words/phrases as values.
        self.intent_words = {}
        for intent_name in self.intents:
            intent_file_path = 'intent/' + intent_name + '_words.txt'
            # Check that the file exists for the intent.
            if os.path.isfile(intent_file_path):
                self.intent_words[intent_name] = open(intent_file_path,'r').read().split('\n')

    # Checks if any of the intent words for the specified intent name
    # are in the given input text.
    # Returns true if the one of the intent words is in the text.
    # Returns false otherwise.
    def intent_in_text(self, input_text, intent_name):
        # Check that this is a valid intent first.
        if not intent_name in self.intents:
            return False
        # Get the intent's list of words.
        words_to_check = self.intent_words[intent_name]

        # Save time by not tokenizing; instead, just put a space before and after
        # each word (and before and after the input text)
        parsed_input = " " + input_text + " "
        for word in words_to_check:
            parsed_word = " " + word + " "
            if parsed_word in parsed_input:
                return True

        #return True in [e in words_to_check for e in input_text.split()]
        # If we have reached this point, then none of the words in the intent's word list
        # appeared in the input. Return false.
        return False
    def isIntent(self,Uinput,intent,Request):
        return self.intent_in_text(Uinput, intent) or self.alexaintent(Request,intent)
    def alexaintent(self,Request,intent):
        return "intent" in Request and Request["intent"]["name"]==intent
    def detect_intent(self, input_text, context,Request):
        # If no intents were detected, return the empty string.
        detected_intents = []
        # Detected intents have an implicit hierarchy, based on which intent is checked first.
        # Intent names match those which are used in the flowChange function in WiseMacaw.py.
        parsed_input = input_text.lower()
        if self.isIntent(parsed_input, "AMAZON.PauseIntent",Request):
            print ("PauseIntent found")
            context["pause"]=True
            detected_intents.append("AMAZON.PauseIntent")
        elif self.isIntent(parsed_input, "AMAZON.HelpIntent",Request):
            print ("Help intent found")
            context["help"]=True
            detected_intents.append("AMAZON.HelpIntent")
        elif self.isIntent(parsed_input, "AMAZON.RepeatIntent",Request):
            print ("Repeat Intent found")
            context["repeat"]=True
            detected_intents.append("AMAZON.RepeatIntent")
        elif self.isIntent(parsed_input, "AMAZON.NoIntent",Request):
            print ("No intent found")
            detected_intents.append("AMAZON.NoIntent")
        elif self.isIntent(parsed_input, "AMAZON.YesIntent",Request):
            print ("Yes intent found")
            detected_intents.append("AMAZON.YesIntent")
        elif self.alexaintent(Request,"ID"):
            print("ID intent found")
            detected_intents.append("ID")
        elif self.isIntent(parsed_input, "AMAZON.ResumeIntent",Request):
            print ("Resume intent found")
            detected_intents.append("AMAZON.ResumeIntent")
        return self.intent_hierarchy(detected_intents)

    def intent_hierarchy(self,intentList):
        if intentList:
            return intentList[0]
        else:
            return None
