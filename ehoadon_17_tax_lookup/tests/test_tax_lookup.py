# -*- coding: utf-8 -*-
from unittest.mock import MagicMock, patch

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase

REQUESTS_GET = 'odoo.addons.ehoadon_tax_lookup.models.res_partner.requests.get'


class TestTaxLookup(TransactionCase):
    def test_button_fills_einvoice_fields(self):
        partner = self.env['res.partner'].create({'name': 'Lookup', 'einvoice_vat_info': '0100109106'})
        response = MagicMock(status_code=200)
        response.json.return_value = {'taxID': '0100109106', 'name': 'VIETTEL', 'address': 'Ha Noi'}
        with patch(REQUESTS_GET, return_value=response) as get:
            partner.button_get_einvoice_info()
        get.assert_called_once()
        self.assertIn('0100109106', get.call_args.args[0])
        self.assertEqual(partner.einvoice_vat, '0100109106')
        self.assertEqual(partner.einvoice_name, 'VIETTEL')
        self.assertEqual(partner.einvoice_address, 'Ha Noi')

    def test_invalid_tax_code_does_not_call_api(self):
        partner = self.env['res.partner'].create({'name': 'Lookup', 'einvoice_vat_info': '123'})
        with patch(REQUESTS_GET) as get, self.assertRaisesRegex(UserError, 'không hợp lệ'):
            partner.button_get_einvoice_info()
        get.assert_not_called()
