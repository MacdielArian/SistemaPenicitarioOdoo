
from odoo import models, fields, api, exceptions, _

class PeleaPrisioneros(models.Model):

    _name = 'pelea.prisioneros'
    _description = 'Pelea Prisioneros'

    celda1 = fields.Many2one( 'celda', string = 'Prisionero 1' )
    celda2 = fields.Many2one( 'celda', string = 'Prisionero 2' )
    ganador = fields.Char( string = 'Ganador' )

    api.constrains('celda1', 'celda2')
    def pelea_prisioneros(self):

        todos_fosos = self.env['foso'].search([])

        for record in self:

            pandilla_prisionero1 = ''
            pandilla_prisionero2 = ''
            nivel_peligrosidad1 = 0
            nivel_peligrosidad2 = 0
            prisionero1 = any
            prisionero2 = any
            
            if record.celda1 == record.celda2:

                raise exceptions.UserError(_('No pueden elegir las mismas celdas'))

            if record.celda1.tipo_prisionero == 'permanente':

                pandilla_prisionero1 = record.celda1.prisionero_permanente.pandilla
                nivel_peligrosidad1 = record.celda1.prisionero_permanente.nivel_peligrosidad_permanente
                prisionero1 = record.celda1.prisionero_permanente

            elif record.celda1.tipo_prisionero == 'temporal':

                pandilla_prisionero1 = record.celda1.prisionero_temporal.pandilla
                nivel_peligrosidad1 = record.celda1.prisionero_temporal.nivel_peligrosidad_temporal
                prisionero1 = record.celda1.prisionero_temporal

            if record.celda2.tipo_prisionero == 'permanente':

                pandilla_prisionero2 = record.celda2.prisionero_permanente.pandilla
                nivel_peligrosidad2 = record.celda2.prisionero_permanente.nivel_peligrosidad_permanente
                prisionero2 = record.celda2.prisionero_permanente

            elif record.celda2.tipo_prisionero == 'temporal':

                pandilla_prisionero2 = record.celda2.prisionero_temporal.pandilla
                nivel_peligrosidad2 = record.celda2.prisionero_temporal.nivel_peligrosidad_temporal
                prisionero2 = record.celda2.prisionero_temporal

            if pandilla_prisionero1 == pandilla_prisionero2:

                raise exceptions.UserError(_('Los prisioneros de una misma pandilla no pueden pelear'))

            else:

                if nivel_peligrosidad1 > nivel_peligrosidad2:

                    if record.celda1.tipo_prisionero == 'permanente':

                        record.celda1.prisionero_permanente.annos_condena = record.celda1.prisionero_permanente.annos_condena + 3

                    elif record.celda1.tipo_prisionero == 'temporal':

                        record.celda1.prisionero_temporal.annos_condena = record.celda1.prisionero_temporal.annos_condena + 3

                    self.env['foso'].create({
                        'numero_piso_foso' : len(todos_fosos) + 1,
                        'tipo_prisionero' : record.celda1.tipo_prisionero,
                        'grupo_guardia' : record.celda1.grupo_guardia.id,
                        'prisionero_permanente' : record.celda1.prisionero_permanente.id,
                        'prisionero_temporal' : record.celda1.prisionero_temporal.id,
                        'dias_restantes' : 10
                    })

                    record.ganador = 'Prisionero 1'
                    prisionero2.unlink()


                else:

                    if record.celda2.tipo_prisionero == 'permanente':

                        record.celda2.prisionero_permanente.annos_condena = record.celda2.prisionero_permanente.annos_condena + 3

                    elif record.celda2.tipo_prisionero == 'temporal':

                        record.celda2.prisionero_temporal.annos_condena = record.celda2.prisionero_temporal.annos_condena + 3

                    self.env['foso'].create({
                        'numero_piso_foso' : len(todos_fosos) + 1,
                        'tipo_prisionero': record.celda2.tipo_prisionero,
                        'grupo_guardia' : record.celda2.grupo_guardia.id,
                        'prisionero_permanente' : record.celda2.prisionero_permanente.id,
                        'prisionero_temporal' : record.celda2.prisionero_temporal.id,
                        'dias_restantes' : 10
                    })

                    record.ganador = 'Prisionero 2'
                    prisionero1.unlink()

                record.celda1.unlink()
                record.celda2.unlink()

            


            
                