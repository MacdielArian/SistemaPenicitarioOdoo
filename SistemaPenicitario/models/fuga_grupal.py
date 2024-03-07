

from odoo import fields, models, api

class FugaGrupal(models.Model):

    _name = 'fuga.grupal'
    _description = 'Fuga grupal'

    cant_prisioneros_fuga = fields.Integer( string = 'Cantidad de prisioneros a la fuga', default = 1 )
    fuga_exitosa = fields.Boolean( string = 'Fuga exitosa' )

    api.constrains('cant_prisioneros_fuga')
    def fuga_grupal(self):

        pos_preso_mayor_prestigio = []
        pos_lider = 0
        mayor_prestigio = 0
        tiempo_total_grupo_guardia = 0
        tiempo_fuga_grupal = 0
        menos_tiempo_fuga_individual = 45

        todas_celdas = self.env['celda'].search([])
        todos_fosos = self.env['foso'].search([])

        for record in self:

            #Recorrer cada celda buscando el mayor prestigio
        
            for i in range ( record.cant_prisioneros_fuga ):

                if todas_celdas[i].tipo_prisionero == 'permanente':
                    
                    if mayor_prestigio < todas_celdas[i].prisionero_permanente.prestigio:
                        mayor_prestigio = todas_celdas[i].prisionero_permanente.prestigio
                
                elif todas_celdas[i].tipo_prisionero == 'temporal':

                    if mayor_prestigio < todas_celdas[i].prisionero_temporal.prestigio:
                        mayor_prestigio = todas_celdas[i].prisionero_temporal.prestigio

                tiempo_total_grupo_guardia += todas_celdas[i].grupo_guardia.tiempo_respuesta
         
            # Buscar al lider o a los lideres
            for i in range( record.cant_prisioneros_fuga ):

                if todas_celdas[i].tipo_prisionero == 'permanente':

                    if todas_celdas[i].prisionero_permanente.prestigio == mayor_prestigio:
                        pos_preso_mayor_prestigio.append( i )
    
                elif todas_celdas[i].tipo_prisionero == 'temporal':

                    if todas_celdas[i].prisionero_temporal.prestigio == mayor_prestigio:
                        pos_preso_mayor_prestigio.append( i )


            if len( pos_preso_mayor_prestigio ) == 1:

                pos_lider = pos_preso_mayor_prestigio[0]

            else:

                for pos in pos_preso_mayor_prestigio:

                    if todas_celdas[pos].tipo_prisionero == 'permanente':

                        if todas_celdas[pos].prisionero_permanente.tiempo_fuga_individual_permanente < menos_tiempo_fuga_individual:
                            menos_tiempo_fuga_individual = todas_celdas[pos].prisionero_permanente.tiempo_fuga_individual_permanente
                            pos_lider = pos

                    elif todas_celdas[pos].tipo_prisionero == 'temporal':

                        if todas_celdas[pos].prisionero_temporal.tiempo_fuga_individual_temporal < menos_tiempo_fuga_individual:
                            menos_tiempo_fuga_individual = todas_celdas[pos].prisionero_temporal.tiempo_fuga_individual_temporal
                            pos_lider = pos

            # Saber el tiempo de fuga grupal

            for i in range( record.cant_prisioneros_fuga ):

                if i != pos_lider:

                    if todas_celdas[i].tipo_prisionero == 'permanente':

                        tiempo_fuga_grupal += todas_celdas[i].prisionero_permanente.tiempo_fuga_individual_permanente
                    
                    elif todas_celdas[i].tipo_prisionero == 'temporal':

                        tiempo_fuga_grupal += todas_celdas[i].prisionero_temporal.tiempo_fuga_individual_temporal

                else:

                    if todas_celdas[pos_lider].tipo_prisionero == 'permanente':

                        tiempo_fuga_grupal += todas_celdas[pos_lider].prisionero_permanente.tiempo_fuga_individual_permanente + ( record.cant_prisioneros_fuga - 1 )

                    elif todas_celdas[pos_lider].tipo_prisionero == 'temporal':

                        tiempo_fuga_grupal += todas_celdas[pos_lider].prisionero_temporal.tiempo_fuga_individual_temporal + ( record.cant_prisioneros_fuga - 1 )

            # Comprobar si la fuga fue exitosa o no
            if tiempo_total_grupo_guardia < tiempo_fuga_grupal:

                for i in range( record.cant_prisioneros_fuga ):

                    if todas_celdas[i].tipo_prisionero == 'permanente':
                        todas_celdas[i].prisionero_permanente.annos_condena = todas_celdas[i].prisionero_permanente.annos_condena + 1
                    elif todas_celdas[i].tipo_prisionero == 'temporal':
                        todas_celdas[i].prisionero_temporal.annos_condena = todas_celdas[i].prisionero_temporal.annos_condena + 1
                
               
                self.env['foso'].create({
                    'numero_piso_foso' : len( todos_fosos ) + 1,
                    'tipo_prisionero' : todas_celdas[pos_lider].tipo_prisionero,
                    'grupo_guardia' : todas_celdas[pos_lider].grupo_guardia.id,
                    'prisionero_permanente' : todas_celdas[pos_lider].prisionero_permanente.id,
                    'prisionero_temporal' : todas_celdas[pos_lider].prisionero_temporal.id,
                    'dias_restantes' : 10
                })

                todas_celdas[pos_lider].unlink()

                record.fuga_exitosa = False

            else:
                
   
                for i in range( record.cant_prisioneros_fuga ):

                    celda = todas_celdas[i]

                    celda.unlink()
                

                record.fuga_exitosa = True
            


             

            
            
            






