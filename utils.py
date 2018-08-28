# -*- coding: utf-8 -
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import os
import wsgiref.handlers

def doRender(handler, tname='index', values={}):
    temp = os.path.join(os.path.dirname(__file__),'templates/' + tname)
    if not os.path.isfile(temp):
        return False
    # Make a copy of the dictionary and add the path
    newval = dict(values)
    #newval['path'] = handler.request.path
    #if 'username' in handler.session:
    #    newval['username'] = handler.session['username']
   
    outstr = template.render(temp, newval)
    handler.response.out.write(outstr)
    return True