import json
from datetime import datetime
import newsOutlet


class NewsOutlet():

    def __init__(self, name, url):
        self.name = name
        self.url = url


class Article():

    def __init__(self, title, link, date, newsOutlet, tweets={}):
        self.title = title
        self.link = link
        self.date = date
        self.newsOutlet = newsOutlet

        self.tweets = tweets


    @classmethod
    def loadFromFile(cls, fileLoc):
        with open(fileLoc, "r") as inFile:
            data = json.load(inFile)

        article = cls(data["title"], data["link"], datetime.strptime(data["date"], "%Y-%m-%d"), newsOutlet.newsOutlet(""))

        tweets = {}
        for t in data["tweets"]
            tweets[d["id"]] = t
