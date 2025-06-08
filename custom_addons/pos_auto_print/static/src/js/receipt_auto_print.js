odoo.define('pos_auto_print.receipt_auto_print', function (require) {
    'use strict';

    const Registries = require('point_of_sale.Registries');
    const ReceiptScreen = require('point_of_sale.ReceiptScreen');

    const ReceiptAutoPrint = (ReceiptScreen) =>
        class extends ReceiptScreen {
            async _onMounted() {
                super._onMounted();
                if (this.env.pos.config.auto_print_receipt) {
                    this.printReceipt();
                    setTimeout(() => {
                        this.env.pos.push_order(this.env.pos.get_order());
                        this.showScreen('ProductScreen');
                    }, 1000);
                }
            }
        };

    Registries.Component.extend(ReceiptScreen, ReceiptAutoPrint);
});
