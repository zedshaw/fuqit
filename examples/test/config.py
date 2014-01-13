from fuqit import data

db = data.database(dbn='sqlite', db='data.sqlite3')
allowed_referer = '.*'
default_mtype = 'text/html'
static_dir = '/static/'

