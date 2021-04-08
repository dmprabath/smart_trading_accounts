
# -*- coding: utf-8 -*-
# Part of Odoo, Flectra. See LICENSE file for full copyright and licensing details.


from flectra import models, fields, api
from flectra.tools import float_is_zero, float_compare, pycompat
from num2words import num2words
from datetime import datetime, date
from flectra.exceptions import ValidationError

class AccountTax(models.Model):
    _inherit = 'account.tax'

    cus_tax_types = fields.Selection(
        [('tax', 'Tax Invoice'),  ('alltax', 'All Inclusive')], string='Tax Types') 

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'


    cus_tax_types = fields.Selection(
        [('tax', 'Tax Invoice'), ('stax', 'Suspended Tax'), ('alltax', 'All Inclusive'), ('comtax', 'Commercial')],
        string='Tax Types')
    suspended_tax = fields.Monetary(string="Suspended V.A.T. 8%", compute='_compute_svat_total')

    amount_word = fields.Char(string='amount in words', compute='compute_word')
    checkedby_name = fields.Many2one('res.users', string='Checked By')

    today = fields.Date(default=fields.Datetime.now())
    age = fields.Integer(string='Age', compute='calculate_date')

    due = fields.Integer(string='Dates to due', compute='calculate_date_due')

    
    # @api.model
    # def _default_currency_with_deliveries(self):
    #     journal = self._default_journal()
    #     if self.env.context.get('type', 'out_invoice'):
    #         if self.deliveries:
    #             for pick in self.deliveries:
    #                 currency_id = pick.sale_id.currency_id
    #                 print("cuurrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr",currency_id)
    #             self.currency_id = currency_id
    #     else:
    #         self.currency_id.id = journal.currency_id.id or journal.company_id.currency_id.id or self.env.user.company_id.currency_id.id

    # currency_id = fields.Many2one('res.currency', string='Currency',
    #     required=True, readonly=True, states={'draft': [('readonly', False)]},
    #     compute=_default_currency_with_deliveries, track_visibility='always')
        

    def calculate_date(self):

        if self.date_invoice:
            d1 = datetime.strptime(self.date_invoice, '%Y-%m-%d')
            d2 = datetime.strptime(self.today, '%Y-%m-%d' )
            d3 = d2 - d1
            self.age = int(d3.days)

    def calculate_date_due(self):

        if self.date_due:
            a1 = datetime.strptime(self.date_due, '%Y-%m-%d')
            a2 = datetime.strptime(self.today, '%Y-%m-%d' )
            a3 = a2 - a1
            self.due = int(a3.days)


    @api.depends('amount_total')
    def compute_word(self):

        for rec in self:
            if rec.amount_total:
                x = num2words(rec.amount_total).upper()
                y = "US DOLLAR " + x
                rec.amount_word = y

    @api.depends('amount_total', 'cus_tax_types')
    def _compute_svat_total(self):
        for tax_line in self:
            if tax_line.amount_total:
                tax_line.suspended_tax = (tax_line.amount_total * 8) / 100

    @api.onchange('partner_id')
    def get_customer_tax_type(self):
        if self.partner_id:
            if self.partner_id.cus_tax_types:
                self.cus_tax_types = self.partner_id.cus_tax_types
            else:
                self.cus_tax_types = 'tax'
            if self.partner_id.user_id:
                self.user_id = self.partner_id.user_id
            # if self.partner_id.currency_id:
            #     self.currency_id = self.partner_id.currency_id

    @api.multi
    def new_invoice_print(self):
        self.ensure_one()
        if self.cus_tax_types == 'stax':
            return self.env.ref('smart_trading_accounts.smart_invoice_lkr_stax_menu').report_action(self)
        if self.cus_tax_types == 'alltax':
            return self.env.ref('smart_trading_accounts.smart_invoice_alltax_menu').report_action(self)
        if self.cus_tax_types == 'comtax':
            return self.env.ref('smart_trading_accounts_reports.smart_invoice_commercial_menu').report_action(self)
        else:
            return self.env.ref('smart_trading_accounts.smart_invoice_lkr_tax_menu').report_action(self)

    @api.multi
    def action_invoice_open(self):
        x = self.env.user
        self.checkedby_name = x

        to_open_invoices = self.filtered(lambda inv: inv.state != 'open')
        if to_open_invoices.filtered(lambda inv: inv.state != 'draft'):
            raise UserError(_("Invoice must be in draft state in order to validate it."))
        if to_open_invoices.filtered(
                lambda inv: float_compare(inv.amount_total, 0.0, precision_rounding=inv.currency_id.rounding) == -1):
            raise UserError(_(
                "You cannot validate an invoice with a negative total amount. You should create a credit note instead."))
        to_open_invoices.action_date_assign()
        to_open_invoices.action_move_create()
        return to_open_invoices.invoice_validate()



class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    invoice_line_tax_ids = fields.Many2many('account.tax',
        'account_invoice_line_tax', 'invoice_line_id', 'tax_id',
        string='Taxes', domain=[('type_tax_use','!=','none'), '|', ('active', '=', False), ('active', '=', True)], oldname='invoice_line_tax_id', compute="generate_default_tax_for_invoice")


    @api.depends('invoice_id.partner_id','invoice_id.cus_tax_types','product_id')
    def generate_default_tax_for_invoice(self):
        for rec in self:
            if rec.product_id:
                if rec.env.context.get('type', 'out_invoice'):
                    if rec.invoice_id.cus_tax_types:
                        tax_types = rec.env['account.tax'].search([('cus_tax_types','=',rec.invoice_id.cus_tax_types),('type_tax_use','=','sale'),('company_id', '=', rec.invoice_id.company_id.id)],limit=1)
                        if tax_types:
                            rec.invoice_line_tax_ids =  [(4, tax_types.id)]
                    #      ("sssssssssssssssssssssssssssssss", tax_types)
            
                # print("sssssssssssssssssssssssssssssss", self.invoice_id.cus_tax_types)
            # invoice_type = self.env.context.get('type', 'in_invoice')