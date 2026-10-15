# -*- coding: utf-8 -*-
{
    'name': 'eHoaDon Integration',
    'version': '17.0.1.0.0',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'summary': 'eHoaDon Online e-invoice on customer invoices',
    'author': 'Thien Long Tri',
    'website': 'https://thienlongtri.vn',
    'support': 'longnb2010@gmail.com',
    'depends': [
        'account',
        'l10n_vn',
    ],
    'data': [
        'security/ehoadon_security.xml',
        'security/ir.model.access.csv',
        'views/ehoadon_config_views.xml',
        'views/ehoadon_template_views.xml',
        'views/ehoadon_menu.xml',
        'views/account_move_views.xml',
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
