from openerp.osv import fields

from openerp import models

class Sale_order(models.Model):

    _inherit = 'sale.order'

    _columns = {
        'state': fields.selection([
            ('draft', 'Draft Quotation'),
            ('to_check','To check'),
            ('checked','Checked'),
            ('approved','Approved'),
            ('sent', 'Quotation Sent'),
            ('cancel', 'Cancelled'),
            ('waiting_date', 'Waiting Schedule'),
            ('progress', 'Sales Order'),
            ('manual', 'Sale to Invoice'),
            ('invoice_except', 'Invoice Exception'),
            ('done', 'Done'),
            ], 'Status', readonly=True, track_visibility='onchange',
            help="Gives the status of the quotation or sales order. \nThe exception status is automatically set when a cancel operation occurs in the processing of a document linked to the sales order. \nThe 'Waiting Schedule' status is set when the invoice is confirmed but waiting for the scheduler to run on the order date.", select=True),
    }

    def menu_tocheck(self, cr, uid, ids,context=None):
     res=self.write(cr, uid, ids, {'state': 'to_check'},context=context)
     return res

    def menu_checked(self, cr, uid, ids,context=None):
     res=self.write(cr, uid, ids, {'state': 'checked'},context=context)
     return res

    def menu_approved(self, cr, uid, ids,context=None):
     res=self.write(cr, uid, ids, {'state': 'approved'},context=context)
     return res