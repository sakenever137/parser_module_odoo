# -*- coding: utf-8 -*-
# from odoo import http


# class CronParser(http.Controller):
#     @http.route('/cron_parser/cron_parser/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cron_parser/cron_parser/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cron_parser.listing', {
#             'root': '/cron_parser/cron_parser',
#             'objects': http.request.env['cron_parser.cron_parser'].search([]),
#         })

#     @http.route('/cron_parser/cron_parser/objects/<model("cron_parser.cron_parser"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cron_parser.object', {
#             'object': obj
#         })
