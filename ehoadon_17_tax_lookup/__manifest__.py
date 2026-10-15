# -*- coding: utf-8 -*-
{
    'name': 'eHoaDon Tax Code Lookup',
    'version': '17.0.1.0.0',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'summary': 'Fill partner e-invoice info from a tax code (XInvoice lookup)',
    'author': 'Thien Long Tri',
    'website': 'https://thienlongtri.vn',
    'support': 'longnb2010@gmail.com',
    'depends': [
        'ehoadon_17',
    ],
    'data': [
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
