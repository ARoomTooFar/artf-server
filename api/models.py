from google.appengine.ext import db

class Machine(db.Model):
	mach_name = db.StringProperty(required = True)
	venue_name = db.StringProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	modified = db.DateTimeProperty(auto_now = True)

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
	char_name = db.StringProperty(required = True)
	char_data = db.TextProperty()
	game_acct_id = db.IntegerProperty(required = True)
	money = db.IntegerProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	modified = db.DateTimeProperty(auto_now = True)

class Item(db.Model):
	item_num = db.IntegerProperty()
	mod_health = db.IntegerProperty()
	mod_armor = db.IntegerProperty()
	mod_strength = db.IntegerProperty()
	mod_coord = db.IntegerProperty()
	mod_move = db.IntegerProperty()
	mod_luck = db.IntegerProperty()
	char_id = db.IntegerProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	modified = db.DateTimeProperty(auto_now = True)
	# still need to account for storing abilities