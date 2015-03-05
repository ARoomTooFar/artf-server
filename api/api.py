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

        if(game_acct_id_str.isdigit() and mach_id_str.isdigit()):
            game_acct_id = int(game_acct_id_str)
            mach_id = int(mach_id_str)

            if game_acct_id and mach_id:
                new_level = Level(live_level_data=live_level_data, draft_level_data=draft_level_data, game_acct_id=game_acct_id, mach_id=mach_id)
                new_level.put()

                new_level_id = str(new_level.key().id())
                self.write(new_level_id)
                logging.info('Level ' + new_level_id + ' created')
            else:
                logging.error('Level upload failed. game_acct_id or mach_id cannot be 0.')
                self.abort(404)
        else:
            logging.error('Level upload failed. game_acct_id and mach_id must be numbers.')
            self.abort(404)

class LevelsIdHand(MainHand):
    def get(self, levelId):
        beginning_path_len = 8 #the length of the string '/levels/'
        total_path_len = len(self.request.path)
        level_id = int(self.request.path[beginning_path_len:total_path_len]) #must be cast to int for query
        entity = Level.get_by_id(level_id)
        level_id = str(level_id) #must be cast to str for logging

        if(entity == None):
            logging.error('Level download failed. Level ' + level_id + ' does not exist in Datastore.')
            self.abort(404)
        else:
            self.write(entity.live_level_data)
            logging.info('Level ' + level_id  + ' downloaded')

    def post(self, levelId):
        flag = self.request.get('flag')
        game_acct_id_str = self.request.get('game_acct_id')
        live_level_data = self.request.get('live_level_data')
        draft_level_data = self.request.get('draft_level_data')

        # Get level ID from end of URL path
        beginning_path_len = 8 #the length of the string '/levels/'
        total_path_len = len(self.request.path)
        level_id = int(self.request.path[beginning_path_len:total_path_len]) #must be cast to int for query

        entity = Level.get_by_id(level_id)
        if(entity == None):
            logging.error('Level manipulation failed. Level does not exist in Datastore.')
            self.abort(404)
        else:
            level_id = str(level_id) #must be cast to str for logging
            if(flag == 'update'):
                if(game_acct_id_str != ''):
                    entity.game_acct_id = int(game_acct_id_str)
                if(live_level_data != ''):
                    entity.live_level_data = live_level_data
                if(draft_level_data != ''):
                    entity.draft_level_data = draft_level_data
                entity.put()
                self.write(level_id)
                logging.info('Level ' + level_id + ' updated')
            elif(flag == 'delete'):
                entity.delete()
                self.write(level_id)
                logging.info('Level ' + level_id + ' deleted')
            else:
                logging.error('Level manipulation failed. No manipulation flag set.')
                self.abort(404)

class GameLoginHand(MainHand):
    def post(self):
        input_game_acct_name = self.request.get('game_acct_name')
        input_game_acct_password = self.request.get('game_acct_password')

        entity = db.GqlQuery('SELECT * FROM GameAccount WHERE game_acct_name = :1', input_game_acct_name).get()

        if(entity != None):
            game_acct_id = str(entity.key().id())

            if(input_game_acct_password == entity.game_acct_password):
                entity = db.GqlQuery('SELECT * FROM Character WHERE game_acct_id = :1', int(game_acct_id)).get()

                if(entity == None):
                    logging.error('Character download for game account ' + game_acct_id +' failed. Character doesn\'t exist for game account.')
                    self.write('')
                else:
                    self.write(entity.char_data)
                    logging.info('Game account ' + game_acct_id + ' logged in') #post location and maybe account name later
            else:
                self.write('')
                logging.info('Login failed for game account ' + game_acct_id + '. Password incorrect.')
        else:
            self.write('')
            logging.info('Login failed for game account ' + input_game_acct_name + '. game_acct_name doesn\'t exist.')

class GameRegisterHand(MainHand):
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

            game_acct_id = str(game_acct_id) #must be cast to str for logging
            self.write(game_acct_id)
            logging.info('Game account ' + game_acct_id + ' created')
        else:
            logging.error('Registration failed for ' + input_game_acct_name + '. game_acct_name already exists.')
            self.write('')

class MachineHand(MainHand):
    def post(self):
        input_mach_name = self.request.get('mach_name')
        input_venue_name = self.request.get('venue_name')

        new_mach = Machine(mach_name=input_mach_name, venue_name=input_venue_name)
        new_mach.put()

        mach_id = str(new_mach.key().id())

        self.write(mach_id)
        logging.info('Machine ' + mach_id + ' created')

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
    ('/gameaccount/login/?', GameLoginHand),
    ('/gameaccount/register/?', GameRegisterHand),
    ('/machine/?', MachineHand),
    ('/dsconn', DSConnHand),
    ('/uploadtest', UploadTestHand)
], debug=True)
