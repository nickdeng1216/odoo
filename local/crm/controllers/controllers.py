# -*- coding: utf-8 -*-
# from odoo import http


# class Src/odoo/local/crm(http.Controller):
#     @http.route('/src/odoo/local/crm/src/odoo/local/crm/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/src/odoo/local/crm/src/odoo/local/crm/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('src/odoo/local/crm.listing', {
#             'root': '/src/odoo/local/crm/src/odoo/local/crm',
#             'objects': http.request.env['src/odoo/local/crm.src/odoo/local/crm'].search([]),
#         })

#     @http.route('/src/odoo/local/crm/src/odoo/local/crm/objects/<model("src/odoo/local/crm.src/odoo/local/crm"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('src/odoo/local/crm.object', {
#             'object': obj
#         })
