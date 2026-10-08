# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase


class TestEhoadonBuyer(TransactionCase):
    def _move(self, partner):
        return self.env['account.move'].create({'type': 'out_invoice', 'partner_id': partner.id})

    def test_partner_without_vat_is_retail_consumer(self):
        partner = self.env['res.partner'].create({'name': 'Khách lẻ'})
        customer = self._move(partner)._ehoadon_build_invoice_customer()
        self.assertEqual(customer['taxNumber'], '')
        self.assertEqual(customer['companyName'], 'Bán cho người tiêu dùng')

    def test_partner_with_vat_maps_company_buyer(self):
        company = self.env['res.partner'].create({
            'name': 'Cong ty ABC',
            'is_company': True,
            'vat': ' 0312345678 ',
            'street': '1 Le Loi',
            'city': 'HCM',
        })
        contact = self.env['res.partner'].create({'name': 'Nguyen Van A', 'parent_id': company.id})
        customer = self._move(contact)._ehoadon_build_invoice_customer()
        self.assertEqual(customer['taxNumber'], '0312345678')
        self.assertEqual(customer['companyName'], 'Cong ty ABC')
        self.assertEqual(customer['fullName'], 'Nguyen Van A')
        self.assertIn('1 Le Loi', customer['address'])
        self.assertNotIn('\n', customer['address'])
