# -*- coding: utf-8 -*-
{
    'name': "Sales Ilusiones",

    'summary': """
        Sales Ilusiones
        """,

    'description': """
        Sales Ilusiones
    """,

    'author': "David Rosales",
    'website': "#",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','sale_management'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
    ],
 	'images': ['static/description/banner.png','static/src/img/icon.png'],
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': 105,
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}
