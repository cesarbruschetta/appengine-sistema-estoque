# -*- coding: utf-8 -
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.api import users

import utils
from models.solicita_produto import SolicitaProduto
from models.quantidade_produto import QuantidadeProduto

def dbg():
    """ Enter pdb in App Engine
        Renable system streams for it.
    """
    import pdb
    import sys
    pdb.Pdb(stdin=getattr(sys,'__stdin__'),stdout=getattr(sys,'__stderr__')).set_trace(sys._getframe().f_back)


class MainHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        D={}
        if user:
            D['user'] = user
        utils.doRender(self,'main_page.html',D)
       
class Login(webapp.RequestHandler):
    def get(self):
        self.redirect(users.create_login_url('/'))
     
class Logout(webapp.RequestHandler):
    def get(self):
         self.redirect(users.create_logout_url('/'))
        
class AddSolicitacaoHandler(webapp.RequestHandler):
    def get(self):
        
       utils.doRender(self,'add_solicitacao.html',{'produtos':QuantidadeProduto().combo_produto(),
                                                   'estoques':QuantidadeProduto().combo_estoque()})

    def post(self):
        if self.request.POST.has_key('nome') and self.request.POST.has_key('produto') and \
            self.request.POST.has_key('estoque') and self.request.POST.has_key('razao'):

            nome = self.request.POST['nome']
            cod_produto = self.request.POST['produto']
            cod_estoque = self.request.POST['estoque']
            razao = self.request.POST['razao']
            
            if nome !='' and cod_produto !='' and cod_estoque!='' and razao !='':
            
                add_solicitacao = SolicitaProduto(nome=nome,produto=db.Key(cod_produto),
                                                  estoque=db.Key(cod_estoque),quantidade=1,
                                                  razao=razao, status=False) 
                add_solicitacao.put()
              
                self.redirect('/')
            
            else:    
             self.redirect('/admin/add_quantidade')
        
        else:    
             self.redirect('/admin/add_quantidade')



def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/add_solicitacao', AddSolicitacaoHandler),
                                          ('/login', Login),
                                          ('/login', Logout)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
