from openerp import models,fields, api
import exceptions
#from openerp.osv import osv
class sale_reports(models.Model):
    _name = 'sale.reports'
    invoice_selection = fields.Selection([('done', 'Invoiced'),('manual', 'Backlog')],'Invoice Selection')
    date_from = fields.Date('Order Date From')
    date_to = fields.Date('Order Date To')
    customer=fields.Many2one('res.partner','Customer')


    def filter_data(self,cr,uid,ids,context=None):
        domain= ''

        filter_rec =self.browse(cr,uid,ids,context=context)
        i_sel=filter_rec.invoice_selection
        c_id=filter_rec.customer.id

        if filter_rec.customer and i_sel:
            if i_sel=='done':
                domain=[('partner_id','=',c_id) ,('state','=','done')]
            elif i_sel=='manual':
                domain=[('partner_id','=',c_id),('state','=','manual')]
        # elif i_sel=='done':
        #      domain=['|' ,('state','=','progress'),('state','=','done')]
        # elif i_sel=='manual':
        #     domain=['|',('state','=','shipping_except'),('state','=','invoice_except')]

        elif filter_rec.customer:
            domain=[('partner_id','=',c_id)]

        elif filter_rec.date_from and filter_rec.date_to:
            domain=[('date_order','>',filter_rec.date_to),('date_order','<',filter_rec.date_from)]


        # elif filter_rec.date_from:
        #     raise exceptions.except_orm(_('Warning!'), _('choose the necessary fields'))
        # elif filter_rec.date_to:
        #     raise exceptions.except_orm(_('Warning!'), _('choose the necessary fields'))


        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'tree',
            'view_type': 'tree',
            'context' : context,
            'target': 'new',
            'domain': domain
             }