
from odoo import models, fields

class Foso(models.Model):

    _name = 'foso'
    _description = 'Foso'

    numero_piso_foso = fields.Integer( string = 'Numero de piso del foso' )

    grupo_guardia = fields.Many2one( 'grupo.guardia', string = 'Grupo de guardia', required = True )
    tipo_prisionero = fields.Selection(
        selection = [ ( 'permanente', 'Permanente' ), ( 'temporal', 'Temporal' ) ],
        string = 'Tipo de prisionero',
        required = True
    )
    prisionero_permanente = fields.Many2one( 'prisionero.permanente', string = 'Prisionero Permanente' )
    prisionero_temporal = fields.Many2one( 'prisionero.temporal', string = 'Prisionero Temporal' )

    dias_restantes = fields.Integer( string = 'Tiempo restante' )

        








