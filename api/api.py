#!/usr/bin/env python
import datetime
import jinja2
import logging
import os
import webapp2

from google.appengine.ext import db
from models import Level, GameAccount, Character, Machine

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
JINJA_ENV = jinja2.Environment(loader = jinja2.FileSystemLoader(TEMPLATE_DIR), autoescape = True)

class MainHand(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.write(*a, **kw)

	def render_str(self, template, **params):
		t = JINJA_ENV.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class FrontHand(MainHand):
	def get(self):
		self.write('<html><head><title>ARTF API</title></head><body>ARTF API 0.0.3</body></html>')

class LevelsHand(MainHand):
	def post(self):
		live_level_data = self.request.get('live_level_data')
		draft_level_data = self.request.get('draft_level_data')
		game_acct_id_str = self.request.get('game_acct_id')
		mach_id_str = self.request.get('mach_id')
		
		game_acct_id = int(game_acct_id_str)
		mach_id = int(mach_id_str)
		
		if game_acct_id and mach_id:
			new_level = Level(live_level_data=live_level_data, draft_level_data=draft_level_data, game_acct_id=game_acct_id, mach_id=mach_id)
			new_level.put()
			self.write(new_level.key().id())
		else:
			logging.error('Missing required properties: game_acct_id or mach_id')
			self.abort(404)

class LevelsIdHand(MainHand):
	def get(self, levelId):
		beginning_path_len = 8 #the length of the string '/levels/'
		total_path_len = len(self.request.path)
		lid = int(self.request.path[beginning_path_len:total_path_len])
		query = Level.get_by_id(lid)

		if(query == None):
			logging.error('Level does not exist')
			self.abort(404)
		else:
			self.write(query.live_level_data)

	def post(self, levelId):
		flag = self.request.get('flag')
		game_acct_id_str = self.request.get('game_acct_id')
		live_level_data = self.request.get('live_level_data')
		draft_level_data = self.request.get('draft_level_data')

		# Get level ID from end of URL path
		beginning_path_len = 8 #the length of the string '/levels/'
		total_path_len = len(self.request.path)
		level_id = int(self.request.path[beginning_path_len:total_path_len])

		query = Level.get_by_id(level_id)
		if(query == None):
			logging.error('Level does not exist')
			self.abort(404)
		else:
			if(flag == 'update'):
				if(game_acct_id_str != ''):
					query.game_acct_id = int(game_acct_id_str)
				if(live_level_data != ''):
					query.live_level_data = live_level_data
				if(draft_level_data != ''):
					query.draft_level_data = draft_level_data
				query.put()
				self.write(query.key().id())
			elif(flag == 'delete'):
				query.delete()
				self.write(query.key().id())
				logging.info('Level ' + str(level_id) + ' deleted')
			else:
				logging.error('No flag set')
				self.abort(404)

class LoginHand(MainHand):
	def post(self):
		input_game_acct_name = self.request.get('game_acct_name')
		input_game_acct_password = self.request.get('game_acct_password')

		entity = db.GqlQuery('SELECT * FROM GameAccount WHERE game_acct_name = :1', input_game_acct_name).get()
		
		if(input_game_acct_password == entity.game_acct_password):
			self.write('LOGIN SUCCESS')
		else:
			self.write('')

class RegisterHand(MainHand):
	def post(self):
		input_game_acct_name = self.request.get('game_acct_name')
		input_game_acct_password = self.request.get('game_acct_password')
		input_char_data = self.request.get('char_data')

		query = db.GqlQuery('SELECT * FROM GameAccount WHERE game_acct_name = :1', input_game_acct_name)

		if(query.count() == 0):
			new_game_acct = GameAccount(game_acct_name=input_game_acct_name, game_acct_password=input_game_acct_password)
			new_game_acct.put()

			game_acct_id = new_game_acct.key().id()

			new_char = Character(char_data=input_char_data, game_acct_id=game_acct_id)
			new_char.put()

			self.write(game_acct_id)
			logging.info('Game account ' + str(game_acct_id) + ' created')
		else:
			logging.error('game_acct_name already exists')
        	self.write('')

class MachineHand(MainHand):
	def post(self):
		input_mach_name = self.request.get('mach_name')
		input_venue_name = self.request.get('venue_name')

		new_mach = Machine(mach_name=input_mach_name, venue_name=input_venue_name)
		new_mach.put()

		mach_id = new_mach.key().id()

		self.write(mach_id)
		logging.info('Machine ' + str(mach_id) + ' created')

class DSConnHand(MainHand):
	def get(self):
		query = Level.all()
		levels = list(query)
		self.render('dsconn.html', levels = levels)

class UploadTestHand(MainHand):
	def get(self):
		self.render('uploadtest.html')

app = webapp2.WSGIApplication([
    ('/?', FrontHand),
    ('/levels/?', LevelsHand),
    ('/levels/([^/]+)?', LevelsIdHand),
    ('/gameaccount/login/?', LoginHand),
    ('/gameaccount/register/?', RegisterHand),
    ('/machine/?', MachineHand),
    ('/dsconn', DSConnHand),
    ('/uploadtest', UploadTestHand)
], debug=True)
