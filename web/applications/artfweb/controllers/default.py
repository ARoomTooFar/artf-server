# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################

#from google.appengine.ext import db
#from google.appengine.ext.db import GqlQuery
#db = GQLDB()
import logging

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to web2py!")

    if auth.user:
        msg = A('Workshop', _class='btn', _href=URL('default', 'workshop'))
    else:
        msg = "Please login or register to edit your level!";

    return dict(inWorkshop=False)

def media():
    return dict(display_title= 'Media')

def locations():
    return dict(display_title= 'Locations')

def blog():
    #form = SQLFORM(db.blog)
    #form.add_button('Add', URL('add'))
    posts = db().select(db.blog.ALL, orderby = ~db.blog.date_posted)

    #return  dict(form=form)
    return dict(posts=posts)

@auth.requires_login()
def add():
    #form = SQLFORM(db.blog)
    form = SQLFORM.factory(
        Field('post_title', 'string', requires=IS_NOT_EMPTY(error_message='Field is empty !'), label='Title'),
        Field('authour', 'string', requires=IS_NOT_EMPTY(error_message='Field is empty !'), label='Authour'),
        Field('date_posted', 'datetime', label='Date Posted'),
        Field('postbody', 'text', requires=IS_NOT_EMPTY(error_message='Field is empty !'), label='Body')
    )

    if form.process().accepted:
        db.blog.insert(**form.vars)
        response.flash = T('Announcement posted')
        redirect(URL('default','blog'))

    return dict(form=form)

def view():
    p = db.blog(request.args(0)) or redirect(URL('default', 'index'))
    form = SQLFORM(db.blog,readonly=True)
    return dict(form=form)


def dbtest():
    q = db().select(db.Level.ALL)
    #levels = db.GqlQuery("SELECT * FROM Level ORDER BY created DESC")
    #personresults = db(Level).select(db.Level.level_name)

    return dict(display_title='DB Test', q=q)

def dbinput():
    form = SQLFORM(db.Level)

    if form.process().accepted:
        session.flash = T('Level added')
        redirect(URL('default', 'dbinput'))

    return dict(display_title='DB Input', form=form)

@auth.requires_login()
def workshop():
    btnLevels = None
    btnAddLevel = None
    levelsList = None
    form = None
    ids = '0'
    levelData = None

    # /workshop
    if request.args(0) is None:
        redirect(URL('default', 'workshop', args=['zones']))
    
    elif request.args(0) == 'zones':

        # /workshop/zones/[LEVELID]/webgl
        if str(request.args(1)).isdigit() and request.args(2) == 'webgl':
            ids = str(auth.user.game_acct_id) + ',' + request.args(1)

            # get level data for debugging purposes
            entity = db(db.Level.id == request.args(1)).select().first()
            levelData = entity.live_level_data

            response.view = request.controller + '/zoneeditor-webgl.html'
            return dict(ids=ids, levelData=levelData)

        # /workshop/zones/[LEVELID]/del
        if str(request.args(1)).isdigit() and request.args(2) == 'del':
            page_title = 'Delete Zone'

            btnLevels = A('Your Zones', _class='btn', _href=URL('default', 'workshop', args=['zones']))
            form = FORM.confirm('Are you sure you want to delete your level?')

            if form.accepted:
                db(db.Level.id == request.args(1)).delete()
                session.flash = T('Level ' + str(request.args(1)) + ' deleted')
                redirect(URL('default', 'workshop', args=['zones']))

        # /workshop/zones/[LEVELID]
        # need to add in security here later so people can't edit other people's levels
        elif str(request.args(1)).isdigit():
            ids = str(auth.user.game_acct_id) + ',' + request.args(1)

            # get level data for debugging purposes
            entity = db(db.Level.id == request.args(1)).select().first()
            levelData = entity.live_level_data

            response.view = request.controller + '/zoneeditor.html'
            return dict(ids=ids, levelData=levelData)

        # /workshop/zones/add
        elif request.args(1) == 'add':
            response.view = request.controller + '/zoneadd.html'
            page_title = 'Create Zone'

            form = FORM.confirm('Do you want to create a new level?')

            if form.accepted:
                levelId = db.Level.insert(live_level_data='farts', draft_level_data='farts', game_acct_id=auth.user.game_acct_id, mach_id=123)
                session.flash = T('New level ' + str(levelId) + ' created!')
                redirect(URL('default', 'workshop', args=['zones']))

            return dict(form=form)

        # /workshop/zones
        else:
            response.view = request.controller + '/zonelist.html'
            page_title = 'Your Zones'

            query = db(db.Level.game_acct_id == auth.user.game_acct_id).select()

            levelsList = []

            for entity in query:
                levelsList.append({'id': entity.id, 'live_level_data': entity.live_level_data})

            return dict(levelsList=levelsList)

    return dict()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """

    if 'register' in request.args:
        field_game_acct_id = db.auth_user['game_acct_id']
        field_game_acct_id.readable = False
        field_game_acct_id.writable = False

    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def api():
    data = 'error'

    # /api/levels
    if request.args(0) == 'levels':
        if request.args(1) != None and request.args(1).isdigit():
            level_id = request.args(1)

            # download level (/api/levels/[LEVELID])
            if(request.env.request_method == 'GET'):
                entity = db(db.Level.id == level_id).select().first()

                # if the level exists in the data store, print its data
                if entity is not None:
                    data = entity.live_level_data
                    logging.info('Level ' + level_id  + ' downloaded')
                else:
                    logging.error('Level download failed. Level ' + level_id + ' does not exist in Datastore.')

            # update level (/api/levels/[LEVELID])
            elif(request.env.request_method == 'POST'):
                entity = db(db.Level.id == level_id).select().first()

                # if the level exists in the data store, update its data
                if entity is not None:
                    entity.update_record(draft_level_data = request.post_vars['draft_level_data'], game_acct_id = request.post_vars['game_acct_id'], live_level_data = request.post_vars['live_level_data'], modified = datetime.utcnow())
                    data = request.post_vars['live_level_data']
                    logging.info('Level ' + level_id + ' updated')
                else:
                    logging.error('Level manipulation failed. No manipulation flag set.')

    # /api/gameaccounts
    elif request.args(0) == 'gameaccts':
        if (request.env.request_method == 'POST'):
            
            # register (/api/gameaccts)
            if request.args(1) is None:
                # register handling goes here
                logging.info('register')

            # login (/api/gameaccts/login)
            elif request.args(1) == 'login':
                input_game_acct_name = request.post_vars['game_acct_name']
                input_game_acct_pass = request.post_vars['game_acct_password']

                entity = db(db.GameAccount.game_acct_name == input_game_acct_name).select().first()
                
                if entity is not None:
                    if entity.game_acct_password == input_game_acct_pass:
                        data = input_game_acct_name + ',' + input_game_acct_pass
                        logging.info('Game account ' + input_game_acct_name + ' logged in')
                    else:
                        logging.info('Login failed for game account ' + input_game_acct_name + '. Password incorrect.')
                else:
                    logging.info('Login failed for game account ' + input_game_acct_name + '. game_acct_name doesn\'t exist.')

    return dict(data=data)

"""@auth.requires_login() 
def api():

    #this is example of API with access control
    #WEB2PY provides Hypermedia API (Collection+JSON) Experimental

    from gluon.contrib.hypermedia import Collection
    rules = {
        'blog': {
        'GET':{'query':None,'fields':['id', 'authour']},
        'POST':{},'PUT':{},'DELETE':{}},
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}}
        }
    return Collection(db).process(request,response,rules)"""
