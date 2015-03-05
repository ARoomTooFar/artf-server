from datetime import datetime

db.define_table('Level',
    Field('live_level_data', 'text'),
    Field('draft_level_data', 'text'),
    Field('game_acct_id', 'integer'),
    Field('mach_id', 'integer'),
    Field('created', 'datetime'),
    Field('modified', 'datetime')
)

db.Level.created.default = datetime.utcnow()
db.Level.created.writable = False
db.Level.modified.default = datetime.utcnow()
db.Level.modified.writable = False