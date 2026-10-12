# -*- coding: utf-8 -*-
{
    'name': 'eHoaDon Tax Code Lookup',
    'version': '20.1.1.0.0',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'summary': 'Fill partner e-invoice info from a tax code (XInvoice lookup)',
    'author': 'Thien Long Tri',
    'website': 'https://thienlongtri.vn',
    'support': 'longnb2010@gmail.com',
    'depends': [
        'ehoadon_20',
    ],
    'data': [
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}