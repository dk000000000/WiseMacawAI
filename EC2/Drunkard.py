from chitchat import chitchat
class Drunkard:
    def __init__(self):
        self.module = chitchat()

    def response(self, text, context):
        if context["DrunkardCount"]==8:
            context["Drunkard"]=2
        if context["Drunkard"]==0:
            context["Drunkard"]=1
            return "You approach the drunkard, who still takes a bit too long to notice you. Why all oh again, he mumbles, balancing precariously on his bar stool. Go on, whispers the detective, say something to him. Maybe if you two talk long enough, he'll  remember something useful. And when you're done talking, just say, go back."
        elif context["Drunkard"]==1:
            context["DrunkardCount"]+=1
            return self.module.response(text,context)
        elif context["Drunkard"]==2:
            context["status"]=["Center","inArea","response"]
            context["hintIndex"]+=1
            context["DrunkardCount"]=0
            context["Drunkard"]=0
            context["givehint"]=True
            if context["hintIndex"]>=len(context["hints"]):
                return " That's all I know about chatbot. we can still chat "
            return " Oh, hey, you know the chatbot's voice? the drunkard says with unusual coherence. I heard a little something about that. %s. The detective quickly jots it down in her notebook, then hurries you back to Central Station. You worked that drunkard over well, she says. " % context["hints"][context["hintIndex"]]

    def repeat(self,text,context):
        return "<prosody rate=\"x-slow\"> "+context["Conversation"][-2]["text"]+"</prosody> "

    def help(self,text,context):
        help_text = "Say whatever you like to him, the detective whispers. Maybe if you two talk long enough, he'll remember something useful. And when you're done, just say, go back, and we'll take our leave of him."
        if context["hintIndex"]>=2:
            help_text += "By the way, the detective continues, if you want me to read you the hints you've gathered, say, HINT. And if you want to accuse the drunkard, just say, ACCUSE."
        return help_text

    def get_caught(self,context):
        context["removed"] = "Drunkard"
        # Bring the user back to Central Station
        context["status"]=["Center","inArea","response"]
        # Start the first end prompt (on the next turn). Setting the context["end"] variable to 0 will accomplish this in Game.py.
        context["end"] = 0
        return "The detective pats the drunkard down and pulls a small urn out from under his sport jacket. Somehow, you know the chatbot's voice is in there. I just wanted to look at it, the drunkard says sheepishly. If I used that voice, I'd never have to pay for drinks again. But before he can say more, the detective leads him off in handcuffs. Nice work, she says, you caught the thief! Any last words for him?"

    def pause(self,text,context):
        pause_text = "Had enough of him? says the detective, me too. Let's go. You back away to the entrance of the bar before speaking again. Who do you want to talk to? the detective asks. The drunkard, or the bartender?"
        # Return the user to the entrance of the bar (Eastern Commons main area).
        context["status"]=["East","inArea","response"]
        # Reset the Bartender's conversation turn counter.
        context["DrunkardCount"] = 0
        # Reset the Bartender's internal state.
        context["Drunkard"] = 0
        return pause_text

    def intro(self,text,context):
        context["Drunkard"]=1
        context["DrunkardCount"]=0
        return "You approach the drunkard, who takes a bit too long to register that you're there. Well hello! he manages, but oddly, he doesn't continue. Go on, whispers the detective, say something to him. Maybe if you two talk long enough, he'll  remember something useful. And when you're done talking, just say, go back."
