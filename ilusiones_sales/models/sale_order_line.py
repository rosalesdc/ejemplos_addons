# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrderMods(models.Model):
    _inherit = 'sale.order'

    #DESCONTAR DEL INVENTARIO EL PRODUCTO ALMACENABLE SI ES PREPAGO O ACTIVACION
    def action_confirm(self):
        for line in self.order_line:
            if (line.x_sale_type == 'prepago' or line.x_sale_type == 'activacion') and line.x_producto_almacenable_id:
                quants = self.env['stock.quant'].search([('product_id', '=', line.x_producto_almacenable_id.id)], limit=1)
                warehouse = self.env['stock.warehouse'].search(
                [('company_id', '=', self.env.company.id)], limit=1
                )
                self.env['stock.quant'].with_context(inventory_mode=True).create({
                    'product_id': line.x_producto_almacenable_id.id,
                    'location_id': warehouse.lot_stock_id.id,
                    'inventory_quantity': quants.quantity - line.product_uom_qty,
                })
                if quants.inventory_quantity < 0:
                    raise UserError(
                    'Sin existencia de producto almacenable')
        order_confirm=super(SaleOrderMods, self).action_confirm()
        return order_confirm

class SaleOrderLinesMods(models.Model):
    _inherit = 'sale.order.line'

    x_sale_type = fields.Selection(
        [('no_tipo', 'Sin tipo asignado'),
        ('prepago', 'Prepago'), 
        ('plan', 'Plan'),
        ('activacion', 'Activación'),], 'Tipo de venta', compute='_compute_state' )
    x_serial_id = fields.Many2one('serial.number', string="Número de serie")
    x_contract_id = fields.Many2one('contract.number', string="Número de contrato")
    #Para los campos de precios se podría utilizar el precio unitario de la línea o especificar el comportamiento esperado
    # x_precio_prepago = fields.Float(string='Precio prepago')
    # x_precio_renta_mensual = fields.Float(string='Precio renta mensual')
    x_proteccion_equipo = fields.Selection(
        [('ninguno', 'Ninguno'), 
        ('proteccion55', 'Protección 55'),
        ('proteccion105', 'Protección 105'),
        ('proteccion155', 'Protección 155'), ], 'Combo protección de equipo' )
    x_producto_almacenable_id = fields.Many2one('product.product', string="Producto almacenable", domain = [('type', '=', 'product')])
    x_producto_servicio_id = fields.Many2one('product.product', string="Servicio", domain = [('type', '=', 'service')])

    #Verificar la existencia al crear las líneas
    def create(self, vals):
        res_id = super(SaleOrderLinesMods, self).create(vals)
        if self.x_sale_type == 'prepago' or self.x_sale_type == 'activacion' :
            if self.x_producto_almacenable_id:
                quants = self.env['stock.quant'].search([('product_id', '=', res_id.x_producto_almacenable_id.id)], limit=1)
                if quants.quantity < res_id.product_uom_qty:
                    raise UserError(
                        'Sin existencia de producto almacenable o no se ha seleccionado.')
            else:
                raise UserError(
                        'No se seleccionó producto almacenable')
        return res_id
    
    #Verificar la existencia al actualizar las líneas
    def write(self, vals):
        res_id = super(SaleOrderLinesMods, self).write(vals)
        if self.x_sale_type == 'prepago' or self.x_sale_type == 'activacion' :
            if self.x_producto_almacenable_id:
                quants = self.env['stock.quant'].search([('product_id', '=', self.x_producto_almacenable_id.id)], limit=1)
                if quants.quantity < self.product_uom_qty:
                    raise UserError(
                        'Sin existencia de producto almacenable.')
            else:
                raise UserError(
                    'No se seleccionó producto almacenable.')
        return res_id

    #Calcular el tipo de venta de acuerdo al producto seleccionado
    @api.depends('product_id')
    def _compute_state(self):
        if self.product_id.barcode == 'producto_prepago':
            self.x_sale_type = 'prepago'
        elif self.product_id.barcode == 'producto_plan':
            self.x_sale_type = 'plan'
        elif self.product_id.barcode == 'producto_activacion':
            self.x_sale_type = 'activacion'
        else:
            self.x_sale_type = 'no_tipo'
