from openerp import models, fields

class Ship1(models.Model):
    _name = 'ship.ship1'

    _sql_constraints = [
        ('IMO_unique', 'unique(IMO)', 'imo number must be unique!'),
    ]

    IMO = fields.Char(string='IMO',required=True)
    _rec_name = 'IMO'
    Hull_Number =fields.Integer(string='Hull_Number',required=True)
    Engine_Number =fields.Integer(string='Engine_Number',required=True)
    Vessel_Name = fields.Char(string='Vessel_Name ',required=True)
    Build_Year =fields.Integer(string='Build_Year',required=True)

    Ship_Yard =fields.Many2one('res.partner',string='Ship_Yard',required=True)
    Ship_Owner =fields.Many2one('res.partner',string='Ship_Owner',required=True)
    Ship_Management =fields.Many2one('res.partner',string='Ship_Management',required=True)
    Engine_Builder = fields.Many2one('res.partner',string='Engine_Builder',required=True)
