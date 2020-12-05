# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.http import route
import base64
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortalInherit(CustomerPortal):
    OPTIONAL_BILLING_FIELDS = ["zipcode", "state_id", "vat", "company_name", "age"]

    @route(['/my/account'], type='http', auth='user', website=True)
    def account(self, redirect=None, **post):
        print('age', post.get('age'))
        print('----- My First Inherit Controller ---')
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values.update({
            'error': {},
            'error_message': [],
        })

        if post and request.httprequest.method == 'POST':
            error, error_message = self.details_form_validate(post)
            values.update({'error': error, 'error_message': error_message})
            values.update(post)
            if not error:
                values = {key: post[key] for key in self.MANDATORY_BILLING_FIELDS}
                values.update({key: post[key] for key in self.OPTIONAL_BILLING_FIELDS if key in post})
                values.update({'country_id': int(values.pop('country_id', 0))})
                values.update({'zip': values.pop('zipcode', '')})
                if values.get('state_id') == '':
                    values.update({'state_id': False})
                partner.sudo().write(values)
                if redirect:
                    return request.redirect(redirect)
                return request.redirect('/my/home')

        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])

        values.update({
            'partner': partner,
            'countries': countries,
            'states': states,
            'has_check_vat': hasattr(request.env['res.partner'], 'check_vat'),
            'redirect': redirect,
            'page_name': 'my_details',
        })

        response = request.render("portal.portal_my_details", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response


class MyFirstModule(http.Controller):

    @http.route('/car/full_description', auth='public', type='http', website=True)
    def display_car_full_description(self, **kw):


        car = request.env['car.car'].search([('id','=',kw.get('id'))])
        vals={
            'car':car
        }
        return request.render('my_first_module.display_car_with_full_description', vals)




    @http.route('/cars', auth='public', type='http', website=True)
    def display_car(self, **kw):
        cars = request.env['car.car'].search([])
        vals = {
            'cars': cars
        }
        return request.render('my_first_module.display_cars', vals)

    @http.route('/cars/create', auth='public', type='http', website=True)
    def redirect_to_form_car_create(self, **kw):
        return request.render('my_first_module.create_car_form')

    @http.route('/create', auth='public', type='http', website=True)
    def create_new_car(self, **kw):
        if kw['file']:
            file = kw.get('file').stream.read()
        request.env['car.car'].create({
            'name': kw.get('name'),
            'doors_number': kw.get('doors_number'),
            'horse_power': kw.get('horse_power'),
            'driver': kw.get('driver'),
            'is_truck': True if kw.get('is_truck') else False,
            'is_sport': True if kw.get('is_sport') else False,
            'start_date': kw.get('start_date'),
            'file': base64.encodestring(file)
        })
        return request.redirect('/cars')

    @http.route('/update', auth='public', type='http', website=True)
    def redirect_to_form_update(self, **kw):
        vals = {}
        car_object = request.env['car.car'].search([('id', '=', kw.get('id'))])
        print('car_object', car_object)
        vals.update({
            'car': car_object
        })
        return request.render('my_first_module.update_car_form', vals)

    @http.route('/update/car', auth='public', type='http', website=True)
    def update_car(self, **kw):
        id = int(kw.get('id'))
        request.env['car.car'].search([('id', '=', id)]).write({
            'name': kw.get('name'),
            'doors_number': kw.get('doors_number'),
            'horse_power': kw.get('horse_power')
        })
        return request.redirect('/cars')

    @http.route('/delete', auth='public', type='http', website=True)
    def delete_cars(self, **kw):
        car_id = kw.get('id')
        request.env['car.car'].search([('id', '=', car_id)]).unlink()
        return request.redirect('/cars')
