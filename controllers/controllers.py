# -*- coding: utf-8 -*-
from flectra import http

# class SmartTraidingAccounts(http.Controller):
#     @http.route('/smart_traiding_accounts/smart_traiding_accounts/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/smart_traiding_accounts/smart_traiding_accounts/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('smart_traiding_accounts.listing', {
#             'root': '/smart_traiding_accounts/smart_traiding_accounts',
#             'objects': http.request.env['smart_traiding_accounts.smart_traiding_accounts'].search([]),
#         })

#     @http.route('/smart_traiding_accounts/smart_traiding_accounts/objects/<model("smart_traiding_accounts.smart_traiding_accounts"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('smart_traiding_accounts.object', {
#             'object': obj
#         })