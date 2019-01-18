from serv import tearDown, db
from logic.logic import Article, NewsOutlet
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
    art.append(Article(title="article: {}".format(i), link="http://a{}".format(i), date=datetime.now(), txt_test="èéâïù@|éçî")) #èéâïù@|éçî

print("adding articles to newsOutlet...")
for a in art:
    random.choice(nos).articles.append(a) # at random

print("adding variables to session...")
db.session.add_all(nos)
db.session.add_all(art)

print("commiting to db...")
db.session.commit()
