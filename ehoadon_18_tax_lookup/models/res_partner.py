# -*- coding: utf-8 -*-
import json

import requests
from requests import RequestException

from odoo import _, models
from odoo.exceptions import UserError

TAX_LOOKUP_URL = 'https://api.xinvoice.vn/gdt-api/tax-payer/%s'
TAX_LOOKUP_TIMEOUT = 30


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _einvoice_tax_code(self, vat_info):
        vat_info = (vat_info or '').strip()
        if not vat_info:
            raise UserError(_("Vui lòng nhập mã số thuế vào field 'Thông tin MST'."))
        tax_code = None
        try:
            vat_data = json.loads(vat_info)
            if isinstance(vat_data, dict) and 'taxID' in vat_data:
                tax_code = str(vat_data['taxID']).strip()
        except ValueError:
            pass
        if not tax_code:
            tax_code = ''.join(c for c in vat_info if c.isdigit() or c == '-').strip()
        if len(''.join(filter(str.isdigit, tax_code))) < 10:
            raise UserError(_(
                "Mã số thuế không hợp lệ. Vui lòng nhập mã số thuế "
                "(ví dụ: 0100109106 hoặc 0100109106-507) vào field 'Thông tin MST'."
            ))
        return tax_code

    def api_lookup_tax_info(self, vat_info):
        """Look up a tax code on XInvoice and return einvoice_* values."""
        tax_code = self._einvoice_tax_code(vat_info)
        try:
            response = requests.get(TAX_LOOKUP_URL % tax_code, timeout=TAX_LOOKUP_TIMEOUT)
        except RequestException:
            raise UserError(_('Không thể kết nối đến API tra cứu mã số thuế (Lỗi kết nối).'))
        if response.status_code == 404:
            raise UserError(_('Mã số thuế %s tra cứu không hợp lệ') % tax_code)
        try:
            response.raise_for_status()
            data = response.json()
        # requests' JSONDecodeError is both ValueError and RequestException.
        except ValueError as e:
            raise UserError(_('Dữ liệu trả về từ API không hợp lệ: %s') % e)
        except RequestException:
            raise UserError(_('Không thể kết nối đến API tra cứu mã số thuế (Lỗi kết nối).'))
        if not data or not isinstance(data, dict):
            raise UserError(_('Mã số thuế %s tra cứu không hợp lệ') % tax_code)
        return {
            'einvoice_vat': data.get('taxID', '') or tax_code,
            'einvoice_partner_id': data.get('taxID', '') or tax_code,
            'einvoice_name': data.get('name', ''),
            'einvoice_buyer_name': data.get('name', ''),
            'einvoice_address': data.get('address', ''),
        }

    def button_get_einvoice_info(self):
        self.ensure_one()
        self.write(self.api_lookup_tax_info(self.einvoice_vat_info))
        return True
