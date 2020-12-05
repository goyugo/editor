# -*- coding: utf-8 -*-

from odoo import models, fields


class my_first_module(models.Model):
    _name = 'car.car'
    name = fields.Char(string='Name')
    doors_number = fields.Integer(string='Doors Number')
    horse_power = fields.Integer(string='Horse Power')
    driver = fields.Many2one('res.partner', string='Driver')
    is_sport = fields.Boolean('Is Sport')
    is_truck = fields.Boolean('Is Truck')
    start_date = fields.Date('Date')
    file = fields.Binary('File')
    description = fields.Text('Description')

    engine_name = fields.Char('Engine Name')
    architect = fields.Char('Architect ')
    engine_layout=fields.Char('Engine Layout ')

    maximum_speed=fields.Char('Maximum Speed')


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    age = fields.Char(string='Age')
