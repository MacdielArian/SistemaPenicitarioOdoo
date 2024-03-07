
from odoo import fields, models, api

class FugaGrupal(models.Model):

    _name = 'fuga.grupal'
    _description = 'Fuga grupal'

    cant_prisioneros_fuga = fields.Integer( string = 'Cantidad de prisioneros a la fuga', default = 1 )
    fuga_exitosa = fields.Boolean( string = 'Fuga exitosa', compute = '_compute_fuga_exitosa' )

    api.constrains('cant_prisioneros_fuga')
    def _compute_fuga_exitosa(self):

        pos_preso_mayor_prestigio = []
        pos_lider = 0
        mayor_prestigio = 0
        tiempo_total_grupo_guardia = 0
        tiempo_fuga_grupal = 0
        menos_tiempo_fuga_individual = 45

        todas_celdas = self.env['celda'].search([])
        todos_fosos = self.env['foso'].search([])
        cant_celdas = len( todas_celdas )

        for record in self:

            #Recorrer cada celda buscando el mayor prestigio
            i = 0

            for celda in todas_celdas:

                if celda.tipo_prisionero == 'permanente':
                    
                    if mayor_prestigio < celda.prisionero_permanente.prestigio:
                        mayor_prestigio = celda.prisionero_permanente.prestigio
                
                elif celda.tipo_prisionero == 'temporal':

                    if mayor_prestigio < celda.prisionero_temporal.prestigio:
                        mayor_prestigio = celda.prisionero_temporal.prestigio

                tiempo_total_grupo_guardia += celda.grupo_guardia.tiempo_respuesta

                i += 1

                if i == record.cant_prisioneros_fuga:
                    break

            # Buscar al lider o a los lideres
            i = 0

            for celda in todas_celdas:

                if celda.tipo_prisionero == 'permanente':

                    if celda.prisionero_permanente.prestigio == mayor_prestigio:
                        pos_preso_mayor_prestigio.append( i )
    
                elif celda.tipo_prisionero == 'temporal':

                    if celda.prisionero_temporal.prestigio == mayor_prestigio:
                        pos_preso_mayor_prestigio.append( i )

                i += 1

                if i == record.cant_prisioneros_fuga:
                    break

            if len( pos_preso_mayor_prestigio ) == 1:

                pos_lider = pos_preso_mayor_prestigio[0]

            else:

                for pos in pos_preso_mayor_prestigio:

                    if celda.tipo_prisionero == 'permanente':

                        if celda[pos].prisionero_permanente.tiempo_fuga_individual_permanente < menos_tiempo_fuga_individual:
                            menos_tiempo_fuga_individual = celda[pos].prisionero_permanente.tiempo_fuga_individual_permanente
                            pos_lider = pos

                    elif celda.tipo_prisionero == 'temporal':

                        if celda[pos].prisionero_temporal.tiempo_fuga_individual_temporal < menos_tiempo_fuga_individual:
                            menos_tiempo_fuga_individual = celda[pos].prisionero_temporal.tiempo_fuga_individual_temporal
                            pos_lider = pos

            # Saber el tiempo de fuga grupal

            i = 0

            for celda in todas_celdas:

                if i != pos_lider:

                    if celda[i].tipo_prisionero == 'permanente':

                        tiempo_fuga_grupal += celda[i].prisionero_permanente.tiempo_fuga_individual_permanente
                    
                    elif celda[i].tipo_prisionero == 'temporal':

                        tiempo_fuga_grupal += celda[i].prisionero_temporal.tiempo_fuga_individual_temporal

                else:

                    if celda[pos_lider].tipo_prisionero == 'permanente':

                        tiempo_fuga_grupal += celda[pos_lider].prisionero_permanente.tiempo_fuga_individual_permanente + ( record.cant_prisioneros_fuga - 1 )

                    elif celda[pos_lider].tipo_prisionero == 'temporal':

                        tiempo_fuga_grupal += celda[pos_lider].prisionero_temporal.tiempo_fuga_individual_temporal + ( record.cant_prisioneros_fuga - 1 )

                i += 1

                if i == record.cant_prisioneros_fuga:
                    break

            # Comprobar si la fuga fue exitosa o no
            if tiempo_total_grupo_guardia > tiempo_fuga_grupal:

                i = 0

                for celda in todas_celdas:

                    if celda.tipo_prisionero == 'permanente':
                        celda.prisionero_permanente.annos_condena = celda.prisionero_permanente.annos_condena + 1
                    elif celda.tipo_prisionero == 'temporal':
                        celda.prisionero_temporal.annos_condena = celda.prisionero_temporal.annos_condena + 1

                    if i == record.cant_prisioneros_fuga:
                        break
                
                self.env['foso'].create({
                    'numero_piso_foso' : len( todos_fosos ) + 1,
                    'tipo_prisionero' : todas_celdas[pos_lider].tipo_prisionero,
                    'grupo_guardia' : todas_celdas[pos_lider].grupo_guardia.id,
                    'prisionero_permanente' : todas_celdas[pos_lider].prisionero_permanente.id,
                    'prisionero_temporal' : todas_celdas[pos_lider].prisionero_temporal.id,
                    'dias_restantes' : 10
                })

                todas_celdas[pos_lider].unlink()

                record.fuga_exitosa = True

            else:

                record.fuga_exitosa = False

                i = 0

                for celda in todas_celdas:

                    celda[pos_lider].unlink()

                    if i == record.cant_prisioneros_fuga:
                        break

            


             

            
            
            






