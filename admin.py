# -*- coding: utf-8 -
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import users

from google.appengine.ext import db

from models.produtos import Produto
from models.estoque import Estoque
from models.quantidade_produto import QuantidadeProduto
from models.solicita_produto import SolicitaProduto
from models.status_solicitacao import StatusSolicitacao

import utils

class AdminHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        
        if not user:
            self.redirect(users.create_login_url(self.request.path))
            
        else:
            utils.doRender(self,'admin.html',{'user':user} )
        
class ProdutoHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        
        if not user:
            self.redirect(users.create_login_url(self.request.path))
            
        else:
            produtos = Produto.all()
            utils.doRender(self,'add_produtos.html',{'user':user, 'produtos':produtos} )        

    def post(self):
        #dbg()
        if self.request.POST.has_key('codigo') and self.request.POST.has_key('nome'):
            cod_produto = self.request.POST['codigo']
            nome_produto = self.request.POST['nome']
            
            produto = Produto(codigo=cod_produto,nome=nome_produto)
            produto.put()
            
            self.get()
        else:    
             self.redirect('/admin/add_produto')   

class EstoqueHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        
        if not user:
            self.redirect(users.create_login_url(self.request.path))
            
        else:
            estoques = Estoque.all()
            utils.doRender(self,'add_estoques.html',{'user':user, 'estoques':estoques} )        

    def post(self):
        #dbg()
        if self.request.POST.has_key('codigo') and self.request.POST.has_key('nome'):
            cod_estoque = self.request.POST['codigo']
            nome_estoque = self.request.POST['nome']
            
            estoque = Estoque(codigo=cod_estoque,nome=nome_estoque)
            estoque.put()
            
            self.get()
        
        else:    
             self.redirect('/admin/add_estoque')
            
class QuantidadeProdutosHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
       
        if not user:
            self.redirect(users.create_login_url(self.request.path))
        else:
            produtos_em_estoque = QuantidadeProduto().quantidade_estoque()
            utils.doRender(self,'add_quantidade_produto.html',{'user':user,
                                                               'produtos_em_estoques':produtos_em_estoque,
                                                               'produtos':QuantidadeProduto().combo_produto(),
                                                               'estoques':QuantidadeProduto().combo_estoque()})        

    def post(self):
        
        if self.request.POST.has_key('produto') and self.request.POST.has_key('estoque') and \
            self.request.POST.has_key('quantidade'):
            
            cod_produto = self.request.POST['produto']
            cod_estoque = self.request.POST['estoque']
            quantidade = self.request.POST['quantidade']
            
            if cod_produto !='' and cod_estoque!='' and quantidade!='':
            
                add_quant_prod_est = QuantidadeProduto(produto=db.Key(cod_produto),
                                                       estoque=db.Key(cod_estoque),
                                                       quantidade=int(quantidade),
                                                       flag_fluxo=True) 
                add_quant_prod_est.put()
              
                self.get()
            
            else:    
             self.redirect('/admin/add_quantidade')
        
        else:    
             self.redirect('/admin/add_quantidade')


class ListaSolicitacoesHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        
        if not user:
            self.redirect(users.create_login_url(self.request.path))
            
        else:
            solicitacoes = SolicitaProduto.all().filter('status =',False)
            utils.doRender(self,'lista_solicitacoes.html',{'user':user, 'solicitacoes':solicitacoes} )        

class StatusSolicitacaoHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if not user:
            self.redirect(users.create_login_url(self.request.path))
            
        else:
            if self.request.GET.has_key('id') and self.request.GET['id'] != '':
                id = self.request.GET['id']
                
                solicitacao = db.GqlQuery("SELECT * FROM SolicitaProduto WHERE __key__ = :1 ", db.Key(id))
                
                #solicitacao = SolicitaProduto.all().get('__key__ =',db.Key(id))   #   filter('key =', db.Key(id))
                utils.doRender(self,'solicitacao.html',{'user':user, 'solicitacao':solicitacao.get()})      

            else:
                self.redirect('/admin/lista_solicitacoes')
  
    def post(self):
        if self.request.POST.has_key('cod_solicitacao'):
            cod_solicitacao = self.request.POST['cod_solicitacao']
            if self.request.POST.has_key('status'):
                status = True
                razao = ''
            else:
                status = False
                razao = self.request.POST['razao']
            
            if cod_solicitacao !='':
                status_solicitacao = StatusSolicitacao(cod_solicitacao=db.Key(cod_solicitacao),
                                                       flag_status=status,razao=razao)
                status_solicitacao.put()
                
                solicitacao = db.GqlQuery("SELECT * FROM SolicitaProduto WHERE __key__ = :1 ", db.Key(cod_solicitacao)).get()
                solicitacao.status = True
                solicitacao.put()
                
                if status:
                    add_quant_prod_est = QuantidadeProduto(produto=solicitacao.produto.key(),
                                                           estoque=solicitacao.estoque.key(),
                                                           quantidade=1,flag_fluxo=False) 
                    add_quant_prod_est.put()
                
                
                self.redirect('/admin/lista_solicitacoes')
  

def main():
    application = webapp.WSGIApplication([('/admin', AdminHandler),
                                         ('/admin/add_produto', ProdutoHandler),
                                         ('/admin/add_estoque', EstoqueHandler),
                                         ('/admin/add_quantidade', QuantidadeProdutosHandler),
                                         ('/admin/lista_solicitacoes', ListaSolicitacoesHandler),
                                         ('/admin/solicitacao', StatusSolicitacaoHandler)], debug=True)   
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()

                