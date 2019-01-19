from serv import tearDown, db
from logic.logic import Article, NewsOutlet, Tweet, TwitterUser
from datetime import datetime
import random

print("tearing down previous db")
tearDown(db)

print("creating db...")
db.create_all()

print("creating news outlet...")
nos = []
for i in range(5):
    nos.append(NewsOutlet(name="news outlet {}".format(i)))

print("creating articles...")
art = []
for i in range(20):
    ar = Article(title="article: {}".format(i), link="http://a{}".format(i), date=datetime.now(), txt_test="èéâïù@|éçî") #èéâïù@|éçî
    art.append(ar)
    db.session.add(ar)

print("adding articles to newsOutlet...")
for a in art:
    random.choice(nos).articles.append(a) # at random
    db.session.add(a)



article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
user_id = db.Column(db.Integer, db.ForeignKey('twitter_user.id'), nullable=False)

tw = Tweet(created_at=datetime.now(), favorite_count=5, retweet_count=54, lang="fr", source="source", text="txt")
db.session.add(tw)

Article.query.first().tweets.append(tw)


twu = TwitterUser(created_at=datetime.now(), name="name", screen_name="screen_name",
                  description="blabla", followers_count=10, favourites_count=100,
                  friends_count=0, statuses_count=0, lang="fr", location="france",
                  url="http://nowere.com", verified=True)

db.session.add(twu)

twu.tweets.append(Tweet.query.all()[0])

print("adding variables to session...")
# db.session.add_all(nos)
# db.session.add_all(art)

print("commiting to db...")
db.session.commit()
