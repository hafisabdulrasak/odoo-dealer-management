# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from odoo.exceptions import AccessError, MissingError, UserError
from datetime import date


class DealerCommission(models.Model):
    _name = 'dealer.commission'
    _description = "sale deal commission"
    _rec_name = 'dealer'

    @api.multi
    def button_reset(self):
        for rec in self:
            rec.write({'state': 'draft'})

    state = fields.Selection([
        ('draft', 'Draft'),
        ('paid', 'Paid'),
    ], required=True, default='draft')

    dealer = fields.Many2one(
        'dealer.dealer', ondelete='cascade', string="Dealer", required=True
    )
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    extra_amount = fields.Float(string='Extra Amount')
    total_amount = fields.Float(string='Total Amount', compute='_compute_out')
    description = fields.Text(string='Description')
    invoice = fields.Many2one(
        'account.invoice', ondelete='cascade', string="Invoice")

    completed_sales = fields.One2many(
        'sale.order', 'comp_id', "completed sales")

    @api.multi
    def button_payed(self):
        for rec in self:
            rec.write({'state': 'paid'})
        result = self.env['account.invoice'].create({
            'partner_id': self.dealer.partner.id,
            'name': 'customer',
            'type': 'out_invoice',
            'date_invoice': date.today(),
            'invoice_line_ids': [(0, 0, {
                'name': 'test line',
                'origin': self.completed_sales.name,
                'account_id': self.dealer.partner.id,
                'price_unit': self.completed_sales.amount_total,
                'quantity': 0.0,
                'discount': 0.0,
                'sale_line_ids': [
                    (6, 0, [line.id for line in self.completed_sales])],
            })],
        })
        self.invoice = result
        return result

    @api.depends('extra_amount', 'completed_sales.amount_pay')
    def _compute_out(self):
        for rec in self:
            total = 0
            for a in rec.completed_sales:
                total = total + a.amount_pay
            rec.total_amount = rec.extra_amount + total

    @api.multi
    def get_sales(self):
        sales = self.env['sale.order'].search(
            [('date_order', '>=', self.start_date),
             ('date_order', '<=', self.end_date),
             ('dealer', '=', self.dealer.id),
             ('state', '=', ['sale', 'done'])]
        )
        if len(self.completed_sales) == 0:
            for sale in sales:
                self.write({'completed_sales': [(4, sale.id)]})
        else:
            for sale_id in self.completed_sales:
                sale_id.comp_id = False
                # self.write({'completed_sales': [(5, )]})
            for sale in sales:
                self.write({'completed_sales': [(4, sale.id)]})

    @api.constrains('dealer')
    def _check_dealer(self):
        menu = self.env['dealer.commission'].search(
            [('state', '=', 'draft'), ('dealer', '=', self.dealer.id)])
        for record in menu:
            m = record.id - self.id
            if m != 0:
                raise UserError('dealer already in draft, It is not accepted!')

