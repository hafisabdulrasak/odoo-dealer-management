# -*- coding: utf-8 -*-
{
    'name': "Dealer Management",

    'summary': """Manage dealers, sales and dealer commissions""",

    'description': """ """,

    'author': "hafis abdul rasak",
    # 'website': "http://www.hafisabdulrasak.com",
    'category': 'management',
    'license': 'AGPL-3',
    'version': '1.0',
    'depends': ['base', 'sale', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/wizard_dealer_commission.xml',
        'views/dealer_complete.xml',
        'views/dealer.xml',
        'views/sale_order_Inherited.xml',
        'report/report.xml',
        'report/dealer_commission.xml',
        'report/dealer_report.xml',
        'report/dealer_commission_wiz.xml',


    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo.xml',
    ],
    'installable': True,
    'application': True,
}
