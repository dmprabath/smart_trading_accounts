# -*- coding: utf-8 -*-
{
    'name': "smart trading accounts",

    'summary': """
        Short """,

    'description': """
        Long description of module's purpose
    """,

    'author': "DM Prabath",
    'website': "http://www.codeso.lk",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/flectra/flectra/blob/master/flectra/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'account',
        'hr',
        'pdc_pay',
        'smart_trading_accounts_reports',
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/demo_data.xml',
        'views/account_invoice.xml',
        'views/new_report_template.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/pdc_pay.xml',
        # 'reports/invoice_commercial_report.xml',
        'reports/invoice_lkr_tax_report.xml',
        'reports/invoice_lkr_stax_report.xml',
        'reports/invoice_alltax_report.xml',
        'reports/menu_report.xml',
    ],
    # only loaded in demonstration mode

}