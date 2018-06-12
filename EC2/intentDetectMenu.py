import os

class intentDetectMenu:
    def __init__(self):
        # Here's our list of intents names
        self.intents = ["AMAZON.PauseIntent"
                        , "AMAZON.HelpIntent"
                        , "AMAZON.RepeatIntent"
                        , "AMAZON.ResumeIntent"
                        , "AMAZON.YesIntent"
                        , "AMAZON.NoIntent"
                        , "text adventure"
                        , "twitter trend"
                        , "message board"
                        , "word game"
                        , "Joke"
                        , "reddit news"
                        , "Assertive"
                        , "AmazonCommand"
                        , "riddle game"
                        , "SmallTalk"
                        ,"horoscope"]
        self.priority = {"high":["text adventure"
                                , "twitter trend"
                                , "message board"
                                , "word game"
                                , "Joke"
                                , "reddit news"
                                , "Assertive"
                                , "AmazonCommand"
                                , "riddle game"
                                , "SmallTalk"
                                , "horoscope"],
                        "low":["AMAZON.PauseIntent"
                            , "AMAZON.HelpIntent"
                            , "AMAZON.RepeatIntent"
                            , "AMAZON.ResumeIntent"
                            , "AMAZON.YesIntent"
                            , "AMAZON.NoIntent"]
                        }
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


    def detect_intent(self, input_text, context):
        # If no intents were detected, return the empty string.
        detected_intents = []
        # Detected intents have an implicit hierarchy, based on which intent is checked first.
        # Intent names match those which are used in the flowChange function in WiseMacaw.py.
        parsed_input = input_text.lower()
        if self.intent_in_text(parsed_input, "AMAZON.PauseIntent"):
            print ("PauseIntent found")
            detected_intents.append("AMAZON.PauseIntent")
            context["pause"] = True
        elif self.intent_in_text(parsed_input, "AMAZON.HelpIntent"):
            print ("Help intent found")
            detected_intents.append("AMAZON.HelpIntent")
            context["help"] = True
        elif self.intent_in_text(parsed_input, "AMAZON.RepeatIntent"):
            print ("Repeat Intent found")
            detected_intents.append("AMAZON.RepeatIntent")
            context["repeat"] = True
        elif self.intent_in_text(parsed_input, "AMAZON.ResumeIntent"):
            print ("Resume intent found")
            detected_intents.append("AMAZON.ResumeIntent")
            context["resume"] = True
        elif self.intent_in_text(parsed_input, "AMAZON.NoIntent"):
            print ("No intent found")
            detected_intents.append("AMAZON.NoIntent")
        elif self.intent_in_text(parsed_input, "AMAZON.YesIntent"):
            print ("Yes intent found")
            detected_intents.append("AMAZON.YesIntent")
        # NOTE: No context variable is set, meaning if an Amazon command is said
        # a module-specific intent will supercede it. This is desired behavior.
        elif self.intent_in_text(parsed_input, "AmazonCommand"):
            print ("AmazonCommand intent found")
            detected_intents.append("AmazonCommand")
        # Only check for module-specific intents if a module is not currently holding.
        # Module specific intent names will match the names of the corresponding module's test code name.
        elif context["hold"] == False:
            if self.intent_in_text(parsed_input, "text adventure"):
                detected_intents.append("text adventure")
            elif self.intent_in_text(parsed_input, "twitter trend"):
                detected_intents.append("twitter trend")
            elif self.intent_in_text(parsed_input, "message board"):
                detected_intents.append("message board")
            elif self.intent_in_text(parsed_input, "word game"):
                detected_intents.append("word game")
            elif self.intent_in_text(parsed_input, "Joke"):
                detected_intents.append("Joke")
            elif self.intent_in_text(parsed_input, "reddit news"):
                detected_intents.append("reddit news")
            elif self.intent_in_text(parsed_input, "Assertive"):
                detected_intents.append("Assertive")
            elif self.intent_in_text(parsed_input, "riddle game"):
                detected_intents.append("riddle game")
            elif self.intent_in_text(parsed_input, "SmallTalk"):
                detected_intents.append("SmallTalk")
            elif self.intent_in_text(parsed_input, "horoscope"):
                detected_intents.append("horoscope")
            if not detected_intents:
                print (str(detected_intents) + " intent found")

        return self.intent_hierarchy(detected_intents)

    def intent_hierarchy(self,intentList):
        if len(intentList)==1:
            return intentList[0]
        else:
            low = ""
            high = ""
            for e in intentList:
                if e in self.priority["high"]:
                    if not high:
                        high = e
                else:
                    if not low:
                        low = e
            if high and low:
                return high
            elif high:
                return high
            else:
                return low
