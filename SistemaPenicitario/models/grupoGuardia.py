
from odoo import fields, models, api, exceptions, _

class grupoGuardia(models.Model):

    _name = 'grupo.guardia'
    _description = 'Grupo Guardia'
    
    name = fields.Char( string = 'Nombre' )
    cantidad_vigilantes = fields.Integer( string = 'Cantidad de vigilantes ( 1 - 5 )', required = True )
    experiencia_promedio = fields.Integer( string = 'Experiencia promedio ( 1 - 10 )', required = True)
    extrictos = fields.Integer( string = 'Extrictos ( 1 - 15 )', required = True )
    confiabilidad = fields.Boolean( string = 'Confiabilidad Nocturna', required = True )
    tiempo_respuesta = fields.Integer( string = 'Tiempo de respueta ( 15 - 45 )', required = True )

    @api.constrains('cantidad_vigilantes')
    def _check_cantidad_vigilantes(self):
        for record in self:
            if record.cantidad_vigilantes < 1 or record.cantidad_vigilantes > 5:
                raise exceptions.UserError(_('La cantidad de vigilantes debe estar entre 1 y 5.'))

    @api.constrains('experiencia_promedio')
    def _check_experiencia_promedio(self):
        for record in self:
            if record.experiencia_promedio < 1 or record.experiencia_promedio > 10:
                raise exceptions.UserError(_('La experiencia promedio de estar entre 1 y 10'))

    @api.constrains('extrictos')
    def _check_extrictos(self):
        for record in self:
            if record.extrictos < 1 or record.extrictos > 15:
                raise exceptions.UserError(_('El rango de extricos con los presos debe de estar entre 1 y 15'))

    @api.constrains('confiabilidad')
    def _check_tiempo_respuesta(self):
        for record in self:
            if record.tiempo_respuesta < 15 or record.tiempo_respuesta > 45:
                raise exceptions.UserError(_('El tiempo de respuesta debe estar entre 15 y 45'))