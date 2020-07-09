from odoo import api, models


class DealerReport(models.AbstractModel):
    _name = 'report.dealer.report_dealer_commission_wiz'

    @api.model
    def _get_report_values(self, docids, data=None):
        date_start = data['form']['date_from']
        date_end = data['form']['date_to']
        dealer = data['form']['dealer']
        sales_confirmed = data['form']['sales_confirmed']
        list1_id = []
        domain = []
        if dealer:
            domain.append(('dealer', 'in', dealer))
        if date_start:
            domain.append(('start_date', '>=', date_start))
        if date_end:
            domain.append(('end_date', '<=', date_end))
        dealer_com = self.env['dealer.commission'].search(domain)
        for rec in dealer_com:
            total = 0
            for b in rec.completed_sales:
                if sales_confirmed:
                    if b.state in 'done':
                        total = b.amount_total + total
                else:
                    if b.state in ['sale', 'draft', 'sent']:
                        total = 0
            x = {'dealer': rec, 'sale_ids': total}
            list1_id.append(x)
        return {
            'doc_ids': docids,
            'doc_model': 'dealer.dealer',
            'docs': list1_id,
        }
