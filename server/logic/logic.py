import json
import collections
from datetime import datetime
from enum import Enum, auto
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class NewsOutletNames(Enum):
    GUARDIAN = auto()
    LEMONDE = auto()
    BFM = auto()
    CNEWS = auto()
    RTL = auto()


class NewsOutlet(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    articles = db.relationship('Article', backref="news_outlet", lazy=True)


class Article(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    link = db.Column(db.String(100), unique=True, nullable=False)
    date = db.Column(db.DateTime)
    txt_test = db.Column(db.String(10), nullable=False)

    news_outlet_id = db.Column(db.Integer, db.ForeignKey('news_outlet.id'), nullable=False)
    tweets = db.relationship('Tweet', backref="article", lazy=True)

    # def __str__(self):
    #     return ("title: " + self.title + "\nlink: " + self.link + "\ndate: " + str(self.date) + "\ntweet count: " + str(len(self.tweets)))


    # @classmethod
    # def articleFromFile(cls, fileLoc, nwso):
    #     with open(fileLoc, "r") as inFile:
    #         data = json.load(inFile)
    #
    #     article = cls(data["title"], data["link"], datetime.strptime(data["date"], "%Y-%m-%d %H:%M:%S"), nwso)
    #
    #     tweets = {}
    #     for t in data["tweets"]:
    #         tweets[t["id"]] = Tweet.fromData(t)
    #
    #     article.tweets = tweets
    #
    #     return article


class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime)
    favorite_count = db.Column(db.Integer)
    retweet_count = db.Column(db.Integer)
    lang = db.Column(db.String(20))
    source = db.Column(db.String(20))
    text = db.Column(db.String(512))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('twitter_user.id'), nullable=False)



class TwitterUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime)
    name = db.Column(db.String(50))
    screen_name = db.Column(db.String(50))
    description = db.Column(db.String(100))
    followers_count = db.Column(db.Integer)
    favourites_count = db.Column(db.Integer)
    friends_count = db.Column(db.Integer)
    statuses_count = db.Column(db.Integer)
    lang = db.Column(db.String(20))
    location = db.Column(db.String(50))
    url = db.Column(db.String(50))
    verified = db.Column(db.Boolean)
    tweets = db.relationship('Tweet', backref="twitter_user")
