from module import module
#from aiml import Kernel
import random
import re
import string
import sys

class aimlbot(module):
    def __init__(self):
        super().__init__()
        print ("initializing aimlbot")
        # Read the list of drinks.
        self.drinks = open('data/drinks.txt','r').read().split('\n')
        # For drink patterns, first try to grab something after the first-half patterns.
        # Regardless of if we do or don't get something, try to grab the first word after
        # the second-half patterns.
        # Drink patterns (first half):
        #   i'll have (drink name)
        #   ive me (drink name)
        #   et me (drink name)
        #   you have (drink name)
        # Drink patterns (second half):
        #   of (drink name)
        #   some (drink name)
        #   a (drink name)
        #   any (drink name)
        # NOTE: These patterns assume a one-word drink name, which may not be true.
        self.drink_patterns_first = []
        self.drink_patterns_first.append(" ill have ")
        self.drink_patterns_first.append(" give me ")
        self.drink_patterns_first.append(" get me ")
        self.drink_patterns_first.append(" you have ")
        self.drink_patterns_second = []
        self.drink_patterns_second.append(" of ")
        self.drink_patterns_second.append(" some ")
        self.drink_patterns_second.append(" a ")
        self.drink_patterns_second.append(" any ")
        # A set of topics that the aimlbot, as the bartender, can discuss.
        self.discussion_topics = []
        # You're with the detective, so what do you want?
        self.discussion_topics.append("WHAT_DO_YOU_WANT")
        # How are you doing today?
        self.discussion_topics.append("HOW_ARE_YOU_DOING")
        # What's your favorite: animal, plant, food, music, movie, game.
        self.discussion_topics.append("FAVORITE|animal")
        self.discussion_topics.append("FAVORITE|plant")
        self.discussion_topics.append("FAVORITE|food")
        self.discussion_topics.append("FAVORITE|music")
        self.discussion_topics.append("FAVORITE|movie")
        self.discussion_topics.append("FAVORITE|game")

    # Create the conversational part of the first response from the bot.
    def first_response(self, input_text, context_data):
        return_text = ""
        return_text = "How are you doing today?"
        context_data["covered_topics"].append("how are you")
        context_data["previous_topic"] = "how are you"
        return return_text

    # possible user responses to the question of "how are you"
    def how_are_you(self, input_text, context):
        good_bad_templates = []
        return_text = ""

        # Add spaces to the start and end of the input text.
        # This will allow us to search for individual words using regex
        # by placing a space before and after search strings, without
        # missing the case where the first and last words do not have
        # spaces before or after them.
        parsed_input = " " + input_text + " "

        # Look for a 'not.' This indicates a negation of the statement.
        negate = False
        negation = {}
        negation["patterns"] = [r' not ']

        # Cover 'bad' templates first
        # 'bad' templates
        #   Terrible
        #   Terribly
        #   Awful
        #   Awfully
        #   Horrible
        #   Horribly
        #   Bad
        #   Disastrous
        #   Disastrously
        # A negation of any of these means "good"
        bad = {}
        # Individual phrases and words have spaces before and after them
        # to prevent regex from matching them in the middle of other words.
        bad["patterns"] = [r' terrible '
                         , r' terribly '
                         , r' awful '
                         , r' awfully '
                         , r' horrible '
                         , r' horribly '
                         , r' bad '
                         , r' disastrous '
                         , r' disastrously ']
        bad["text"] = "I'm sorry to hear that, the bartender says. Hope your day takes a turn for the better. "
        bad["topic"] = "doing bad"
        good_bad_templates.append(bad)

        # 'good' templates
        #   Fine
        #   Good
        #   Ok
        #   Okay
        #   Well
        #   Swimmingly
        #   Alright
        #   Great
        #   Fantastic
        #   Spectacular
        #   Spectacularly
        #   Splendid
        #   Splendidly
        #   Wonderful
        #   Wonderfully
        # A negation of any of these means "bad"
        good = {}
        # Individual phrases and words have spaces before and after them
        # to prevent regex from matching them in the middle of other words.
        good["patterns"] = [r' fine '
                         , r' good '
                         , r' ok '
                         , r' okay '
                         , r' well '
                         , r' swimmingly '
                         , r' alright '
                         , r' great '
                         , r' fantastic '
                         , r' spectacular '
                         , r' splendid ']
        good["text"] = "That's great to hear, she says, I'm doing alright myself. "
        good["topic"] = "doing good"
        good_bad_templates.append(good)

        # First, check for a negation.
        for pattern in negation["patterns"]:
            search_result = re.search(pattern, parsed_input)
            if search_result:
                negate = True

        # Next, check for a good/bad response.
        input_is_good = None
        for pattern in good["patterns"]:
            search_result = re.search(pattern, parsed_input)
            if search_result:
                if negate:
                    input_is_good = False
                else:
                    input_is_good = True
        # If we could not determine whether the input is good or not from the good patterns,
        # then check the bad patterns
        if input_is_good is None:
            for pattern in bad["patterns"]:
                search_result = re.search(pattern, parsed_input)
                if search_result:
                    if negate:
                        input_is_good = True
                    else:
                        input_is_good = False
        # If we STILL don't know whether it was a good or a bad input, then leave the return text as the empty string.
        # Otherwise, the return text is either the good response or the bad response.
        if not input_is_good is None:
            if input_is_good:
                return_text = good["text"]
                #context_data["covered_topics"].append(good["topic"])
                #context_data["previous_topic"] = good["topic"]
            else:
                return_text = bad["text"]
                #context_data["covered_topics"].append(bad["topic"])
                #context_data["previous_topic"] = bad["topic"]

        # Choose a new topic prompt.
        return_text += "Hey, I've been wondering something. " + self.get_topic_to_discuss("", context)

        return return_text

    def salutations(self, input_text, context):
        salutation_templates = []

        # 'how are you' templates:
        #   .*how are you (today.*|doing( today)*)
        #       - how are you?
        #       - how are you today?
        #       - how are you doing?
        #       - how are you, (name)?
        #       - how are you doing today?

        # 'hello' templates:
        #   - hello
        #   - hello again
        #   - hello, how are you?
        #   - hi
        #   - hi there
        #   - hey
        #   - hey there
        #   - howdie
        #   - good morning
        #   - good day

        # 'goodbye' templates:
        #   - goodbye
        #   - byebye
        #   - bye bye
        #   - have a good night
        #   - good night
        #   - catch you later
        #   - see you
        #   - farewell
        #   - see you soon

        how_are_you = {}
        how_are_you["patterns"] = [r'.*how are you( (today.*|doing( today)*))*']
        how_are_you["text"] = "I'm doing fine, thanks for asking."
        how_are_you["topic"] = "how am I"
        salutation_templates.append(how_are_you)

        hello = {}
        hello["patterns"] = [r'hello'
                             , r'hello again'
                             , r'hi'
                             , r'hi there'
                             , r'hey'
                             , r'hey there'
                             , r'howdie'
                             , r'good morning'
                             , r'good day']
        hello["text"] = "Hello to you too, she says with a nod. "
        hello["topic"] = "hello"
        salutation_templates.append(hello)

        goodbye = {}
        goodbye["patterns"] = [r'goodbye'
                             , r'byebye'
                             , r'bye bye'
                             , r'have a good night'
                             , r'good night'
                             , r'catch you later'
                             , r'see you'
                             , r'farewell'
                             , r'see you soon']
        goodbye["text"] = "Leaving so soon? The bartender asks. "
        goodbye["topic"] = "goodbye"
        salutation_templates.append(goodbye)

        for template in salutation_templates:
            for pattern in template["patterns"]:
                search_result = re.search(pattern, input_text)
                if search_result:
                    return_text = ""
                    return_text += template["text"]
                    return return_text
        return ""

    # Would be more rich with category member catchers for each favorite category. (e.g. animals, movies, games, music genres, food, etc.)
    def favorites(self, input_text, context):
        #print ("favorites input text: " + input_text)
        favorite_templates = []

        # Default least-favorite answer
        least_favorite = {}
        least_favorite["patterns"] = [r'.*your least (favorite|favourite).*']
        least_favorite["text"] = "I don't really have a least favorite one of those."
        least_favorite["topic"] = "least favorite"
        favorite_templates.append(least_favorite)

        # 'Favorite question' templates:
        #   .*your (most )*(favorite|favourite) (sort of |kind of |type of )*blank.*
        #       - what's your most favorite (blank)?
        #       - what's your favorite (blank)?
        #       - what's your favorite type of (blank)?
        #       - what's your favorite kind of (blank)?
        #       - what's your favorite sort of (blank)?
        #       - tell me your favorite (blank)
        #       - tell me about your favorite (blank)
        #   .*what (sort of |kind of |type of )*blank is your (most )*(favorite|favourite).*
        #       - what blank is your favorite?
        #       - what blank is your most favorite?
        #   r'.*what (sort of |kind of |type of )*blank do you like.*'
        #       - what blank do you like?
        #       - what blank do you like most?
        #       - what sort of blank do you like most?
        #       - what sort of blank do you like?
        #       - what kind of blank do you like most?
        #       - what kind of blank do you like?
        #       - what type of blank do you like?
        #       - what type of blank do you like most?
        #   .*do you have a (most )*(favorite|favourite) (sort of |kind of |type of )*blank.*
        #       - do you have a favorite blank?
        #       - do you have a most favorite blank?
        #   .*(a|the) (sort of |kind of |type of )*blank (that )*you like.*
        #       - is there a blank that you like most?
        #       - is there a blank that you like?
        #       - is there a blank you like?
        #       - is there a blank that you like most?
        #       - is there a blank that you like best?
        #       - tell me about a blank that you like

        favorite_animal = {}
        favorite_animal["patterns"] = [r'.*your (most )*(favorite|favourite) (sort of |kind of |type of )*(animal|pet).*'
                                       , r'.*what (sort of |kind of |type of )*(animal|pet) is your (most )*(favorite|favourite).*'
                                       , r'.*what (sort of |kind of |type of )*(animal|pet) do you like.*'
                                       , r'.*do you have a (most )*(favorite|favourite) (sort of |kind of |type of )*(animal|pet).*'
                                       , r'.*(a|the) (sort of |kind of |type of )*(pet|animal) (that )*you like.*']
        favorite_animal["text"] = "I like dogs the best, the bartender says with a grin, they're just so cute. Who wouldn't love them? "
        favorite_animal["topic"] = "favorite|animal"
        favorite_templates.append(favorite_animal)

        favorite_dog = {}
        favorite_dog["patterns"] = [r'.*your (most )*(favorite|favourite) (sort of |kind of |type of )*dog.*'
                                       , r'.*what (sort of |kind of |type of )*dog is your (most )*(favorite|favourite).*'
                                       , r'.*what (sort of |kind of |type of )*dog do you like.*'
                                       , r'.*do you have a (most )*(favorite|favourite) (sort of |kind of |type of )*dog.*'
                                       , r'.*(a|the) (sort of |kind of |type of )*dog (that )*you like.*']
        favorite_dog["text"] = "I like all dogs!"
        favorite_dog["topic"] = "favorite|dog"
        favorite_templates.append(favorite_dog)

        favorite_plant = {}
        favorite_plant["patterns"] = [r'.*your (most )*(favorite|favourite) (sort of |kind of |type of )*(plant|flower|tree).*'
                                       , r'.*what (sort of |kind of |type of )*(plant|flower|tree) is your (most )*(favorite|favourite).*'
                                       , r'.*what (sort of |kind of |type of )*(plant|flower|tree) do you like.*'
                                       , r'.*do you have a (most )*(favorite|favourite) (sort of |kind of |type of )*(plant|flower|tree).*'
                                       , r'.*(a|the) (sort of |kind of |type of )*(plant|flower|tree) (that )*you like.*']
        favorite_plant["text"] = "My favorite plant is the fern. It just looks so unique. The bartender pantomimes the shape of a fern. "
        favorite_plant["topic"] = "favorite|plant"
        favorite_templates.append(favorite_plant)

        favorite_food = {}
        favorite_food["patterns"] = [r'.*your (most )*(favorite|favourite) (sort of |kind of |type of )*food.*'
                                       , r'.*what (sort of |kind of |type of )*food is your (most )*(favorite|favourite).*'
                                       , r'.*what (sort of |kind of |type of )*food do you like.*'
                                       , r'.*do you have a (most )*(favorite|favourite) (sort of |kind of |type of )*food.*'
                                       , r'.*(a|the) (sort of |kind of |type of )*food (that )*you like.*']
        favorite_food["text"] = "I could always go for some chips. The bartender looks around, patting her stomach. Too bad I don't serve food here. "
        favorite_food["topic"] = "favorite|food"
        favorite_templates.append(favorite_food)

        favorite_music = {}
        favorite_music["patterns"] = [r'.*your (most )*(favorite|favourite) (sort of |kind of |type of )*(music|song).*'
                                       , r'.*what (sort of |kind of |type of )*(music|song) is your (most )*(favorite|favourite).*'
                                       , r'.*what (sort of |kind of |type of )*(music|song) do you like.*'
                                       , r'.*do you have a (most )*(favorite|favourite) (sort of |kind of |type of )*(music|song).*'
                                       , r'.*(a|the) (sort of |kind of |type of )*(music|song) (that )*you like.*']
        favorite_music["text"] = "I like jazz, the bartender says. It can be so hectic and exciting, but it can be really relaxing too, you know? "
        favorite_music["topic"] = "favorite|music"
        favorite_templates.append(favorite_music)

        favorite_movie = {}
        favorite_movie["patterns"] = [r'.*your (most )*(favorite|favourite) (sort of |kind of |type of )*(movie|film).*'
                                       , r'.*what (sort of |kind of |type of )*(movie|film) is your (most )*(favorite|favourite).*'
                                       , r'.*what (sort of |kind of |type of )*(movie|film) do you like.*'
                                       , r'.*do you have a (most )*(favorite|favourite) (sort of |kind of |type of )*(movie|film).*'
                                       , r'.*(a|the) (sort of |kind of |type of )*(movie|film) (that )*you like.*']
        favorite_movie["text"] = "My favorite movie? Oh, I can't just choose one, she says, rubbing her chin. Noir is, by far, my favorite genre, though. "
        favorite_movie["topic"] = "favorite|movie"
        favorite_templates.append(favorite_movie)

        favorite_game = {}
        favorite_game["patterns"] = [r'.*your (most )*(favorite|favourite) (sort of |kind of |type of )*(game|videogame|video game).*'
                                       , r'.*what (sort of |kind of |type of )*(game|videogame|video game) is your (most )*(favorite|favourite).*'
                                       , r'.*what (sort of |kind of |type of )*(game|videogame|video game) do you like.*'
                                       , r'.*do you have a (most )*(favorite|favourite) (sort of |kind of |type of )*(game|videogame|video game).*'
                                       , r'.*(a|the) (sort of |kind of |type of )*(game|videogame|video game) (that )*you like.*']
        favorite_game["text"] = "I don't really play videogames, the bartender says, except the really old arcade games. You know, tetris and stuff. "
        favorite_game["topic"] = "favorite|game"
        favorite_templates.append(favorite_game)

        for template in favorite_templates:
            for pattern in template["patterns"]:
                search_result = re.search(pattern, input_text)
                if search_result:
                    return_text = ""
                    return_text += template["text"]
                    # Remove the last topic; it was probably a what's your favorite question.
                    context["Bartender"]["last_topic"] = "NONE"
                    return return_text
        return ""

    # The bot has just asked if they can get the user anything to drink.
    def get_drink_response(self, user_input, context):
        return_text = ""
        padded_input = " " + user_input + " "
        # First, try to detect a drink name in the text.
        drink_found = ""
        # Don't pad the drink names before checking, so we can catch all plurals.
        for drink_name in self.drinks:
            # padded_drink_name = " " + drink_name + " "
            if (drink_name in padded_input):
                drink_found = drink_name
                break
        # If we've found a drink in the input, we're done!
        # Otherwise, try a drink pattern to find a drink name.
        #if drink_found == "":
        #    self.get_drink_from_patterns(padded_input)
        # If we still haven't found a drink, be vague.
        if drink_found == "":
            drink_found = "something"
            return_text = "The bartender gets something from behind the counter and slides it over to you. Try that, she says. "
        else:
            return_text = "The bartender gets " + drink_found + " from behind the counter and slides it over to you. Here you go, she says. "
        
        # After giving a drink, start another discussion topic.
        new_topic_text = self.get_topic_to_discuss(padded_input, context)
        return_text += new_topic_text

        return return_text

    # The bot has just asked for the user's motive.
    def get_motive_response(self, user_input, context):
        return_text = ""

        # Check first if they mention the chatbot's voice
        # chatbot_voice_mentioned = self.chatbot_voice_mentioned(user_input)

        # Check if they mention that they're looking for information
        # about the chatbot's voice.
        #looking_for_info_mentioned = self.looking_for_info_mentioned(user_input)

        # Check if they mention the detective.
        #detective_mentioned = self.detective_mentioned(user_input)

        # Check if they mention a crime or any sort of criminal
        #crime_mentioned = self.crime_mentioned(user_input)

        # The hierarchy is: chatbot, crime, looking for info, detective, anything else.
        if self.chatbot_voice_mentioned(user_input) == True:
            return_text = "The chatbot's voice? You know, I think I did hear something about that, the bartender begins, but it's just not coming to me right now. Sorry. I know, let's talk about something else. "
            # The topic will change to whatever is chosen here.
            return_text += self.get_topic_to_discuss(user_input, context)
        elif self.crime_mentioned(user_input) == True:
            return_text = "A crime, huh? the bartender says, resting her chin on her hand, I did hear something about the chatbot's voice, but it's not coming to me right now. Sorry. I know, let's talk about something else. "
            # The topic will change to whatever is chosen here.
            return_text += self.get_topic_to_discuss(user_input, context)
        elif self.looking_for_info_mentioned(user_input) == True:
            return_text = "Looking for information, huh? That sounds like her, the bartender says, gesturing towards the detective. So, what do you need info about? "
            # The topic will remain WHAT_DO_YOU_WANT
        elif self.detective_mentioned(user_input) == True:
            return_text = "Ah, yes, the detective, she says, nodding in her direction, she used to come around all the time. But what are you two hoping to hear about here? "
            # The topic will remain WHAT_DO_YOU_WANT
        else:
            return_text = "Hmm. Well, maybe I can help. Who knows, she says, cleaning some dirt off the counter, maybe I just need some time to remember. I know, let's talk about something else. "
            # The topic will change to whatever is chosen here.
            return_text += self.get_topic_to_discuss(user_input, context)
        return return_text

    def response(self,text,context):
        # The response sieve:
        #   Layer 1: Look for a response related to the last topic the aimlbot mentioned.
        #   Layer 2: Look for a response that conforms to some general pattern that can be mirrored or otherwise responded to.
        #   Layer 3: Give a response that doesn't rely on the user's input.
        # If any of the layers of the sieve fails, it continues to the next layer. The last layer
        # will always return some response.
        print ("Starting aimlbot response. Last topic: " + context["Bartender"]["last_topic"])
        # Parse input: remove all punctutation and set all to lower case.
        parsed_input = ''.join(c for c in text if c not in string.punctuation)
        parsed_input = parsed_input.lower()

        response_text = ""
        last_topic = context["Bartender"]["last_topic"]
        #print ("Favorite check: " + last_topic.split("|")[0])
        # Layer 1: Use the last topic to figure out which response function to call.
        if last_topic == "SOMETHING_TO_DRINK":
            response_text = self.get_drink_response(parsed_input, context)
        elif last_topic == "WHAT_DO_YOU_WANT":
            response_text = self.get_motive_response(parsed_input, context)
        elif last_topic == "HOW_ARE_YOU_DOING":
            response_text = self.how_are_you(parsed_input, context)
        # The FAVORITE format is FAVORITE|SUBJECT
        elif last_topic.split("|")[0] == "FAVORITE":
            #print ("Favorite found. Checking favorite " + last_topic.split("|")[1])
            response_text = self.favorites("whats your favorite " + last_topic.split("|")[1], context)
        # If the response text is still the empty string, Layer 1 has failed to find a response.
        # Layer 2: Find a general pattern in the user input to determine a response.
        if response_text == "":
            response_text = self.find_template_response(parsed_input, context)
        # If the response text is still the empty string, Layer 2 has failed to find a response.
        # Layer 3: Return a response that doesn't rely on user input. 
        if response_text == "":
            response_text = self.get_generic_response(context)
        return response_text

    # Find a response by checking each template for a match
    def find_template_response(self, input_text, context):
        # Check salutations
        salutations_response = self.salutations(input_text, context)
        if not salutations_response == "":
            return salutations_response
        # Check asking for one of the aimlbot's favorites
        favorites_response = self.favorites(input_text, context)
        if not favorites_response == "":
            return favorites_response
        return ""

    # Get a generic response
    def get_generic_response(self, context):
        return_text = ""

        # Half the time, roll into a new topic.
        random_choice = random.randint(0, 5)
        if random_choice == 0:
            return_text = "The bartender nods along, finally finishing one glass and picking up another to clean. She gestures for you to continue. "
        elif random_choice == 1:
            return_text = "That's interesting, the bartender says, though you can't tell if she was actually listening. Please, she says, go on. "
        elif random_choice == 2:
            return_text += "Is that so? the bartender asks idly, but you can tell she's preoccupied keeping an eye on the drunkard. Go on, she says, I'm listening. "
        elif random_choice == 3:
            return_text += "The bartender nods along, finally finishing one glass and picking up another to clean. Hey, I've been wondering something, she begins. "
            return_text += self.get_topic_to_discuss("", context)
        elif random_choice == 4:
            return_text += "That's interesting, the bartender says, though you can't tell if she was actually listening. Tell me something. "
            return_text += self.get_topic_to_discuss("", context)
        elif random_choice == 5:
            return_text += "Is that so? the bartender asks idly, but you can tell she's preoccupied keeping an eye on the drunkard. Hey, how about this. "
            return_text += self.get_topic_to_discuss("", context)

        return return_text

    # PROMPTS
    # What do you want?
    def what_do_you_want_prompt(self):
        return_text = ""
        # Randomly pick one.
        return_text = "Now, you're here with the detective, which means that you must be here for a reason. "
        random_choice = random.randint(0, 2)
        if random_choice == 0:
            return_text += "So, what is it? "
        if random_choice == 1:
            return_text += "So, what can I do for you? "
        if random_choice == 2:
            return_text += "So, how can I help you? "

        return return_text

    # How are you doing?
    def how_are_you_doing_prompt(self):
        return_text = ""
        random_choice = random.randint(0, 2)
        if random_choice == 0:
            return_text = "So, how are you doing today? "
        if random_choice == 1:
            return_text = "How are you doing? Well? Not well? "
        if random_choice == 2:
            return_text = "How's your day going? "
        return return_text

    # What's your favorite X?
    def whats_your_favorite_prompt(self, subject):
        return_text = ""
        random_choice = random.randint(0, 2)
        if random_choice == 0:
            return_text = "What's your favorite " + subject + "? "
        if random_choice == 1:
            return_text = "What " + subject + " is your favorite? "
        if random_choice == 2:
            return_text = "What's your most favorite " + subject + "? "
        return return_text

    # HELPER FUNCTIONS
    # Choose a topic for the bot to prompt to the user.
    # Does the following bookkeeping:
    #   Adds the topic that it chooses to the list of topics discussed
    #   Flushes the list of topics discussed when there are no more topics that haven't been discussed
    def get_topic_to_discuss(self, input_text, context):
        return_text = ""
        chosen_topic = ""

        # If we have run out of topics that haven't been mentioned, reset the topic lists.
        if (len(context["Bartender"]["topics_not_mentioned"]) <= 0):
            self.reset_topics(context)

        # First, if the bartender hasn't asked the user their motive yet, do so now.
        if not context["Bartender"]["motive_asked"]:
            context["Bartender"]["motive_asked"] = True
            chosen_topic = "WHAT_DO_YOU_WANT"
            return_text = self.what_do_you_want_prompt()
        # Otherwise, randomly pick a topic from the list of topics that haven't been mentioned yet.
        else:
            chosen_topic = random.choice(context["Bartender"]["topics_not_mentioned"])
        # Get the prompt for the chosen topic.
        if chosen_topic == "WHAT_DO_YOU_WANT":
            return_text = self.what_do_you_want_prompt()
        elif chosen_topic == "HOW_ARE_YOU_DOING":
            return_text = self.how_are_you_doing_prompt()
        # Favorite topics are FAVORITE|SUBJECT.
        elif chosen_topic.split("|")[0] == "FAVORITE":
            return_text = self.whats_your_favorite_prompt(chosen_topic.split("|")[1])

        # Do some bookkeeping on the chosen topic.
        self.choose_topic(chosen_topic, context)

        return return_text


    # Functions for checking if something was mentioned.
    # Check if the chatbot's voice was mentioned
    def chatbot_voice_mentioned(self, user_input):
        chatbot_voice_keywords = []
        chatbot_voice_keywords.append("chatbot")
        chatbot_voice_keywords.append("voice")
        for chatbot_voice_keyword in chatbot_voice_keywords:
            if chatbot_voice_keyword in user_input:
                print ("Chatbot's voice mentioned")
                return True
        return False
    # Check if the user mentions that they're looking for information or if
    # the bot has heard something.
    def looking_for_info_mentioned(self, user_input):
        looking_for_info_keywords = []
        looking_for_info_keywords.append("info")
        looking_for_info_keywords.append("heard anything")
        looking_for_info_keywords.append("heard something")
        looking_for_info_keywords.append("you've heard")
        for looking_for_info_keyword in looking_for_info_keywords:
            if looking_for_info_keyword in user_input:
                print ("Looking for info mentioned")
                return True
        return False
    # Check if the user mentions the detective.
    def detective_mentioned(self, user_input):
        detective_keywords = []
        detective_keywords.append("detective")
        detective_keywords.append("sleuth")
        detective_keywords.append("police")
        detective_keywords.append("cop")
        detective_keywords.append("my friend")
        for detective_keyword in detective_keywords:
            if detective_keyword in user_input:
                print ("Detective mentioned")
                return True
        return False
    # Check if the user mentions a crime or a criminal
    def crime_mentioned(self, user_input):
        crime_keywords = []
        crime_keywords.append("criminal")
        crime_keywords.append("crime")
        crime_keywords.append("thief")
        crime_keywords.append("thieve")
        crime_keywords.append("stole")
        crime_keywords.append("steal")
        crime_keywords.append("theft")
        crime_keywords.append("took")
        for crime_keyword in crime_keywords:
            if crime_keyword in user_input:
                print ("Crime mentioned")
                return True
        return False        

    # Bookkeeping function, for when a topic is chosen.
    def choose_topic(self, chosen_topic, context):
        # Add the topic to the list of topics mentioned
        context["Bartender"]["topics_mentioned"].append(chosen_topic)
        # Remove the topic from the list of topics not mentioned
        if chosen_topic in context["Bartender"]["topics_not_mentioned"]:
            context["Bartender"]["topics_not_mentioned"].remove(chosen_topic)
        # Set it as the last topic
        context["Bartender"]["last_topic"] = chosen_topic

    # Reset the lists of what topics have been mentioned and which ones haven't
    def reset_topics(self, context):
        context["Bartender"]["topics_mentioned"] = []
        # Refill the lists of topics to mention from the original list.
        context["Bartender"]["topics_not_mentioned"] = []
        for discussion_topic in self.discussion_topics:
            context["Bartender"]["topics_not_mentioned"].append(discussion_topic)

    def get_drink_from_patterns(self, input_text):
        drink_found = ""
        # First, try to get everything after a first-half drink pattern.
        first_half_input = input_text
        second_half_input = input_text
        for first_half_pattern in drink_patterns_first:
            # Split the padded input by the drink pattern, and get the first thing after the split.
            split_input_1 = input_text.split(first_half_pattern, 1)
            if split_input_1.count > 0:
                # If we have a split, then the first-half pattern was found.
                # Re-pad the first and second half inputs.
                first_half_input = split_input_1[0] + " "
                second_half_input = " " + split_input_1[1]
                break
        # Whether or not a first-half pattern was found, we now check a second-half pattern.
        # Check the second half.
        for second_half_pattern in drink_patterns_second:
            # Split the second half input by the pattern
            split_input_2 = second_half_input.split(second_half_pattern, 1)
            if split_input_2.count > 0:
                # If we have a split, then a second-half pattern was found.
                possible_drink_name = split_input_2[1]
                # Split by space and get the first item to get the first word after the second pattern.
                drink_found = possible_drink_name.split(" ", 1)[0]
                # We've found a possible drink name! We're done.
                break
        # If we still don't have a drink name and a first-half pattern was found,
        # check the first half as well for a second-half pattern.
        if not first_half_input == second_half_input:
            for second_half_pattern in drink_patterns_second:
                # Split the second half input by the pattern
                split_input_2 = first_half_input.split(second_half_pattern, 1)
                if split_input_2.count > 0:
                    # If we have a split, then a second-half pattern was found.
                    possible_drink_name = split_input_2[1]
                    # Split by space and get the first item to get the first word after the second pattern.
                    drink_found = possible_drink_name.split(" ", 1)[0]
                    # We've found a possible drink name! We're done.
                    break
        return drink_found

