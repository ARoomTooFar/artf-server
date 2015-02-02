import jinja2
import os
import webapp2

from google.appengine.ext import db

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
JINJA_ENV = jinja2.Environment(loader = jinja2.FileSystemLoader(TEMPLATE_DIR), autoescape = True)

class Level(db.Model):
	uid = db.IntegerProperty(required = True)
	level_name = db.StringProperty(required = True)
	live_level_data = db.TextProperty()
	draft_level_data = db.TextProperty()
	created = db.DateTimeProperty(auto_now_add = True)
	modified = db.DateTimeProperty(auto_now_add = True)

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
		self.write('<html><head><title>ARTF Web</title></head><body>Hello world!</body></html>')

class DisplayDataHand(MainHand):
	def get(self):
		query = Level.all()
		levels = list(query)
		self.render('displaydata.html', levels = levels)

app = webapp2.WSGIApplication([
    ('/', FrontHand),
    ('/display-data', DisplayDataHand)
], debug=True)
