# -*- coding: utf-8 -*-
from google.appengine.ext import db

from models.produtos import Produto
from models.estoque import Estoque

# Create your models here.
class SolicitaProduto(db.Model):
    usuario = db.UserProperty()
    nome = db.StringProperty()  #max_length=200)
    produto = db.ReferenceProperty(Produto)
    estoque = db.ReferenceProperty(Estoque)
    quantidade = db.IntegerProperty()
    razao = db.TextProperty()
    status = db.BooleanProperty()
    
    
    