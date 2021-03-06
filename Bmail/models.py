from google.appengine.ext import ndb

class Email(ndb.Model):
    sender = ndb.StringProperty()
    receiver = ndb.StringProperty()
    subject = ndb.StringProperty()
    email = ndb.TextProperty()
    time = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)