from serv import tearDown, db
from logic.logic import Article, NewsOutlet, Tweet, TwitterUser
from datetime import datetime
import dateutil.parser
import random
import json
import os
import tarfile


def twitterUserMapper(data):
    key_list = ["id", "name", "screen_name",
                "description", "followers_count", "favourites_count",
                "friends_count", "statuses_count", "lang",
                "location", "url", "verified"]
    user_data = {}
    user_data["created_at"] = datetime.strptime(data["created_at"], "%a %b %d %H:%M:%S %z %Y")
    for key in key_list:
        user_data[key] = data[key]
    return user_data

def tweetMapper(data):
    key_list = ["id", "favorite_count", "retweet_count",
                "lang", "source", "text"]
    tweet_data = {}
    tweet_data["created_at"] = datetime.strptime(data["created_at"], "%a %b %d %H:%M:%S %z %Y")
    for key in key_list:
        tweet_data[key] = data[key]
    return tweet_data



def main():

    DATA_DIR = "./server/data/"
    tearDown(db)
    db.create_all()

    for file_name in os.listdir(DATA_DIR):

        # create news outlet object and add it to session
        news_outlet_name = file_name.replace(".tar.gz", "").replace("_", " ")
        news_outlet = NewsOutlet(name=news_outlet_name)
        db.session.add(news_outlet) # add news outlet to db session

        with tarfile.open(DATA_DIR + file_name) as inFile:
            print("on file: {}".format(file_name))
            members = inFile.getmembers()[1:] # ignore first member
            for m in members:
                fileobj = inFile.extractfile(m) # create file object from tar

                try:
                    data = json.load(fileobj) # data dict
                except json.JSONDecodeError:
                    data = {}
                    data["title"] = m.name
                    data["date"] = None
                    data["link"] = m.name
                    data["tweets"] = []

                print("loaded data from: {}".format(m.name))

                # create article
                try:
                    date = dateutil.parser.parse(data["date"])
                except (ValueError, TypeError):
                    date = None

                title = data["title"]
                if not title:
                    title = data["link"]

                article = Article(title=title, link=data["link"],
                                  date=date) # create article from data
                news_outlet.articles.append(article) # append article to news outlet
                db.session.add(article) # add article to db session

                # create tweets
                i = 0
                for t in data["tweets"]:
                    i += 1
                    tweet = Tweet.query.filter_by(id=t["id"]).first()
                    if tweet is None: # if tweet doesn't exits in db, create it
                        tweet_data = tweetMapper(t)
                        tweet = Tweet(**tweet_data)
                        db.session.add(tweet) # add tweet to db session

                    twitter_user = TwitterUser.query.filter_by(id=t["user"]["id"]).first()
                    if twitter_user is None:
                        user_data = twitterUserMapper(t["user"])
                        twitter_user = TwitterUser(**user_data)
                        db.session.add(twitter_user) # add twitter user to db session

                    twitter_user.tweets.append(tweet)
                    article.tweets.append(tweet)
                print("{} - added {} tweets".format(news_outlet_name, i))


    db.session.commit()




def test():
    print("tearing down preavious db...")
    tearDown(db)
    print("creating db...")
    db.create_all()


    fnames = os.listdir("./server/data/test/")

    with open("./server/data/test/{}".format(fnames[0]), "r") as inFile:
        data = json.load(inFile)

        news_outlet = NewsOutlet(name="lemonde")
        db.session.add(news_outlet)

        try:
            date = datedateutil.parser.parse(data["date"])
        except ValueError:
            date = null

        article = Article(title=data["title"], link=data["link"], date=date)
        news_outlet.articles.append(article)
        db.session.add(article)

        prev_user = TwitterUser(id=308721132)
        db.session.add(prev_user)

        for t in data["tweets"]:
            tweet = Tweet.query.filter_by(id=t["id"]).first()
            if tweet is None:
                tweet_data = tweetMapper(t)
                tweet = Tweet(**tweet_data)
            db.session.add(tweet)

            twitter_user = TwitterUser.query.filter_by(id=t["user"]["id"]).first()
            if twitter_user is None:
                user_data = twitterUserMapper(t["user"])
                twitter_user = TwitterUser(**user_data)
            else:
                print("user with id {} exists".format(twitter_user.id))
            db.session.add(twitter_user)

            twitter_user.tweets.append(tweet)
            article.tweets.append(tweet)
        db.session.commit()



if __name__ == '__main__':
    main()
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
