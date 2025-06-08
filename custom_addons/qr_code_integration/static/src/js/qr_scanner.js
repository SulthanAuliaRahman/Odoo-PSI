odoo.define('qr_code_integration.qr_scanner', function(require) {
    'use strict';

    const { PosComponent } = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('@web/core/utils/hooks');

    class QRScannerButton extends PosComponent {
        static template = 'QRScannerButton';
        setup() {
            super.setup();
            useListener('click', this.onClick);
        }

        async onClick() {
            try {
                if (!window.Html5Qrcode) {
                    this.showPopup('ErrorPopup', {
                        title: this.env._t('Library Error'),
                        body: this.env._t('html5-qrcode library not loaded!'),
                    });
                    return;
                }
                const scanner = new Html5Qrcode("qr-reader");
                await scanner.start(
                    { facingMode: "environment" },
                    { fps: 10, qrbox: 250 },
                    (decodedText) => {
                        scanner.stop();
                        this.env.posbus.trigger('barcode_scanned', { barcode: decodedText });
                        this.showPopup('ConfirmPopup', {
                            title: this.env._t('QR Code Scanned'),
                            body: this.env._t('QR Code: ') + decodedText,
                        });
                    },
                    (errorMessage) => {
                        console.warn('QR Scan error: ', errorMessage);
                    }
                );
            } catch (err) {
                console.error('Failed to start scanner: ', err);
                this.showPopup('ErrorPopup', {
                    title: this.env._t('Scanner Error'),
                    body: this.env._t('Failed to start QR scanner.'),
                });
            }
        }
    }

    Registries.Component.add(QRScannerButton);

    ProductScreen.addControlButton({
        component: QRScannerButton,
        condition: function() {
            return true; // Always show the button
        },
    });

    return QRScannerButton;
});