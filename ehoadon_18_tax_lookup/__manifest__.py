# -*- coding: utf-8 -*-
{
    'name': 'eHoaDon Tax Code Lookup',
    'version': '18.0.1.0.0',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'summary': 'Fill partner e-invoice info from a tax code (XInvoice lookup)',
    'author': 'BizStore Group',
    'website': 'https://ehoadon.online',
    'support': 'ehoadon@bizstore.vn',
    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
    ],
    'depends': [
        'ehoadon_18',
    ],
    'data': [
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
