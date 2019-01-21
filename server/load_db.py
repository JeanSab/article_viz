from serv import tearDown, db
from logic.logic import Article, NewsOutlet, Tweet, TwitterUser
from datetime import datetime
import random
import json
import os


def main():
    print("main")


def test():
    print("tearing down preavious db...")
    tearDown(db)
    print("creating db...")
    db.create_all()

    fnames = os.listdir("./server/data/")
    with open("./server/data/{}".format(fnames[0]), "r") as inFile:
        data = json.load(inFile)

        news_outlet = NewsOutlet(name="lemonde")
        db.session.add(news_outlet)

        article = Article(title=data["title"], link=data["link"], date=datetime.strptime(data["date"], "%Y-%m-%d %H:%M:%S"))
        news_outlet.articles.append(article)
        db.session.add(article)

        for t in data["tweets"]:
            tweet = Tweet.query.filter_by(id=t["id"]).first()
            if tweet is None:
                created_at = datetime.strptime(t["created_at"], "%a %b %d %H:%M:%S %z %Y")
                tweet = Tweet(id=t["id"], created_at=created_at, favorite_count=t["favorite_count"],
                              retweet_count=t["retweet_count"], lang=t["lang"],
                              source=t["source"], text=t["text"])
            db.session.add(tweet)

            twitter_user = TwitterUser.query.filter_by(id=t["user"]["id"]).first()
            if twitter_user is None:
                created_at = datetime.strptime(t["user"]["created_at"], "%a %b %d %H:%M:%S %z %Y")
                tw=t["user"]
                twitter_user = TwitterUser(id=tw["id"], created_at=created_at, name=tw["name"],
                                           screen_name=tw["screen_name"], description=tw["description"],
                                           followers_count=tw["followers_count"], favourites_count=tw["favourites_count"],
                                           friends_count=tw["friends_count"], statuses_count=tw["statuses_count"],
                                           lang=tw["lang"], location=tw["location"], url=tw["url"], verified=tw["verified"])

            db.session.add(twitter_user)

            twitter_user.tweets.append(tweet)
            article.tweets.append(tweet)
        db.session.commit()






if __name__ == '__main__':
    test()
# for each News Outlet rep
#   create NewsOutlet and add to db session
#   for each file in rep
#       create news article and add to db session
#           for each news article
#               create tweets and add to db session
#               for each tweets
#                   if user not in db session
#                      create user
#                 else
#                      get user from db
#
#                 add tweet to user
#                 add tweet to article
#               add article to news Outlet
#
# commit sessio to db
