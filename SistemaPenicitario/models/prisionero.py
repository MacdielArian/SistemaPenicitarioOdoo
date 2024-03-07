
from odoo import models, fields, api, exceptions, _

class Prisionero(models.Model):

    _name = 'prisionero'
    _description = 'Prisionero'

    name = fields.Char( string = 'Nombre', required = True )
    nivel_escolaridad = fields.Selection(
        selection = [( 'ninguno', 'Ninguno' ), ( 'secundario', 'Secundario' ), ( 'preuniversitario', 'Preuniversitario' ), ( 'universitario', 'Universitario' )],
        string = 'Nivel de Escolaridad',
        required = True
    )
    pandilla = fields.Selection(
        selection = [ ('yakuza', 'Yakuza'), ( 'latinos', 'Latinos' ), ( 'blancos', 'Blancos' ), ( 'afros', 'Afros' ) ],
        string = 'Pandilla',
        required = True
    )
    annos_condena = fields.Integer( string = 'Años de condena', required = True )
    asesinato = fields.Boolean( string = 'Asesinato', required = True )
    prestigio = fields.Integer( string = 'Prestigio (1 - 15)', required = True )

    @api.constrains('prestigio')
    def _check_prestigio(self):
        for record in self:
            if record.prestigio < 1 or record.prestigio > 15:
                raise exceptions.UserError(_('El prestigio debe ser entre 1 y 15'))


class PrisioneroPermanente(models.Model):

    _name = 'prisionero.permanente'
    _description = 'Prisionero permanente'
    _inherit = 'prisionero'

    relacion_guardia = fields.Selection(
        selection = [ ( 'excelente', 'Excelente' ), ( 'bien', 'Bien' ), ( 'mal', 'Mal' ) ],
        string = 'Relacion con los guardias',
        required = True
    )

    relacion_prisionero = fields.Selection(
        selection = [ ('excelente', 'Excelente' ), ( 'bien', 'Bien'), ( 'mal', 'Mal' ) ],
        string = 'Relacion con los prisioneros',
        required = True
    )

    tiempo_fuga_individual_permanente = fields.Integer( string = ' Tiempo de fuga individual', compute = '_compute_tiempo_fuga_permanente' )
    nivel_peligrosidad_permanente = fields.Integer( string = 'Nivel de peligrosidad', compute = '_compute_nivel_peligrosidad_permanente')

    @api.depends('nivel_escolaridad', 'relacion_guardia')
    def _compute_tiempo_fuga_permanente(self):

        for record in self:

            if record.nivel_escolaridad == 'universitario' and record.relacion_guardia == 'excelente':
                record.tiempo_fuga_individual_permanente = 15
            elif record.nivel_escolaridad == 'universitario' and record.relacion_guardia == 'bien':
                record.tiempo_fuga_individual_permanente = 30
            else:
                record.tiempo_fuga_individual_permanente = 35

    @api.depends('relacion_prisionero', 'prestigio')
    def _compute_nivel_peligrosidad_permanente(self):

        for record in self:

            if record.relacion_prisionero == 'excelente':

                record.nivel_peligrosidad_permanente = 1 + 5 + record.prestigio

            elif record.relacion_prisionero == 'bien':

                record.nivel_peligrosidad_permanente = 1 + 3 + record.prestigio

            else:
                record.nivel_peligrosidad_permanente = record.prestigio


class PrisioneroTemporal(models.Model):

    _name = 'prisionero.temporal'
    _description = 'Prisionero Temporal'
    _inherit = 'prisionero'

    experiencia_combate = fields.Boolean( string = 'Experiencia en combate' )
    nivel_adaptacion = fields.Integer( string = 'Nivel de adaptacion ( 1 - 5 )', required = True )

    tiempo_fuga_individual_temporal = fields.Integer( string = ' Tiempo de fuga individual', compute = '_compute_tiempo_fuga_temporal' )
    nivel_peligrosidad_temporal = fields.Integer( string = 'Nivel de peligrosidad', compute = '_compute_nivel_peligrosidad_temporal' )

    @api.constrains('nivel_adaptacion')
    def _check_nivel_adaptacion(self):
        for record in self:
            if record.nivel_adaptacion < 1 or record.nivel_adaptacion > 5:
                raise exceptions.UserError(_('El nivel de adaptación debe ser entre 1 y 5')) 

    @api.depends('nivel_adaptacion')
    def _compute_tiempo_fuga_temporal(self):

        for record in self:
            if record.nivel_adaptacion == 5:
                record.tiempo_fuga_individual_temporal = 30
            else:
                record.tiempo_fuga_individual_temporal = 40
    

    @api.depends('nivel_adaptacion', 'experiencia_combate')
    def _compute_nivel_peligrosidad_temporal(self):

        for record in self:

            if record.experiencia_combate == False:
                record.nivel_peligrosidad_temporal = 1 + record.nivel_adaptacion 
            else:
                record.nivel_peligrosidad_temporal = 1 + record.nivel_adaptacion + 3
