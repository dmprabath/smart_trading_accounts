from flectra import models, fields, api, _


class pdcInhr(models.Model):
    _inherit = 'pdc.payment'

    client_name = fields.Many2one('res.partner', string="Client Name", related="related_inv_ids.partner_id")
    

    # @api.onchange('client_name')
    # def check_client(self):
    #     for rec in self:
    #         return{ 'domain': {'related_inv_ids': [('partner_id', '=',rec.client_name.id),('state', '=', 'open')]}}



class PdcPaymentWizard(models.TransientModel):
    _inherit='pdc.payment.wizard'

    @api.onchange('related_inv_ids')
    def set_client_name(self):
        if self.related_inv_ids:
            inv_obj = self.env['account.invoice'].search([('id', '=', self.related_inv_ids.id)])
            self.client_name = inv_obj.partner_id