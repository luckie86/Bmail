from google.appengine.ext import ndb

class Email(ndb.Model):
    sender = ndb.StringProperty()
    receiver = ndb.StringProperty()
    subject = ndb.StringProperty()
    email = ndb.TextProperty()
    time = ndb.DateTimeProperty(auto_now_add=True)

class User(ndb.Model):
    name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    user_name = ndb.StringProperty()
    email = ndb.StringProperty()
    password = ndb.StringProperty()
