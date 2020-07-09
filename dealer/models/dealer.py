# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import date
from datetime import timedelta


class Dealer(models.Model):
    _name = 'dealer.dealer'
    _description = "sale dealers"

    name = fields.Char(string="name", required=True)
    age = fields.Integer(string='Age')
    city = fields.Char(string="City")
    email = fields.Char(string="Email", widget="email")
    commission = fields.Float(string='Commission')
    sales = fields.Integer(string='Annual sales')
    commission_type = fields.Selection(
        [('fixed', 'Fixed'), ('percentage', 'Percentage')], "commission type",
        default="fixed"
    )
    commission_paid = fields.Float(string='Commission Paid',
                                   compute='_compute_commission_paid')
    count = fields.Integer(string='sale count', compute='sales_count')
    partner = fields.Many2one(
        'res.partner', ondelete='cascade', string="Partner", required=True)

    @api.multi
    def create_commission(self):
        new_obj = self.env['dealer.commission']
        self.ensure_one()
        new_commission = new_obj.create({
            'dealer': self.id,
            'start_date': date.today(),
            'end_date': date.today() + timedelta(days=30),
        })
        new_commission.get_sales()
        return new_commission

    @api.multi
    def button_paid(self):
        return {
            'name': 'deal commission',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'dealer.commission',
            'type': 'ir.actions.act_window',
            'domain': [('dealer.id', '=', self.id)],
            'context': {'search_default_by_state_paid': 1},
        }

    @api.multi
    def button_sales(self):
        return {
            'name': 'deal sales',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'type': 'ir.actions.act_window',
            'domain': [('dealer.id', '=', self.id)],
            'context': {'search_default_sales': 1},
        }

    @api.multi
    def _compute_commission_paid(self):
        pay = 0
        new = []
        menu = self.env['dealer.commission'].search(
            [('state', '=', 'paid'), ('dealer', '=', self.id)])
        for rec in menu:
            new.append(rec)
            for aa in new:
                pay = pay + aa.total_amount
            self.commission_paid = pay

    @api.multi
    def sales_count(self):
        menu = self.env['sale.order'].search(
            [('state', '=', 'sale'), ('dealer', '=', self.id)])
        self.count = len(menu)


class SaleOrderInherited(models.Model):
    _inherit = 'sale.order'

    dealer = fields.Many2one('dealer.dealer', ondelete='cascade', string="Dealer", required=True)

    comp_id = fields.Many2one("dealer.commission", "completed_sale", ondelete="cascade")

    commission_type = fields.Selection([('fixed', 'Fixed'), ('percentage', 'Percentage')], "Commission Type")
    dealer_commission = fields.Float(string="Dealer Commission")
    amount_pay = fields.Float(string="Amount to pay")

    @api.onchange('dealer')
    def _onchange_dealer_(self):
        if self.dealer.id:
            self.commission_type = self.dealer.commission_type
            self.dealer_commission = self.dealer.commission

    @api.onchange('commission_type', 'dealer_commission', 'amount_total')
    def _onchange_commission_(self):
        if self.commission_type == 'fixed':
            self.amount_pay = self.dealer_commission
        if self.commission_type == 'percentage':
            self.amount_pay = self.amount_total * (self.dealer_commission / 100)
        if not self.commission_type:
            self.amount_pay = 0


# class SaleOrderLineInherited(models.Model):
#     _inherit = 'sale.order.line'
#
#     @api.model
#     def create(self, vals):
#         print(vals)
#         return super(SaleOrderLineInherited, self).create(vals)
