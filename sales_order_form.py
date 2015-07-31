from openerp import models, fields, api

class sale_order(models.Model):
    _inherit = 'sale.order'
    ship = fields.Many2one('ship.ship1','Ship')

    project = fields.Char(string='Project')
    contract_no = fields.Char(string='Contract No:')

    related_purchase = fields.One2many('purchase.order','related_so')

    related_commission = fields.One2many('salesman_commission','sales_order_id')

    prepared_by= fields.Char(string='Prepared by',readonly=True)
    approved_by= fields.Char(string='Approved by',readonly=True)

    def update_order(self, cr, uid, ids, context=None):
        sale_order_rec = self.browse(cr, uid, ids, context=context)
        for order_line_rec in sale_order_rec.order_line:
            order_line_rec.write({'ship':sale_order_rec.ship.id })

    #functions for automatically filling values in approved by and prepared by when button press
    @api.one
    @api.depends('prepared_by')
    def update_prepared_by(self):
       self.prepared_by= self.env.user.name

    @api.one
    @api.depends('approved_by')
    def update_approved_by(self):
        self.approved_by= self.env.user.name


class sale_order_line(models.Model):
    _inherit = 'sale.order.line'
    ship=fields.Many2one('ship.ship1','Ship')

class purchase_order(models.Model):
    _inherit = 'purchase.order'
    contract_no = fields.Char(string='Contract No:')
    related_so = fields.Many2one('sale.order',string='Related Sales Order',ondelete='cascade')

    def onchange_sale(self, cr, uid, ids, related_so, context=None):
        res = {}
        if related_so:
            obj = self.pool.get('sale.order').browse(cr, uid, related_so)
            res['contract_no'] = obj.contract_no
        return {'value': res}

class salesman_commission(models.Model):
    _name = 'salesman_commission'

    user = fields.Many2one('res.users',string='User')
    sales_order_id = fields.Many2one('sale.order',string='Sale id',ondelete='cascade')
    sales_val = fields.Float(compute='function1',string='Sales Value')
    percent = fields.Float(string='Percent')
    commission = fields.Integer(compute='function2',string='Commission')

    @api.one
    @api.depends('sales_order_id.amount_total')
    def function1(self):
        self.sales_val = self.sales_order_id.amount_total

    @api.one
    @api.depends('sales_val','percent')
    def function2(self):
        self.commission = (self.sales_val*self.percent)/100