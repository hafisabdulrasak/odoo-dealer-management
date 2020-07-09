from odoo import models, fields, api


class WizardDealerCommission(models.TransientModel):
    _name = 'dealer.commission.wiz'
    _description = 'Dealer Commission Calc'

    date_from = fields.Date(string='Start date')
    date_to = fields.Date(string='End date')
    # dealer = fields.Many2one('dealer.dealer', string='Dealer')
    dealer = fields.Many2many(
        "dealer.dealer", "dealer_commission_rel", "dealer")
    sales_confirmed = fields.Boolean(string='Sales Complete', default=True)

    @api.multi
    def get_report(self):
        data = {}
        data["form"] = self.read(
            [
                "dealer",
                "date_from",
                "date_to",
                "sales_confirmed"
            ]
        )[0]
        return self.env.ref("dealer.action_report_dealer_commission_wiz"
                            ).report_action(self, data=data)
