# -*- coding: utf-8 -*-

from flectra import models, fields, api
from flectra.tools import float_is_zero, float_compare, pycompat
from num2words import num2words
from datetime import datetime, date
from flectra.exceptions import ValidationError


class Sales(models.Model):
    _inherit = 'sale.order'
    amount_word = fields.Char(string='amount in words', compute='compute_word')
    packingsum = fields.Integer(string='packing', compute='word')
    netweightsum = fields.Integer(string='nweight', compute='netword')

    @api.depends('amount_total')
    def compute_word(self):

        for rec in self:
            if rec.amount_total:
                x = num2words(rec.amount_total).upper()
                y = "US DOLLAR " + x
                rec.amount_word = y

    def word(self):
        for record in self:
            sum = 0

            for rec in record.order_line:
                sum = sum + rec.cus_package_count
            record.packingsum = sum

    def netword(self):
        for record in self:
            netweight = 0

            for rec in record.order_line:
                netweight = netweight + rec.netweight

            record.netweightsum = netweight


class Salesline(models.Model):
    _inherit = 'sale.order.line'
    netweight = fields.Integer(string='net', compute='wordqty')

    def wordqty(self):
        for record in self:
            multi = 0

            multi = (record.product_uom_qty * record.product_id.weight)
            record.netweight = multi


class Stock(models.Model):
    _inherit = 'stock.picking'
    packingsum = fields.Float(string='packing', compute='word')
    netweightsum = fields.Float(string='nweight', compute='netword')
    grossweightsum = fields.Float(string='gweight', compute='gword')

    def word(self):
        for record in self:
            sum = 0

            for rec in record.move_lines:
                sum = sum + rec.cus_package_count

            record.packingsum = sum

    def netword(self):
        for record in self:
            netweight = 0

            for rec in record.move_lines:
                netweight = netweight + rec.netweight

            record.netweightsum = netweight

    def gword(self):
        for record in self:
            x = 0

            for rec in record.move_lines:
                x = x + rec.g

            record.grossweightsum = x


class Stockmove(models.Model):
    _inherit = 'stock.move'
    netweight = fields.Integer(string='net', compute='wordqty')

    def wordqty(self):
        for record in self:
            multi = 0

            multi = (record.quantity_done * record.product_id.weight)
            record.netweight = multi


class Partner(models.Model):
    _inherit = 'res.partner'

    cus_tax_types = fields.Selection(
        [('tax', 'Tax Invoice'), ('stax', 'Suspended Tax'), ('alltax', 'All Inclusive'), ('comtax', 'Commercial'),
         ('protax', 'Proforma')]
        , string='Tax Types', default='tax')

