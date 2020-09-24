# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrderMods(models.Model):
    _inherit = 'sale.order'

    #DESCONTAR DEL INVENTARIO
    def action_confirm(self):
        for line in self.order_line:
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
                'Sin existencia para la cantidad seleccionada so: %s ' % (line.x_producto_almacenable_id.name))
        order_confirm=super(SaleOrderMods, self).action_confirm()
        return order_confirm
        

class SaleOrderLinesMods(models.Model):
    _inherit = 'sale.order.line'

    x_sale_type = fields.Selection(
        [('prepago', 'Prepago'), 
        ('plan', 'Plan'),
        ('activacion', 'Activación'),], 'Tipo de venta',default='prepago' )
    x_serial_id = fields.Many2one('serial.number', string="Número de serie")
    x_contract_id = fields.Many2one('contract.number', string="Número de contrato")
    x_precio_prepago = fields.Float(string='Precio prepago')
    x_precio_renta_mensual = fields.Float(string='Precio renta mensual')
    x_proteccion_equipo = fields.Selection(
        [('ninguno', 'Ninguno'), 
        ('proteccion55', 'Protección 55'),
        ('proteccion105', 'Protección 105'),
        ('proteccion155', 'Protección 155'), ], 'Combo protección de equipo' )
    x_producto_almacenable_id = fields.Many2one('product.product', string="Producto almacenable", domain = [('type', '=', 'product')])
    x_producto_servicio_id = fields.Many2one('product.product', string="Servicio", domain = [('type', '=', 'service')])

    # @api.onchange('x_producto_almacenable_id')
    # def _in_stock_product(self):
    #     quants = self.env['stock.quant'].search([('product_id', '=', self.x_producto_almacenable_id.id)], limit=1)
    #     if quants.quantity < self.product_uom_qty:
    #         raise UserError(
    #             'Sin existencia para la cantidad seleccionada')

    #Verificar la existencia al crear las líneas
    def create(self, vals):
        res_id = super(SaleOrderLinesMods, self).create(vals)
        quants = self.env['stock.quant'].search([('product_id', '=', res_id.x_producto_almacenable_id.id)], limit=1)
        if quants.quantity < res_id.product_uom_qty:
            raise UserError(
                'Sin existencia para la cantidad seleccionada cr: %s ' % (res_id.x_producto_almacenable_id.name))
        return res_id
    
    #Verificar la existencia al actualizar las líneas
    def write(self, vals):
        res_id = super(SaleOrderLinesMods, self).write(vals)
        quants = self.env['stock.quant'].search([('product_id', '=', self.x_producto_almacenable_id.id)], limit=1)
        if quants.quantity < self.product_uom_qty:
            raise UserError(
                'Sin existencia para la cantidad seleccionada wr: %s ' % (self.x_producto_almacenable_id.name))
        return res_id

