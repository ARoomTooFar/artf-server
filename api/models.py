from google.appengine.ext import db

class Machine(db.Model):
	mach_name = db.StringProperty(required = True)
	venue_name = db.StringProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	modified = db.DateTimeProperty(auto_now_add = True)

class Level(db.Model):
	live_level_data = db.TextProperty()
	draft_level_data = db.TextProperty()
	level_name = db.StringProperty(required = True)
	user_id = db.IntegerProperty(required = True)
	mach_id = db.IntegerProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	modified = db.DateTimeProperty(auto_now_add = True)

class Account(db.Model):
	acct_name = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	modified = db.DateTimeProperty(auto_now_add = True)

class Character(db.Model):
	char_name = db.StringProperty(required = True)
	char_data = db.TextProperty()
	acct_id = db.IntegerProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	modified = db.DateTimeProperty(auto_now_add = True)

class Item(db.Model):
	mod_health = db.IntegerProperty()
	mod_armor = db.IntegerProperty()
	mod_strength = db.IntegerProperty()
	mod_coord = db.IntegerProperty()
	mod_move = db.IntegerProperty()
	mod_luck = db.IntegerProperty()
	char_id = db.IntegerProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	modified = db.DateTimeProperty(auto_now_add = True)
	# still need to account for storing abilities