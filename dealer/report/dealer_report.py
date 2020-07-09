from odoo import api, models


class DealerReport(models.AbstractModel):
    _name = 'report.dealer.report_dealer'

    @api.model
    def _get_report_values(self, docids, data=None):
        list1_id = []
        for rec in docids:
            sale_obj = self.env['sale.order'].search([('dealer', '=', rec)])
            dealer_obj = self.env['dealer.dealer'].browse(rec)
            x = {'dealer': dealer_obj, 'sale_ids': sale_obj}
            list1_id.append(x)
        return {
            'doc_ids': docids,
            'doc_model': 'dealer.dealer',
            'docs': list1_id,
        }
