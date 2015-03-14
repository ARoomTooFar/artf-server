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

    return dict(message=T('A Room Too Far Web Server'), msg=msg)

def editor():
    if auth.user:
        lvlId = '5715999101812736';
    else:
        lvlId = '0';

    return dict(display_title='Level Editor', lvlId=lvlId)

def media():


    return dict(display_title= 'Media')

def locations():


    return dict(display_title= 'Locations')

def blog():


    return dict(display_title= 'Blog')

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

def webgl():
    return dict()

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
        page_title = 'Workshop'
        btnLevels = A('Your Levels', _class='btn', _href=URL('default', 'workshop', args=['levels']))
    
    elif request.args(0) == 'levels':

        # /workshop/levels/[LEVELID]/del
        if str(request.args(1)).isdigit() and request.args(2) == 'del':
            page_title = 'Delete Level'

            btnLevels = A('Your Levels', _class='btn', _href=URL('default', 'workshop', args=['levels']))
            form = FORM.confirm('Are you sure you want to delete your level?')

            if form.accepted:
                db(db.Level.id == request.args(1)).delete()
                session.flash = T('Level ' + str(request.args(1)) + ' deleted')
                redirect(URL('default', 'workshop', args=['levels']))

        # /workshop/levels/[LEVELID]
        # need to add in security here later so people can't edit other people's levels
        elif str(request.args(1)).isdigit():
            page_title = 'Level Editor'
            ids = str(auth.user.game_acct_id) + ',' + request.args(1)
            btnLevels = A('Your Levels', _class='btn', _href=URL('default', 'workshop', args=['levels']))

            # get level data for debugging purposes
            entity = db(db.Level.id == request.args(1)).select().first()
            levelData = entity.live_level_data

            response.view = request.controller + '/leveleditor.html'

        # /workshop/levels/add
        elif request.args(1) == 'add':
            page_title = 'New Level'

            btnLevels = A('Your Levels', _class='btn', _href=URL('default', 'workshop', args=['levels']))
            form = FORM.confirm('Do you want to create a new level?')

            if form.accepted:
                db.Level.insert(live_level_data='', draft_level_data='', game_acct_id=auth.user.game_acct_id, mach_id=123)
                session.flash = T('New level created!')
                redirect(URL('default', 'workshop', args=['levels']))

        # /workshop/levels
        else:
            page_title = 'Your Levels'

            btnAddLevel = A('Add Level', _class='btn', _href=URL('default', 'workshop', args=['levels', 'add']))

            def create_btnEditLevel(row):
                btnEditLevel = A('Edit Level', _class='btn', _href=URL('default', 'workshop', args=['levels', row.id]))
                return btnEditLevel

            def create_btnDelLevel(row):
                btnDelLevel = A('Delete Level', _class='btn', _href=URL('default', 'workshop', args=['levels', row.id, 'del']))
                return btnDelLevel

            links = [
                dict(header='', body=create_btnEditLevel),
                dict(header='', body=create_btnDelLevel)
            ]

            levelsList = SQLFORM.grid(db.Level.game_acct_id == auth.user.game_acct_id, create=False, editable=False, deletable=False, details=False, csv=False, user_signature=False, links=links)

    return dict(page_title=page_title, btnLevels=btnLevels, btnAddLevel=btnAddLevel, levelsList=levelsList, ids=ids, form=form, levelData=levelData)

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


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
