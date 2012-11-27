from google.appengine.ext import db


class Error(db.Model):
    url = db.LinkProperty()
    host = db.LinkProperty()
    error = db.StringProperty(multiline=True)
    filename = db.StringProperty()
    line = db.IntegerProperty()
    useragent = db.StringProperty(multiline=True)
    time = db.DateTimeProperty(auto_now_add=True)
