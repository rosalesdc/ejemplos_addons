# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ServicesSales(models.Model):
    _name = 'serial.number'
    _description = "Número de serie"

    name = fields.Char(string='Número de serie', required=True)
    #Unico
