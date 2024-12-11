# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1


class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

#     Getters
    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2


class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower()

    def is_phrase_in(self, text):
        text_edited = ''
        for char in text:
            if char not in string.punctuation:
                text_edited += char
            else:
                text_edited += ' '
        text_list = text_edited.split()
        phrase_list = self.phrase.split()
        check_list = []
        for word in phrase_list:
            if word in text_list:
                check_list.append(text_list.index(word))
        for i in range(1, len(check_list)):
            if check_list[i] < check_list[i-1] or abs(check_list[i] - check_list[i-1] > 1):
                return False
        return len(check_list) == len(phrase_list)


# Problem 3
class TitleTrigger(PhraseTrigger):

    def evaluate(self, title):
        return self.is_phrase_in(title.get_title().lower())


# Problem 4
class DescriptionTrigger(PhraseTrigger):

    def evaluate(self, description):
        return self.is_phrase_in(description.get_description().lower())

# TIME TRIGGERS

# Problem 5
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.


class TimeTrigger(Trigger):
    def __init__(self, est_time):
        time_formatted = datetime.strptime(est_time, "%d %b %Y %H:%M:%S")
        time_formatted = time_formatted.replace(tzinfo=pytz.timezone("EST"))
        self.time = time_formatted


# Problem 6
class BeforeTrigger(TimeTrigger):
    def evaluate(self, fire_time):
        return self.time > fire_time.get_pubdate()


class AfterTrigger(TimeTrigger):
    def evaluate(self, fire_time):
        return self.time < fire_time.get_pubdate()

# COMPOSITE TRIGGERS


# Problem 7
class NotTrigger(Trigger):
    def __init__(self, trigger_class):
        self.trigger_class = trigger_class

    def evaluate(self, argument):
        return not self.trigger_class.evaluate(argument)
# Problem 8


class AndTrigger(Trigger):
    def __init__(self, trigger_class1, trigger_class2):
        self.trigger_class1 = trigger_class1
        self.trigger_class2 = trigger_class2

    def evaluate(self, argument):
        return self.trigger_class1.evaluate(argument) and self.trigger_class2.evaluate(argument)


# Problem 9
class OrTrigger(Trigger):
    def __init__(self, trigger_class1, trigger_class2):
        self.trigger_class1 = trigger_class1
        self.trigger_class2 = trigger_class2

    def evaluate(self, argument):
        return self.trigger_class1.evaluate(argument) or self.trigger_class2.evaluate(argument)


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    stories_new = []
    stories_new = [story for story in stories for trigger in triggerlist
                   if trigger.evaluate(story) and story not in stories_new]
    stories = stories_new
    return stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    trigger_type = {'TITLE': TitleTrigger,
                    'DESCRIPTION': DescriptionTrigger,
                    'AFTER': AfterTrigger,
                    'BEFORE': BeforeTrigger,
                    'NOT': NotTrigger,
                    'AND': AndTrigger,
                    'OR': OrTrigger}
    lines_final = []
    trigger_dict = {}
    for line in lines:
        current_line = line.split(',')
        if current_line[0] != 'ADD':
            if current_line[1] == 'AND' or current_line[1] == 'OR':
                trigger_dict[current_line[0]] = (trigger_type[current_line[1]]
                                                 (trigger_dict[current_line[2]], trigger_dict[current_line[3]]))
            else:
                trigger_dict[current_line[0]] = trigger_type[current_line[1]](current_line[2])
        else:
            for i in current_line[1:]:
                lines_final.append(trigger_dict[i])
    return lines_final



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Israel")
        t3 = DescriptionTrigger("Palestine")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            # stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

