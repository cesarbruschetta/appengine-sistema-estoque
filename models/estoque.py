# -*- coding: utf-8 -*-
from google.appengine.ext import db

# Create your models here.
class Estoque(db.Model):
    codigo = db.StringProperty() #max_length=200)
    nome = db.StringProperty()  #max_length=200)
    