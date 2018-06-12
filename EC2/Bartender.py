from aimlbot import aimlbot

class Bartender:
    def __init__(self):
        self.module = aimlbot()
        # How many turns of conversation until the bartender remembers her hint.
        self.initial_hint_threshold = 5

    def initialize_context_variables(self, context):
        """Initializes all of the Bartender's context variables for this session."""

        # The variable in Context where all of the bartender's information will be stored
        context["Bartender"] = {}
        # Which state of the bartender's conversation we're in.
        #   0 = Just walked up to the bartender
        #   1 = In the middle of the conversation
        context["Bartender"]["state"] = 0
        # Whether or the user has visited the bartender before.
        context["Bartender"]["visited"] = False
        # Whether or not the Bartender has given a hint yet or not.
        context["Bartender"]["hint_given"] = False
        # Whether or not the Bartender has asked the user what they want (should only happen once)
        context["Bartender"]["motive_asked"] = False
        # How many number of turns the user has conversed with the aimlbot.
        # Only counts for a single conversation; if they leave, it'll get
        # reset when they come back.
        # Is incremented AFTER each conversation turn.
        context["Bartender"]["turn_count"] = 0
        # What the current threshold number of conversation turns is before the bartender gives a hint.
        # Starts at the initial hint threshold.
        context["Bartender"]["hint_threshold"] = self.initial_hint_threshold

        # What topic the aimlbot said last.
        context["Bartender"]["last_topic"] = "NONE"
        # What topics the bartender's already said
        context["Bartender"]["topics_mentioned"] = []
        # What topics the bartender hasn't said
        context["Bartender"]["topics_not_mentioned"] = []

    def response(self, text, context):
        return_text = ""
        # Redundant check if we need to initialize the Bartender context variables.
        if not "Bartender" in context:
            self.initialize_context_variables(context)
        # Next, check the state.
        # If the state is 0, the user has just walked up to the bartender and we're in the beginning of this conversation.
        if context["Bartender"]["state"] == 0:
            if not context["Bartender"]["visited"]:
                context["Bartender"]["visited"] = True
                return_text = "You approach the bartender, who is nodding along politely to the drunkard's ramblings. Welcome, she says, and good to see you back here, detective. Can I get you anything to drink? she asks, readying a glass."
            else:
                return_text = "You approach the bartender, who's still humoring the drunkard. Welcome back, she says to both you and the detective. Can I get you anything to drink? she asks, readying a glass."
            # Go to the 'in conversation' state.
            context["Bartender"]["state"] = 1
            # Reset the turn count to 1; it only counts for the current conversation.
            context["Bartender"]["turn_count"] = 1
            # Set the Bartender's last topic accordingly. This will let the aimlbot know where to start.
            context["Bartender"]["last_topic"] = "SOMETHING_TO_DRINK"
        # If the state is 1, the user is in the middle of a conversation with the bartender.
        elif context["Bartender"]["state"] == 1:
            # Check if we've reached the threshold and we haven't given a hint yet.
            if (context["Bartender"]["turn_count"] >= context["Bartender"]["hint_threshold"] and context["Bartender"]["hint_given"] == False):
                # If so, then the user has reached the threshold for the bartender to remember a hint.
                # Return the hint instead of the bartender's response.
                return_text = self.get_hint(text, context)
                # The user returns to Central Station after the hint is given, so we don't want to conversation continuing.
                # Call this NPC's pause function, without using the pause text.
                # This will end the conversation and set the bartender's
                # context variables accordingly.
                self.pause(text, context)
            else:
                return_text = self.module.response(text, context)
                context["Bartender"]["turn_count"] += 1

        return return_text

    def get_hint(self, text, context):
        """Returns the text for a hint
            Does the following bookkeeping:
                Increments which hint should be given next
                Brings the user back to Central Station
                Notes that the bartender has given at least one hint
                Increases the bartender's hint threshold
        """

        if context["hintIndex"]<=len(context["hints"]):
            return_text = "Oh, hey, actually, I just remembered something that might help you, she says. About the chatbot's voice. "
            return_text += context["hints"][context["hintIndex"]]
            return_text += "The detective quickly jots it down in her notebook, then hurries you back to Central Station. "
            return_text += "Nice work with the bartender, she says. "
            return_text += "Where should we go next? Northern University, the Eastern Commons, Southern Square, or the Western Woods? "
            context["Bartender"]["hint_given"] = True
            # Increase the threshold number of turns before the bartender gives another hint.
            context["Bartender"]["hint_threshold"] += 3
            # Set the location back to Central Station
            context["status"]=["Center","inArea","response"]
            # Increment which hint should be given next
            context["hintIndex"]+=1
        else:
            #TODO: write when we have given all hints
            return_text = "Turns out, a chatbot's voice is pretty powerful. I don't really understand it all, but it really shouldn't be tampered with. "
            return_text += "The detective jots something down in her notebook, then hurries you back to Central Station. "
            return_text += "Looks like she doesn't really know anything else, she says. "
            return_text += "Where should we go next? Northern University, the Eastern Commons, Southern Square, or the Western Woods? "
            # Set the location back to Central Station
            context["status"]=["Center","inArea","response"]

        return return_text

    def get_caught(self,context):
        """Returns the text for when the bartender is the thief and gets accused.
            Does the following bookkeeping:
                Notes that the bartender has been removed.
                Brings the user back to central station.
                Starts the first end prompt.
        """

        caught_text = "The detective reaches behind the bar, much to the bartender's chagrin, and pulls a small urn out from under the counter. "
        caught_text += "Somehow, you know the chatbot's voice is in there. I just wanted to bring more business into my bar, the bartender says. "
        caught_text += "With that voice, no one would be able to resist coming here! But before she can say more, the detective leads her off in handcuffs. "
        caught_text += "Nice work, she says, you caught the thief! Any last words for her?"

        # Note the bartender's removal
        context["removed"] = "Bartender"
        # Bring the user back to Central Station
        context["status"]=["Center","inArea","response"]
        # Start the first end prompt (on the next turn). Setting the context["end"] variable to 0 will accomplish this in Game.py.
        context["end"] = 0

        return caught_text

    def repeat(self,text,context):
        return "<prosody rate=\"x-slow\"> "+context["Conversation"][-2]["text"]+"</prosody> "

    def help(self,text,context):

        # Redundant check to see if we need to initialize the Bartender context variables.
        if not "Bartender" in context:
            self.initialize_context_variables(context)
        help_text = ""
        # Help text depends on what the user's done/is doing.
        # If the user hasn't gotten a hint from the bartender yet
        if (context["Bartender"]["hint_given"] == False):
            help_text = "Just talk to her, the detective whispers. It may take her a bit to remember something useful. "
            help_text += "And when you're done, just say, go back, and we'll take our leave. "
        # If the user has gotten at least one hint from the bartender
        else:
            help_text = "Just talk to her, the detective whispers. She might remember something else that could be useful. "
            help_text += "And when you're done, just say, go back, and we'll take our leave. "
        # Additionally, if the user has three or more hints, the detective will remind them of more.
        if (context["hintIndex"]>=2):
            help_text += "By the way, the detective continues, if you want me to read you the hints you've gathered, say, HINT. "
            help_text += "And if you want to accuse the bartender, just say, ACCUSE. "
        return help_text

    def pause(self,text,context):
        """End the conversation and return the user to the entrance of the bar.
            Does the following bookkeeping:
                Brings the user back to the entrance of the bar.
                Resets the conversation turn counter.
                Resets the Bartender's state to 0, the introduction state.
                Sets the hold variable to false.
        """

        # Redundant check if we need to initialize the Bartender context variables.
        if not "Bartender" in context:
            self.initialize_context_variables(context)
        pause_text = "Done talking to her? the detective asks, alright. Let's go. "
        pause_text += "You back away to the entrance of the bar before speaking again. "
        pause_text += "Who do you want to talk to? the detective asks. The drunkard, or the bartender?"

        # Return the user to the entrance of the bar (Eastern Commons main area).
        context["status"]=["East","inArea","response"]
        # Reset the Bartender's conversation turn counter.
        context["Bartender"]["turn_count"] = 0
        # Reset the Bartender's internal state.
        context["Bartender"]["state"] = 0
        return pause_text

    def intro(self,text,context):
        """Function that's called when the NPC is visited for the first time."""

        # Make sure all the context variables for the Bartender are initialized.
        # This puts the state to 0, turn count to 0, hint threshold to the initial threshold,
        # and sets visited, hint_given, and removed to false.
        if not "Bartender" in context:
            self.initialize_context_variables(context)
        # Go to the NPC's response function.
        return self.response(text,context)

    # For Bartender testing, disable when merging up.
