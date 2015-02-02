from google.appengine.ext import db

class Level(db.Model):
	uid = db.IntegerProperty(required = True)
	level_name = db.StringProperty(required = True)
	live_level_data = db.TextProperty()
	draft_level_data = db.TextProperty()
	created = db.DateTimeProperty(auto_now_add = True)
	modified = db.DateTimeProperty(auto_now_add = True)