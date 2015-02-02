#!/usr/bin/env python
import datetime
import jinja2
import logging
import os
import webapp2

from models import Level

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
		self.write('<html><head><title>ARTF API</title></head><body>ARTF API 0.0.2</body></html>')

class LevelsHand(MainHand):
	def post(self):
		uid_str = self.request.get('user_id')
		level_name = self.request.get('level_name')
		live_level_data = self.request.get('live_level_data')
		draft_level_data = self.request.get('draft_level_data')
		
		uid = int(uid_str) #need to check if non-int is input later
		
		if uid and level_name:
			new_level = Level(uid = uid, level_name = level_name, live_level_data = live_level_data, draft_level_data = draft_level_data)
			new_level.put()
			self.write(new_level.key().id())
		else:
			logging.error('Missing required properties: uid or level_name')
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
		lid_str = self.request.get('level_id')
		uid_str = self.request.get('user_id')
		level_name = self.request.get('level_name')
		live_level_data = self.request.get('live_level_data')
		draft_level_data = self.request.get('draft_level_data')

		beginning_path_len = 8 #the length of the string '/levels/'
		total_path_len = len(self.request.path)
		lid = int(self.request.path[beginning_path_len:total_path_len])

		query = Level.get_by_id(lid)
		if(query == None):
			logging.error('Level does not exist')
			self.abort(404)

		if(flag == 'update'):
			if(uid_str != ''):
				query.uid = int(uid_str)
			if(level_name != ''):
				query.level_name = level_name
			if(live_level_data != ''):
				query.live_level_data = live_level_data
			if(draft_level_data != ''):
				query.draft_level_data = draft_level_data
			query.put()
			self.write(query.key().id())
		else:
			logging.error('No flag set')
			self.abort(404)

class DSConnHand(MainHand):
	def get(self):
		query = Level.all()
		levels = list(query)
		self.render('dsconn.html', levels = levels)

app = webapp2.WSGIApplication([
    ('/?', FrontHand),
    ('/levels/?', LevelsHand),
    ('/levels/([^/]+)?', LevelsIdHand),
    ('/dsconn', DSConnHand)
], debug=True)
