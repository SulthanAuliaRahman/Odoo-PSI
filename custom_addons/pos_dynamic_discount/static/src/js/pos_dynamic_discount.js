odoo.define('pos_dynamic_discount.pos_dynamic_discount', function (require) {
    "use strict";

    const PosComponent = require('point_of_sale.PosComponent');
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    const { useState } = owl;

    const PosDynamicDiscountPaymentScreen = PaymentScreen =>
        class extends PaymentScreen {
            setup() {
                super.setup();
                this.state = useState({ discountApplied: 0.0, ruleName: '' });
                this.checkDiscountRule();
            }

            async checkDiscountRule() {
                const currentTime = new Date().getHours() + (new Date().getMinutes() / 60);
                const currentDay = new Date().toLocaleString('en-us', { weekday: 'long' }).toLowerCase();
                const posConfig = this.env.pos.config;

                const rules = await this.rpc({
                    model: 'pos.discount.rule',
                    method: 'search_read',
                    domain: [['pos_config_id', '=', posConfig.id]],
                    fields: ['start_time', 'end_time', 'day_of_week', 'discount_percentage', 'name'],
                });

                for (const rule of rules) {
                    if (rule.day_of_week === currentDay &&
                        currentTime >= rule.start_time &&
                        currentTime < rule.end_time) {
                        this.state.discountApplied = rule.discount_percentage;
                        this.state.ruleName = rule.name;
                        this.applyDiscount();
                        this.displayDiscountMessage();
                        break;
                    }
                }
            }

            applyDiscount() {
                if (this.state.discountApplied > 0) {
                    const order = this.env.pos.get_order();
                    const total = order.get_total_with_tax();
                    const discountAmount = (total * this.state.discountApplied) / 100;
                    order.set_discount(discountAmount);
                }
            }

            displayDiscountMessage() {
                const order = this.env.pos.get_order();
                const discountAmount = order.get_discount();
                if (discountAmount > 0) {
                    const message = `Discount Applied: ${discountAmount.toFixed(2)} IDR (${this.state.discountApplied}% - ${this.state.ruleName})`;
                    const discountDiv = document.createElement('div');
                    discountDiv.className = 'discount-info';
                    discountDiv.style.margin = '10px';
                    discountDiv.style.padding = '10px';
                    discountDiv.style.backgroundColor = '#e0ffe0';
                    discountDiv.style.border = '1px solid #00ff00';
                    discountDiv.innerHTML = `<p><strong>${message}</strong></p>`;

                    const orderlinesDiv = this.el.querySelector('.orderlines');
                    if (orderlinesDiv) {
                        orderlinesDiv.insertAdjacentElement('afterend', discountDiv);
                    } else {
                        // Fallback: Append to the payment screen container
                        const screenContainer = this.el.querySelector('.payment-screen');
                        if (screenContainer) {
                            screenContainer.appendChild(discountDiv);
                        }
                    }
                }
            }
        };

    Registries.Component.extend(PaymentScreen, PosDynamicDiscountPaymentScreen);
    return PosDynamicDiscountPaymentScreen;
});