# For aimlbot testing. Remove when merging up.
"""
def main():
    print ("testing aimlbot")
    context = {}
    context["Bartender"] = {}
    context["Bartender"]["last_topic"] = ""
    context["Bartender"]["topics_mentioned"] = []
    context["Bartender"]["topics_not_mentioned"] = []
    context["Bartender"]["motive_asked"] = False
    context["Bartender"]["state"] = 0
    context["Bartender"]["visited"] = False
    
    bartender = aimlbot()

    text = ""
    return_text = ""
    while not text == "stop":
        text = input("User Input: ")
        if (text == "stop"):
            break
        if context["Bartender"]["state"] == 0:
            if not context["Bartender"]["visited"]:
                context["Bartender"]["visited"] = True
                return_text = "You approach the bartender, who is nodding along politely to the drunkard's ramblings. Welcome, she says, and good to see you back here, detective. Can I get you anything to drink? she asks, readying a glass."
            else:
                return_text = "You approach the bartender, who's still humoring the drunkard. Welcome back, she says to both you and the detective. Can I get you anything to drink? she asks, readying a glass."
            # Go to the 'in conversation' state.
            context["Bartender"]["state"] = 1
            # Set the Bartender's last topic accordingly. This will let the aimlbot know where to start.
            context["Bartender"]["last_topic"] = "SOMETHING_TO_DRINK"
        # If the state is 1, the user is in the middle of a conversation with the bartender.
        elif context["Bartender"]["state"] == 1:
            return_text = bartender.response(text, context)
        print ("Response: " + str(return_text))

if __name__ == "__main__":
    main()
"""