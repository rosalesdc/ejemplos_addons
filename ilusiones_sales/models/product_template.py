# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplateMods(models.Model):
    _inherit = 'product.template'

    product_type = fields.Many2one('product.template', string='Productos almacenables')
    x_sale_type = fields.Selection(
        [('prepago', 'Prepago'), 
        ('plan', 'Plan'),
        ('activacion', 'Activación'),], 'Tipo de venta' )
    x_serial_id = fields.Many2one('serial.number', string="Número de serie")
    x_contract_id = fields.Many2one('contract.number', string="Número de contrato")
    x_precio_prepago = fields.Float(string='Precio prepago')
    x_precio_renta_mensual = fields.Float(string='Precio renta mensual')
    x_proteccion_equipo = fields.Selection(
        [('ninguno', 'Ninguno'), 
        ('proteccion55', 'Protección 55'),
        ('proteccion105', 'Protección 105'),
        ('proteccion155', 'Protección 155'), ], 'Protección de equipo' )