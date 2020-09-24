# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ContractNumber(models.Model):
    _name = 'contract.number'
    _description = "Numero de conrato"

    name = fields.Char(string='Numero de serie', required=True)
    date = fields.Date(string="Fecha del contrato")
    