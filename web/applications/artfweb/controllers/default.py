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

@auth.requires_login()
def workshop():
    btnLevels = None
    levelsList = None
    lvlId = 0

    # /workshop
    if request.args(0) is None:
        page_title = 'Workshop'
        btnLevels = A('Your Levels', _class='btn', _href=URL('default', 'workshop', args=['levels']))
    
    elif request.args(0) == 'levels':
        
        # /workshop/levels/[LEVELID]
        # need to add in security here later so people can't edit other people's levels
        if request.args(1) is not None:
            page_title = 'Level Editor'
            lvlId = request.args(1)
            response.view = request.controller + '/leveleditor.html'
        
        # /workshop/levels
        else:
            page_title = 'Your Levels'

            def create_btnEditLvl(row):
                btnEditLvl = A('Edit Level', _class='btn', _href=URL('default', 'workshop', args=['levels', row.id]))
                return btnEditLvl

            links = [
                dict(header='', body=create_btnEditLvl)
            ]

            levelsList = SQLFORM.grid(db.Level.game_acct_id == auth.user.game_acct_id, create=False, editable=False, deletable=False, details=False, csv=False, user_signature=False, links=links)

    return dict(page_title=page_title, btnLevels=btnLevels, levelsList=levelsList, lvlId=lvlId)

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
