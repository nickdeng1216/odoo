# -*- coding: utf-8 -*-
# from odoo import http


# class Src/odoo/local/crm_project(http.Controller):
#     @http.route('/src/odoo/local/crm_project/src/odoo/local/crm_project/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/src/odoo/local/crm_project/src/odoo/local/crm_project/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('src/odoo/local/crm_project.listing', {
#             'root': '/src/odoo/local/crm_project/src/odoo/local/crm_project',
#             'objects': http.request.env['src/odoo/local/crm_project.src/odoo/local/crm_project'].search([]),
#         })

#     @http.route('/src/odoo/local/crm_project/src/odoo/local/crm_project/objects/<model("src/odoo/local/crm_project.src/odoo/local/crm_project"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('src/odoo/local/crm_project.object', {
#             'object': obj
#         })
