# -*- coding: utf-8 -*-
from google.appengine.ext import db

from models.produtos import Produto
from models.estoque import Estoque

# Create your models here.
class QuantidadeProduto(db.Model):
    produto = db.ReferenceProperty(Produto)
    estoque = db.ReferenceProperty(Estoque)
    quantidade = db.IntegerProperty()
    flag_fluxo = db.BooleanProperty()
    
   
    def combo_estoque(self):
        estoques = Estoque.all()
        return estoques
    
    def combo_produto(self):
        produtos = Produto.all()
        return produtos
    
    
    def quantidade_estoque(self,estoques=None,produtos=None):
        if produtos == None:
            produtos = Produto.all()

        produtos_estoque = []    
        for produto in produtos:
            if estoques == None:
                estoques = Estoque.all()
            for estoque in estoques:
                quantidades_produtos = QuantidadeProduto.all().filter('estoque =', estoque.key()).filter('produto =', produto.key())
                if quantidades_produtos.count() != 0:
                    quantidade = 0 
                    D = {}
                    for quantidade_produto in quantidades_produtos:
                        nome_produto = quantidade_produto.produto.nome
                        if quantidade_produto.flag_fluxo:
                            quantidade += quantidade_produto.quantidade
                        else:
                            quantidade -= quantidade_produto.quantidade
                    D['quantidade'] = quantidade
                    D['nome_produto'] = nome_produto
                    D['estoque'] = estoque.nome
                    D['id_estoque'] = estoque.key()
                    
                    produtos_estoque.append(D)    
        
        return produtos_estoque    