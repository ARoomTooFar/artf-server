from datetime import datetime

db.define_table('Level',
    Field('live_level_data', 'text'),
    Field('draft_level_data', 'text'),
    Field('game_acct_id', 'bigint'),
    Field('mach_id', 'bigint'),
    Field('created', 'datetime'),
    Field('modified', 'datetime')
)

db.define_table('GameAcct',
    Field('game_acct_name', 'string'),
    Field('game_acct_password', 'string'),
    Field('web_acct_id', 'bigint'),
    Field('created', 'datetime'),
    Field('modified', 'datetime')
)

db.define_table('blog',
	Field('post_title', 'string'),
	Field('authour', 'string'),
	Field('date_posted', 'datetime'),
	Field('postbody', 'text'))

db.Level.game_acct_id.required = True
db.Level.mach_id.required = True
db.Level.created.default = datetime.utcnow()
db.Level.created.writable = False
db.Level.modified.default = datetime.utcnow()
db.Level.modified.writable = False

db.GameAcct.game_acct_name.required = True
db.GameAcct.game_acct_password.required = True
db.GameAcct.created.default = datetime.utcnow()
db.GameAcct.created.writable = False
db.GameAcct.modified.default = datetime.utcnow()
db.GameAcct.modified.writable = False
