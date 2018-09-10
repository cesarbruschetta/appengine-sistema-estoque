# -*- coding: utf-8 -
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users

import os
import wsgiref.handlers

def doRender(handler, tname='index', values={}, requered_aut=False):
    temp = os.path.join(os.path.dirname(__file__),'templates/' + tname)
    if not os.path.isfile(temp):
        return False

    user = users.get_current_user()
    if user:
        values['user'] = user

    if not user and requered_aut:
        handler.redirect(users.create_login_url(handler.request.path))

    # Make a copy of the dictionary and add the path
    newval = dict(values)

    #newval['path'] = handler.request.path
    #if 'username' in handler.session:
    #    newval['username'] = handler.session['username']

    outstr = template.render(temp, newval)
    handler.response.out.write(outstr)
    return True