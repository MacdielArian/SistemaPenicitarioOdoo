
{
    'name' : 'Sistema Penicitario',
    'version' : '1.0',
    'category' : 'Ejercicio',
    'author' : 'Mc Dev',
    'depends' : [ 'base', 'mail' ],
    'data' : [
        'views/grupo_guardia_view.xml',
        'views/prisionero_permanente_view.xml',
        'views/prisionero_temporal_view.xml',
        'views/prisionero_view.xml',
        'views/celda_view.xml',
        'views/foso_view.xml',
        'views/fuga_grupal.xml',
        'views/pelea_prisioneros.xml',
        'views/menu.xml',
        'security/ir.model.access.csv'
    ],
    'application' : True
}