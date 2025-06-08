from odoo import http
from odoo.http import request

class XenditController(http.Controller):
    @http.route('/payment/xendit/redirect', type='http', auth='public', methods=['POST'])
    def xendit_redirect(self, **post):
        return request.render('xendit_payment.xendit_payment_form', post)

    @http.route('/payment/xendit/callback', type='json', auth='public', methods=['POST'])
    def xendit_callback(self):
        data = request.jsonrequest
        if data.get('status') == 'PAID':
            transaction = request.env['payment.transaction'].sudo().search([('reference', '=', data.get('external_id'))], limit=1)
            if transaction:
                transaction._set_done()
        return {'status': 'received'}

    @http.route('/pos/xendit/generate_qr', type='json', auth='public')
    def pos_xendit_generate_qr(self, amount, reference, acquirer_id):
        acquirer = request.env['payment.acquirer'].sudo().browse(int(acquirer_id))
        if acquirer.provider != 'xendit':
            return {'error': 'Invalid acquirer'}
        return acquirer.pos_xendit_generate_qr(amount, reference)