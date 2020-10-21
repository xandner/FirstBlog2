from flask import session

from . import admin


@admin.route('/')
def admin_index():
    return 'hello admin'
@admin.route('/login')
def login():
    session['name']='xander'

    return '1'
