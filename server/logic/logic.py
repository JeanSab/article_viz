import json
import collections
from datetime import datetime
from enum import Enum, auto


class NewsOutlet():
    def __init__(self, no, url):
        self.name = no
        self.url = url

class NewsOutletNames(Enum):
    GUARDIAN = auto()
    LEMONDE = auto()
    BFM = auto()
    CNEWS = auto()
    RTL = auto()


class Article():

    def __init__(self, title, link, date, newsOutlet, tweets={}):
        self.title = title
        self.link = link
        self.date = date
        self.newsOutlet = newsOutlet
        self.tweets = tweets


    def __str__(self):
        return ("title: " + self.title + "\nlink: " + self.link + "\ndate: " + str(self.date) + "\ntweet count: " + str(len(self.tweets)))


    @classmethod
    def articleFromFile(cls, fileLoc, nwso):
        with open(fileLoc, "r") as inFile:
            data = json.load(inFile)

        article = cls(data["title"], data["link"], datetime.strptime(data["date"], "%Y-%m-%d %H:%M:%S"), nwso)

        tweets = {}
        for t in data["tweets"]:
            tweets[t["id"]] = Tweet.fromData(t)

        article.tweets = tweets

        return article


class Tweet():

    @classmethod
    def fromData(cls, data):

        f = collections.namedtuple("Tweet", data.keys())
        f.__str__ = lambda s: str(s.text)

        return f(*data.values())
