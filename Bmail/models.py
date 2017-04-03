from google.appengine.ext import ndb

class Email(ndb.Model):
    sender = ndb.StringProperty()
    receiver = ndb.StringProperty()
    subject = ndb.StringProperty()
    email = ndb.TextProperty()
#sent = ndb.BooleanProperty()
#received = ndb.BooleanProperty()
    time = ndb.DateTimeProperty(auto_now_add=True)

class User(ndb.Model):
    name = ndb.StringProperty()
    lastname = ndb.StringProperty()
    username = ndb.StringProperty()
    email = ndb.StringProperty()
    password = ndb.StringProperty()
