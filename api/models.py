from google.appengine.ext import db

class Level(db.Model):
	live_level_data = db.TextProperty()
	draft_level_data = db.TextProperty()
	game_acct_id = db.IntegerProperty(required = True)
	mach_id = db.IntegerProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	modified = db.DateTimeProperty(auto_now = True)

class GameAccount(db.Model):
	game_acct_name = db.StringProperty(required = True)
	game_acct_password = db.StringProperty(required = True)
	web_acct_id = db.IntegerProperty()
	created = db.DateTimeProperty(auto_now_add = True)
	modified = db.DateTimeProperty(auto_now = True)

class Character(db.Model):
	char_data = db.TextProperty(required = True)
	game_acct_id = db.IntegerProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	modified = db.DateTimeProperty(auto_now = True)

class Machine(db.Model):
	mach_name = db.StringProperty(required = True)
	venue_name = db.StringProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	modified = db.DateTimeProperty(auto_now = True)
