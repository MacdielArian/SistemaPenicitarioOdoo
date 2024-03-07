

def tiempo_fuga_prisionero_permanente( prisionero ):

    tiempo_fuga_prisionero = 0

    if prisionero.nivel_escolaridad == 'universidad' and prisionero.relacion_guardia == 'excelente':
        tiempo_fuga_prisionero = 15
    elif prisionero.nivel_escolaridad == 'universidad' and prisionero.relacion_guardia == 'buena':
        tiempo_fuga_prisionero = 20
    else:
        tiempo_fuga_prisionero = 35
        
    return tiempo_fuga_prisionero

def tiempo_fuga_prisionero_temporal( prisionero ):

    tiempo_fuga_prisionero = 0

    if prisionero.nivel_adaptacion == 5:
        tiempo_fuga_prisionero = 30
    else:
        tiempo_fuga_prisionero = 40

    return tiempo_fuga_prisionero