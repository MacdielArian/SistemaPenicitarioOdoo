
from odoo import models, fields, api, _, exceptions
from . import auxiliares

class Celda(models.Model):

    _name = 'celda'
    _decription = 'Celda'
    _order = 'numero_celda asc'

    numero_celda = fields.Integer(  string = 'Numero de celda oficial', readonly = True )
    grupo_guardia = fields.Many2one( 'grupo.guardia', string = 'Grupo de guardia', required = True )
    tipo_prisionero = fields.Selection(
        selection = [ ( 'permanente', 'Permanente' ), ( 'temporal', 'Temporal' ) ],
        string = 'Tipo de prisionero',
        required = True
    )
    prisionero_permanente = fields.Many2one( 'prisionero.permanente', string = 'Prisionero Permanente' )
    prisionero_temporal = fields.Many2one( 'prisionero.temporal', string = 'Prisionero Temporal' )

    
    @api.constrains('grupo_guardia')
    def _check_grupo_guardia(self):

        for record in self:
            if self.env['celda'].search_count([('grupo_guardia', '=', record.grupo_guardia.id)]) > 1:
                raise exceptions.UserError(_("El grupo de guardia ya ha sido asignado a otra celda."))

    @api.constrains('prisionero_permanente','prisionero_temporal' ,'tipo_prisionero')
    def _check_prisioneros(self):

        for record in self:

            if record.tipo_prisionero == 'permanente':

                if self.env['celda'].search_count([('prisionero_permanente', '=', record.prisionero_permanente.id)]) > 1:
                    raise exceptions.UserError(_('Este prisionero ya fue asignado a otra celda'))
            
            elif record.tipo_prisionero == 'temporal':

                if self.env['celda'].search_count([('prisionero_temporal', '=', record.prisionero_temporal.id)]) > 1:
                    raise exceptions.UserError(_('El prisionero ya fue asignado a otra celda'))

    @api.model
    def create(self, vals):
        # Verifica si hay celdas existentes
        existing_cells = self.env['celda'].search([])
        if  existing_cells:
            last_cell = self.env['celda'].search([], order='numero_celda desc', limit=1)
            vals['numero_celda'] = last_cell.numero_celda + 1
            return super(Celda, self).create(vals)
        else:
            vals['numero_celda'] = 1
            return super(Celda, self).create(vals)

    def transcurrir_dia(self):
        todas_celdas = self.env['celda'].search([])
        todos_pisos_foso = self.env['foso'].search([])
        ultima_celda = self.env['celda'].search([], order = 'id desc', limit = 1)

        cant_celdas = len(todas_celdas)

        for record in todas_celdas:

            if cant_celdas > 1:
                record.numero_celda = record.numero_celda + 1
            else:
                record.numero_celda = 1

            cant_celdas -= 1

        for record in todos_pisos_foso:

            record.dias_restantes -= 1

            if record.dias_restantes == 0:
 
                self.env['celda'].create({
                    'numero_celda' : ultima_celda.numero_celda,
                    'grupo_guardia' : record.grupo_guardia.id,
                    'tipo_prisionero' : record.tipo_prisionero,
                    'prisionero_permanente' : record.prisionero_permanente.id,
                    'prisionero_temporal' : record.prisionero_temporal.id
                })

                record.unlink()


    def fugo_individual(self):

        primera_celda = self.env['celda'].search([], order = 'numero_celda asc', limit = 1 )
        todos_fosos = self.env['foso'].search([])

        if primera_celda.tipo_prisionero == 'permanente':

            if primera_celda.prisionero_permanente.tiempo_fuga_individual_permanente < primera_celda.grupo_guardia.tiempo_respuesta:

                primera_celda.prisionero_permanente.annos_condena = primera_celda.prisionero_permanente.annos_condena + 1

                self.env['foso'].create({
                    'numero_piso_foso' : len(todos_fosos) + 1,
                    'tipo_prisionero' : primera_celda.tipo_prisionero,
                    'grupo_guardia' : primera_celda.grupo_guardia.id,
                    'prisionero_permanente' : primera_celda.prisionero_permanente.id,
                    'prisionero_temporal' : primera_celda.prisionero_temporal.id,
                    'dias_restantes' : 10
                })

            else:

                primera_celda.prisionero_permanente.unlink()
                
        elif primera_celda.tipo_prisionero == 'temporal':

            if primera_celda.prisionero_temporal.tiempo_fuga_individual_temporal < primera_celda.grupo_guardia.tiempo_respuesta:

                primera_celda.prisionero_temporal.annos_condena = primera_celda.prisionero_temporal.annos_condena + 1

                self.env['foso'].create({
                    'numero_piso_foso' : len(todos_fosos) + 1,
                    'tipo_prisionero' : primera_celda.tipo_prisionero,
                    'grupo_guardia' : primera_celda.grupo_guardia.id,
                    'prisionero_permanente' : primera_celda.prisionero_permanente.id,
                    'prisionero_temporal' : primera_celda.prisionero_temporal.id,
                    'dias_restantes' : 10
                })

            else:

                primera_celda.prisionero_temporal.unlink()

        primera_celda.unlink()

        todas_celdas = self.env['celda'].search([])

        cant_celdas = len(todas_celdas)

        for record in todas_celdas:

            record.numero_celda -= 1
            cant_celdas -= 1











     

