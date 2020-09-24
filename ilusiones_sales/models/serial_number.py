# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ServicesSales(models.Model):
    _name = 'serial.number'
    _description = "Numero de serie"

    name = fields.Char(string='Numero de serie', required=True)
    #Unico
