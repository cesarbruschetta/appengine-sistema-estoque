# -*- coding: utf-8 -*-
from google.appengine.ext import db

from models.produtos import Produto
from models.solicita_produto import SolicitaProduto

# Create your models here.
class StatusSolicitacao(db.Model):
    cod_solicitacao = db.ReferenceProperty(SolicitaProduto)
    flag_status = db.BooleanProperty()
    razao = db.TextProperty()
    