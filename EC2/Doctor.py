from search import search
from easyQA import easyQA
from module import module
class Doctor(module):
    def __init__(self):
        self.search = search()
        self.easyQA = easyQA()
        self.complaints = [
        "Doing PHD is hard work, but I always procrastinate. ",
        "I hope I would become professor one day. ",
        "Science and technology is the most importanat things in my life, I need work harder. ",
        "weather is bad, I made no progress for four years, maybe I'm stupid and should quit PHD and find a job? ",
        "those undergrade came up with all kind of weird reason to not hand in homework, and I have to spend weekends to grade them. ",
        ]
        self.easyQAPrompts = [
        "I think this might be useful to you, ",
        "I know this, "
        ]
        self.randomPrompts = [
        "It's easy, let me find that for you. ",
        "I'm kind of busy, let me search that for you. ",
        ]
        self.threshold = 5
    def response(self,text,context):
        if context["DoctorCount"]>=self.threshold:
            context["Doctor"]=3

        if context["Doctor"]==0:
            if context["removed"]!="EMPTY":
                return "You find your way to the Doctor's office. Welcome back, he says, standing as you enter. I've already told you what I know, but I can still answer questions for you. What do you say? Yes, or no?"
            else:
                return "You find your way to the Doctor's office. Welcome back, he says, standing as you enter. I'm still working on my question answering skills. Help me practice, and I'll tell you what I know. What do you say? Yes, or no?"
        elif context["Doctor"]==1:
            if "yes" in text.lower() or context["intent"]=="AMAZON.YesIntent" or context["intent"]=="AMAZON.ResumeIntent":
                context["Doctor"]=2
                return "Wonderful, the Doctor says, settling into his chair. Please, try to keep your questions to general knowledge. I may not very specific things. Now then, ask away."
            elif "no" in text.lower() or context["intent"]=="AMAZON.NoIntent":
                context["status"]=["North","inArea","response"]
                return "Very well, the Doctor says, taking out his pen and continuing his work. If you change your mind, my door is open to you. You find yourself back at the University entrance. The detective turns to you. So, who should we talk to? she asks, The Librarian, or the Doctor? If you think we should check somewhere else, just tell me a direction and we'll go there."
            else:
                return "The Doctor stares blankly at you. My apologies, he says, I don't quite understand. Yes, you'd like to ask me questions, or no, you do not?"
        elif context["Doctor"]==2:
            context["DoctorCount"]+=1
            try:
                response = "OK, "+ self.easyQA.response(text,context)
            # If there is no QA response, get the response for search
            except Exception as ex:
                print ("No templated response or ask question response. Returning search response. Exception: " + str(ex))
                response = "Well, Search Engine says "+ self.search.response(text,context)
            return response
        elif context["Doctor"]==3:
            context["Doctor"]=0
            context["DoctorCount"] = 0
            if context["hintIndex"]>=len(context["hints"]):
                response = "Turns out, a chatbot's voice is pretty powerful. I don't really understand it all, but it really shouldn't be tampered with."
            else:
                context["status"]=["Center","inArea","response"]
                context["hintIndex"]+=1
                context["givehint"]=True
                response = "I think that's quite enough practice, the Doctor says, I thank you for your time. Now, I do believe I owe you some information, don't I? Well, here it is. %s. The detective quickly jots it down in her notebook, then hurries you back to Central Station. Good job with that know it all, she says." % context["hints"][context["hintIndex"]]
            return response

    def get_caught(self,context):
        """Returns the text for when the bartender is the thief and gets accused.
            Does the following bookkeeping:
                Notes that the bartender has been removed.
                Brings the user back to central station.
                Starts the first end prompt.
        """

        caught_text = "The detective searches his desk and finds a small urn. Somehow, you know the chatbot's voice is in there. The Doctor sighs and allows the detective to cuff him. Do you even know what that voice can do? he asks. With it, I could have stolen the answer to any and every question imaginable. I could have known everything, while the rest of the world knew nothing! But before he can say more, the detective leads him off in handcuffs. Nice work, she says, you caught the thief! Any last words for him?"

        # Note the removal
        context["removed"] = "Doctor"
        # Bring the user back to Central Station
        context["status"]=["Center","inArea","response"]
        # Start the first end prompt (on the next turn). Setting the context["end"] variable to 0 will accomplish this in Game.py.
        context["end"] = 0

        return caught_text

    def repeat(self,text,context):
        return "<prosody rate=\"x-slow\"> "+context["Conversation"][-2]["text"]+"</prosody> ."

    def help(self,text,context):
        if context["Doctor"]==1:
            help_text = "Sounds like he wants to know if you want to ask him some questions, the detective whispers. Just say yes or no."
        elif context["Doctor"]==2:
            help_text = "He wants you to ask him a question, the detective whispers."
        if context["hintIndex"]>=2:
            help_text += "By the way, the detective continues, if you want me to read you the hints you've gathered, say, HINT. And if you want to accuse The Doctor, just say, ACCUSE."
        return help_text

    def pause(self,text,context):
        pause_text = "Very well, the Doctor says, taking out his pen and continuing his work. If you change your mind, my door is open to you. You find yourself back at the University entrance. The detective turns to you. So, who should we talk to? she asks, The Librarian, or the Doctor? If you think we should check somewhere else, just tell me a direction and we'll go there."

        # Return the user to the entrance of the bar (Eastern Commons main area).
        context["status"]=["North","inArea","response"]
        # Reset the Bartender's conversation turn counter.
        context["DoctorCount"] = 0
        # Reset the Bartender's internal state.
        context["Doctor"] = 0

        return pause_text

    def intro(self,text,context):
        context["Doctor"]=1
        context["DoctorCount"]=0
        return "You find your way through the twisting halls of the University to a certain office. An older gentleman with curly, grey hair greets you, tucking a fountain pen into his lapel. Nice to meet you, he says. I'm the Doctor. Someone told me you were looking for the chatbot's voice? Well, as it just so happens, I need practice answering questions for one of my classes. Help me practice, and I'll tell you what I know. What do you say? Yes, or no?"
