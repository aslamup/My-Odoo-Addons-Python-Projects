from openerp import models, fields, api
from openerp.osv import osv

class sale_related_field(models.Model):
    _inherit = 'sale.order'

    project_id = fields.Many2one('account.analytic.account',string='Contract / Analytic',required=True,ondelete='cascade', domain=[('parent_id','ilike','ordernumber')])
    order_type = fields.Many2one('account.analytic.account',string='Order Type',required=True, domain=[('parent_id','ilike','ordertype')])
    staff = fields.Many2one('account.analytic.account',string='Staff',required=True, domain=[('parent_id','ilike','staff')], ondelete='cascade')



class purchase_related_field(models.Model):
    _inherit = 'purchase.order.line'

    order_type = fields.Many2one('account.analytic.account',string='Order Type',required=True,domain=[('parent_id','ilike','ordertype')])
    staff = fields.Many2one('account.analytic.account',string='Staff',required=True,domain=[('parent_id','ilike','staff')])

class invoice_related_field(models.Model):
    _inherit = 'account.invoice.line'

    order_type = fields.Many2one('account.analytic.account',string='Order Type',required=True,domain=[('parent_id','ilike','ordertype')])
    staff = fields.Many2one('account.analytic.account',string='Staff',required=True,domain=[('parent_id','ilike','staff')])

class create_invoice(models.Model):
    _inherit = 'sale.order'

    def _prepare_invoice(self, cr, uid, order, lines, context=None):

        self.pool.get('account.invoice.line').write(cr, uid, lines, {'order_type': order.order_type.id,'staff' : order.staff.id})
        return super(create_invoice, self)._prepare_invoice(cr, uid, order, lines, context=None)

class my_stock_move(osv.osv):
    _inherit = 'stock.move'

    def _get_invoice_line_vals(self, cr, uid, move,partner, inv_type, context=None):
        res = super(my_stock_move, self)._get_invoice_line_vals(cr, uid, move, partner, inv_type, context=context)
        if inv_type in ('out_invoice', 'out_refund') and move.procurement_id and move.procurement_id.sale_line_id:
            sale_line = move.procurement_id.sale_line_id
            res['order_type'] = sale_line.order_id.order_type and sale_line.order_id.order_type.id or False
            res['staff'] = sale_line.order_id.staff and sale_line.order_id.staff.id or False

        return res

class journel_related_field(models.Model):
    _inherit = 'account.move.line'

    order_type = fields.Many2one('account.analytic.account',string='Order Type',required=True,domain=[('parent_id','ilike','ordertype')])
    staff = fields.Many2one('account.analytic.account',string='Staff',required=True,domain=[('parent_id','ilike','staff')])

class my_account_invoice(models.Model):
    _inherit = "account.invoice"

    @api.model
    def line_get_convert(self, line, part, date):
        res = super(my_account_invoice, self).line_get_convert(line, part, date)
        res['order_type'] = line.get('order_type',False)
        res['staff'] = line.get('staff',False)
        return res

class my_account_invoice_line(models.Model):
    _inherit = "account.invoice.line"

    @api.model
    def move_line_get_item(self,line):
        res = super(my_account_invoice_line, self).move_line_get_item(line)
        res['order_type'] = line.order_type.id
        res['staff'] = line.staff.id
        return res

class my_journel_related_field(models.Model):
    _inherit = "account.invoice.tax"

    @api.model
    def move_line_get(self,invoice_id):
        res = super(my_journel_related_field, self).move_line_get(invoice_id)
        for row in self._cr.dictfetchall():
            res.append({
                'order_type': row['order_type'],
                'staff': row['staff'],
            })
        return res